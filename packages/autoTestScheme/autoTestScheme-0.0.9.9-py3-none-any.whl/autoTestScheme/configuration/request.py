import os
import sys
import allure
import copy
import time
import inspect
import requests

from urllib.parse import urlencode
from . import api
from ..common import config, constant, logger


class requestBase(api.Api):

    def __init__(self):
        self.setup_hook_list = []
        self.teardown_hook_list = []
        self.logger = logger
        self.is_hook = True
        self.session = requests.Session()
        self.agreement = 'http'  # 协议
        self.base_url = None # 域名
        self.subdomain = None # 子域名
        self.catch_response = False # locust的时候使用
        self.kwargs = {} # request配置文件内的参数

    def set_session(self, client):
        self.session = client

    def register_setup_hook(self, hook):
        """
        注册前置钩子
        :param hook:
        :return:
        """
        self.setup_hook_list.append(hook)

    def register_teardown_hook(self, hook):
        """
        注册后置钩子
        :param hook:
        :return:
        """
        self.teardown_hook_list.append(hook)

    def get_url(self, path):
        '''
            获取网址
        '''
        if self.subdomain is None:
            base_url = self.base_url
        else:
            base_url = self.subdomain + '.' + self.base_url
        url = '{}://{}{}'.format(self.agreement, base_url, path)
        return url

    def send(self, api_id, params={}, json={}, data={}, timeout=None, title=None, is_json=True):
        request = self.get_api(api_id)
        request['params'] = params
        request['json'] = json
        request['data'] = data
        if timeout is not None:
            request['timeout'] = timeout
        if title is not None:
            request['title'] = title
        response = self._excute(request)
        if is_json is True:
            return response.json()
        return response

    def close_hook(self):
        self.is_hook = False

    def open_hook(self):
        self.is_hook = True

    def execute(self, request):
        """
            发送请求
        """
        if self.is_hook is True:
            for hook in self.setup_hook_list:
                self.excute_kwargs(hook, request)
        request['title'] = request.get('title') if request.get('title') is not None else request.get('path')
        with allure.step(request['title']):
            self.logger.debug('发送请求：{}'.format(request['title']))
            response = self._excute(request)
            if self.is_hook is True:
                for hook in self.teardown_hook_list:
                    self.excute_kwargs(hook, request)
            return response

    def excute_kwargs(self, hook, request):
        kwarg = {}
        kwargs = {'request': request, 'session': self.session, 'kwargs': self.kwargs}
        for i in inspect.getfullargspec(hook).args:
            if i in ['self', 'cls']:
                continue
            kwarg[i] = kwargs[i]
        hook(**kwarg)
    
    def copy_request(self, request):
        new_request = {}
        if 'files' not in request:
            new_request = copy.deepcopy(request)
        else:
            for key in request:
                if key == 'files':
                    new_request['files'] = request['files']
                else:
                    new_request[key] = copy.deepcopy(request[key])
        return new_request

    def _excute(self, request):
        current_time = time.time()
        new_request = self.copy_request(request)
        new_request['url'] = self.get_url(new_request.get('path'))
        if 'path' in new_request:
            del new_request['path']
        new_request['verify'] = False
        if self.catch_response is True:
            new_request['url'] = new_request['url'] + '?' + urlencode(new_request['params'])
            new_request['name'] = new_request['title']
            del new_request['params']
            new_request['catch_response'] = True
        for i in ['id', 'title']:
            if i in new_request:
                del new_request[i]
        result = self.session.request(**new_request)
        response = result.text.replace('\n', '').replace('\r', '').replace('  ', '')
        self.logger.debug('请求参数：method：{}，url：{}, \nparams:{}, headers:{}, \ndata:{}, json:{}, \n返回：{},时间:{}, '
                          '状态码:{}'.format(new_request.get('method'), new_request.get('url'), new_request.get('params'),
                                            new_request.get('headers'), new_request.get('data'), new_request.get('json'),
                                            response, time.time() - current_time, result.status_code))
        if self.catch_response is True:
            return result
        return result

    def qs_parse(self, data):
        for key in list(data.keys()):
            value = data[key]
            if type(value) == dict:
                del data[key]
                for _key in list(value.keys()):
                    data[key + '[' + _key + ']'] = value[_key]
            elif type(value) == list:
                del data[key]
                for _key in range(len(value)):
                    data[key + '[' + str(_key) + ']'] = value[_key]
