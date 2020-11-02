#!/usr/bin/python
# coding=utf-8
from requests.sessions import Session
from functools import wraps
from jinja2 import Template
from copy import deepcopy

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import inspect

from .utils import format_json
from .json_processor import JSONProcessor
from fs.Trace import Trace
from engine.runner import Runner
import json
import traceback


class HttpRequest(object):
    def __init__(self, url='', method='get', **kwargs):
        self.tmp_url = url
        self.url = url
        self.method = method
        self.decorator_args = kwargs
        self.func_return = None
        self.func_doc = None
        self.func_im_self = None
        self.session = None

    def __call__(self, func):
        self.func = func
        self.is_class = False
        try:
            if inspect.getargspec(func).args[0] == 'self':
                self.is_class = True
        except IndexError:
            pass

        def fun_wrapper(*args, **kwargs):
            log = Trace("HttpRequest::fun_wrapper")
            self.func_return = self.func(*args, **kwargs) or {}
            self.func_im_self = args[0] if self.is_class else object
            self.decorator_args.update(self.func_return)
            try:
                self.func.__doc__ = self.func.__doc__.decode('utf-8')
            except:
                pass
            self.func_doc = (self.func.__doc__ or self.func.__name__).strip()
            self.create_url()
            self.create_session()
            return Request(self.method, self.url, self.session, self.func_doc, self.decorator_args)

        return fun_wrapper

    def create_url(self):
        """
        生成http请求的url
        """

        # 使用在函数中定义的url变量,如果没有,使用装饰器中定义的

        base_url = getattr(self.func_im_self, 'base_url', '')
        # print 'base_url = %s'%base_url
        self.url = self.func_return.get('url') or self.url
        # self.url = urljoin(base_url, self.url)
        self.url = urljoin(base_url, self.tmp_url)
        print 'url = %s' % self.url

    def create_session(self):
        """
        如果接收到的要变参数中有session,且为Session对象,赋值给session变量, 否则创建一个
        """
        log = Trace("HttpRequest::create_session")
        if self.is_class:
            self.session = getattr(self.func_im_self, 'session', None)
            if not isinstance(self.session, Session):
                session = Session()
                setattr(self.func_im_self, 'session', session)
                self.session = session
        elif isinstance(self.func_return.get('session'), Session):
            self.session = self.func_return.get('session')
        else:
            self.session = Session()


request = HttpRequest

LOG_TEMPLATE = u'''
******************************************************
{% for index, item in items %}
{{ index + 1 }}、{{ item['desc'] }}
{{ item['value'] }}
{% endfor %}
'''


def logging(className, funcName):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Logger = Trace("%s::%s" % (className, funcName))
            try:
                return func(*args, **kwargs)
            except Exception, e:
                errMsg = traceback.format_exc()
                Logger.error("error: %s" % errMsg)

        return wrapper

    return decorator


def context(func):
    def wrapper(self):
        self._request()
        try:
            res = func(self)
        finally:
            self._log()
        return res

    return wrapper


class Request(object):
    """
    请求对象模型
    """

    def __init__(self, method, url, session, doc, args):
        log = Trace("Request::_log")
        self.method = method
        self.url = url
        self.session = session
        self.doc = doc
        self.args = args
        self.response = None
        self.runner = Runner()
        self.locust_flag = False  # 对于locust client需要打印response log
        """
        对locust_client特殊处理,暂时没想到优雅的处理方式
        """
        if self.args.has_key('http_client_session'):
            http_client = self.args['http_client_session']
            if http_client is not None:
                self.runner = Runner(http_client)
                self.locust_flag = True
            del self.args['http_client_session']

        self.log_content = [
            dict(desc=u'接口描述', value=doc),
            dict(desc=u'请求url', value=url),
            dict(desc=u'请求方法', value=method),
        ]
        headers = deepcopy(args.get('headers', {}))
        headers.update(session.headers)

        params = args.get('data') if args.get('data') else args.get('params')
        if isinstance(params, dict):
            if params.get('X-Token'):
                args['headers'] = headers
                args['headers']['X-Token'] = params.get('X-Token')
                del params['X-Token']
            if params.get('Pid'):
                args['headers'] = headers
                args['headers']['Pid'] = str(params.get('Pid'))  # http header 字段值必须是字符串
                del params['Pid']
            #     """
            #     data=immediateExecute&data=manage
            #     """
            # self._dealwithToken(params)
            self.args['data'] = json.dumps(params)
            # args['data'] = json.dumps(params, ensure_ascii=False)
        elif isinstance(params, unicode) or isinstance(params, str):
            """
            {'headers': {'Content-Type': 'application/json'}, 'data': u'{"X-Token": "289_9c3b57cd-bba8-4a56-a8e3-19e341c1db66", "data": {"projectId": 110, "manageDesc": "sceneDesc_18598603689", "manageName": "sceneName_18878400579"}}'}
            X-Token 特殊处理，data传过来是一个json串，需要转成dict提取X-Token字段
            """
            params_ = json.loads(params, encoding='utf-8')
            self._dealwithToken(params_)
            print 'params_ = %s' % params_
            self.args['data'] = json.dumps(params_)
            # if params.get('X-Token'):
            #     args['headers'] = headers
            #     args['headers']['X-Token'] = params.get('X-Token')
            #     del params['X-Token']
            #     """
            #     data=immediateExecute&data=manage
            #     """
            #     args['data'] = json.dumps(params,ensure_ascii=False)

        if args.get('X-Token'):
            """
            {'files': {'partFile': <open file 'D:\\pic\\nansheng.png', mode 'rb' at 0x02DEC968>}, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'}, 
            'X-Token': u'289_8aca62e6-e396-4a9b-a079-540c24991658'}
            X-Token 特殊处理，文件上传post请求无需构造data字段,requests.post(url=url,headers=headers,files=files)
            """
            args['headers'] = headers
            args['headers']['X-Token'] = args.get('X-Token')
            del args['X-Token']
        # if args.get('Pid'):
        #     args['headers'] = headers
        #     args['headers']['Pid'] = args.get('Pid')
        #     del args['Pid']

        # import urllib
        # params = urllib.urlencode(params, 'utf-8')
        # log.debug('headers = %s'%repr(headers))
        # headers.update(session.headers)
        # log.debug('headers = %s'%repr(headers))

        if headers:
            self.log_content.append(dict(
                desc=u'请求headers', value=format_json(headers)
            ))

        if args.get('params'):
            self.log_content.append(dict(
                desc=u'请求url参数', value=format_json(args.get('params'))
            ))

        if args.get('data'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(args.get('data'))
            ))

        if args.get('json'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(args.get('json'))
            ))

    def _dealwithToken(self, params):
        if params.get('X-Token'):
            self.args['headers'] = self.headers
            self.args['headers']['X-Token'] = params.get('X-Token')
            del params['X-Token']
            print 'params = %s' % params
            """
            data=immediateExecute&data=manage
            """
        # self.args['data'] = json.dumps(params)

    @context
    def to_json(self):
        try:
            response_json = self.response.json()
            self.log_content.append(dict(
                desc=u'响应结果',
                value=format_json(response_json)
            ))
        except ValueError:
            self.log_content.append(dict(
                desc=u'响应结果',
                value=self.response.content.decode('utf-8')
            ))
            raise ValueError(u'No JSON object in response')
        return JSONProcessor(response_json)

    @context
    def to_content(self):
        response_content = self.response.content
        self.log_content.append(dict(desc=u'响应结果', value=response_content.decode('utf-8')))
        return response_content

    @context
    def to_headers(self):
        # TypeError: {'Date': 'Mon, 12 Feb 2018 09:49:37 GMT', 'Content-Length': '0',
        # 'Location': 'http://xxx.com/xxx/xxx/xxx/xxx?xxx=10&kind=%E9%99%86%E9%B2%B8
        # , 'Connection': 'keep-alive', 'Server': 'Tengine'} is not JSON serializable
        try:
            response_headers = dict(self.response.headers)
            if response_headers.has_key('Date'):
                del response_headers['Date']
            self.log_content.append(dict(
                desc=u'响应headers',
                value=format_json(response_headers)
            ))
        except ValueError:
            self.log_content.append(dict(
                desc=u'响应headers',
                value=self.response.headers.decode('utf-8')
            ))
            raise ValueError(u'No JSON object in response')
        return JSONProcessor(response_headers)

    @property
    def json(self):
        return self.to_json()

    @property
    def content(self):
        return self.to_content()

    @property
    def headers(self):
        return self.to_headers()

    def _log(self):
        pass
        # log = Trace("Request::_log")
        # log.info(Template(LOG_TEMPLATE).render(items=enumerate(self.log_content)))

    def _request(self):
        if not self.response:
            # print 'self.args = %s'%self.args
            # self.response = self.session.request(self.method, self.url, **self.args)
            self.response = self.runner.run_test(self.url, self.method, self.args)
            # print 'response = %s'%self.response
            if self.locust_flag:
                log = Trace("Request::_log")
                log.debug('response = %s' % (self.response.content.decode('utf-8')))

    def __getattr__(self, item):
        self._request()
        self._log()
        return getattr(self.response, item)


def make_session():
    return Session()
