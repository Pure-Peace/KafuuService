# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.3
@date: 2020-4-16

WebService i love
'''

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
import ApiHandler as Api
from KafuuService import _a
from SystemHandler import base_path
from Utils import getTime, logg


version = '0.10'
port = 13377
static_path = base_path('static\\')
template_path = base_path('static\\')
main_page = 'MainPage.html'


apis = [
    {"title": f"切换服务器到Kafuu", "link": "api/add_hosts", "color": None},
    {"title": f"切换服务器到Bancho官服", "link": "api/delete_hosts", "color": None},
    {"title": "检查是否已切换到osu!Kafuu", "link": "api/check_hosts", "color": None},
    {"title": f"安装osu!Kafuu证书", "link": "api/add_cert", "color": None},
    {"title": "移除osu!Kafuu证书", "link": "api/remove_cert", "color": None},
    {"title": "仅退出控制台 (您可继续在osu!kafuu游玩)", "link": "api/exit_api", "color": None},
    {"title": "彻底停止并退出所有服务，并返回osu官服", "link": "api/exit_all", "color": "red"}
]


def render_data(**kw):
    kw['port'] = port
    kw['version'] = version
    kw['msg'] = kw.get('msg', '欢迎使用osu!Kafuu / Service Api 控制台')
    kw['show_tab'] = kw.get('show_tab', False)
    kw['cert_status'] = Api.get_cert_status()
    kw['hosts_status'] = Api.check_hosts()
    if kw['show_tab'] == True and kw.get('apis') == None:
        kw['apis'] = apis
    return kw


class IndexHandler(RequestHandler):
    def get(self):
        self.render(main_page, **render_data(show_tab=True))


class ServiceStatus(RequestHandler):
    def get(self):
        self.write(Api.get_service_status())


class ErrorHandler(RequestHandler):
    def get(self):
        self.render(main_page, **render_data(msg='没有找到这个页面哦~'))


class ApiTip(RequestHandler):
    def get(self):
       self.render(main_page, **render_data(msg='请输入完整的api地址哦，如 “api/status”'))


class ApiHandler(RequestHandler):
    def get(self, handle):
        func = getattr(Api, handle, None)
        re = {}
        if callable(func):
            temp = func()
            re['result'] = temp
            re['time'] = getTime(1)
            re['handle'] = handle
            logg(f'apiHandle：{handle} ({self.request.remote_ip}) done.')
            self.write(re) 
        else:
            self.render(main_page, **render_data(msg=f'没有找到 “{handle}” 这个api哦~'))


class SystemInfoHandler(RequestHandler):
    def get(self, handle):
        temp = Api.get_sys_info(handle)
        re = {}
        if temp == -1:
            self.render(main_page, **render_data(msg=f'没有找到 “{handle}” 这个系统信息api~'))
        else:
            re['result'] = temp
            re['time'] = getTime(1)
            re['handle'] = handle
            self.write(re)
    

handlers = [
    ("/", IndexHandler),
    ("/status", ServiceStatus),
    ("/api/get_sys_info/(\w+)", SystemInfoHandler),
    ("/api/(\w+)", ApiHandler),
    ("/api", ApiTip),
    (".*", ErrorHandler)
]


def run_app():
    app = Application(handlers, static_path=static_path, template_path=template_path, debug=False)
    app.listen(port)
    logg('KafuuService ver.{} NOW RUNNING...'.format(version))
    _a.ShellExecute(0, 'open', 'http://127.0.0.1:{}'.format(port), '','',1)
    IOLoop.current().start()
