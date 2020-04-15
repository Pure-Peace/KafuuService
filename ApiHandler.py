# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.3
@date: 2020-4-16

ApiHandler yes
'''

from HostsHandler import HostManager
from CertHandler import CertManager
import SystemHandler as sy
from Utils import logg


hm = HostManager()
cm = CertManager()


def get_cert_status():
    return cm.cert_status()


def add_cert():
    return cm.add_cert()


def remove_cert():
    return cm.remove_cert()


def get_nginx_status():
    return 1 if (sy.check_nginx() == True) else -1


def get_service_status():
    return {'status': 1, 'nginx': get_nginx_status()}


def check_hosts():
    return hm.check_hosts()


def add_hosts():
    return hm.add_hosts()


def backup_hosts():
    return hm.backup_hosts()


def delete_hosts():
    return hm.delete_hosts()


def write_sys_info():
    return sy.write_all()


def get_sys_info(what=None):
    if what in (None, '', 'all'):
        return sy.get_all()
    elif what in (
        'cpu',
        'mainboard',
        'bios',
        'disk',
        'memory',
        'battery',
        'mac',
        'user',
        'system',
        'system_root'
    ):
        func = getattr(sy, what, None)
        if callable(func):
            return func()
    else:
        return -1


def start_nginx():
    return sy.run_nginx()


def stop_nginx():
    return sy.stop_nginx()


def program_dir():
    return sy.base_path()


def exit_all():
    logg(f'apiHandle：停止并退出所有服务，并返回osu官服')
    h1 = delete_hosts()
    h2 = sy.exit_all_service()
    return {'delete_hosts': h1, 'exit_all': h2}


def exit_api():
    logg(f'apiHandle：退出api')
    return sy.exit_api()



    


