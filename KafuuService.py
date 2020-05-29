# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.2
@date: 2020-4-16

KafuuService good
'''

import ctypes, sys
import win32api as _a
import win32con as _c
import WebService
from SystemHandler import kill_self
from ApiHandler import add_hosts
from Utils import logg


def check_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin() != True:
            text = "您好！欢迎使用osu!Kafuu服务系统~~\n程序需要管理员权限才能够正常运行，请您在随后的选项弹窗选择“是”。"
            title = "提示！"
            options = _c.MB_ICONASTERISK | _c.MB_SYSTEMMODAL
            message_box(text, title, options)
            run_with_admin()
    except Exception as err:
        text = f"出现以下错误：\n{err}\n\n请您截图报告开发者以解决问题，谢谢！"
        title = "致命错误！"
        options = _c.MB_SYSTEMMODAL | _c.MB_ICONHAND | _c.MB_ABORTRETRYIGNORE
        action = message_box(text, title, options)
        # stop
        if action == 3:
            sys.exit(0)
        # retry
        elif action == 4:
            run_with_admin()
        # pass
        else:
            logg(f'已忽略问题{err}继续运行')


def run_with_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)


def message_box(text, title, options):
    default = '来自KafuuService的话~'
    return _a.MessageBox(0, text, title + default, options)


def main(dev):  
    if dev != True: 
        check_admin()
    kill_self()
    add_hosts()
    WebService.run_app()


if __name__ == '__main__':
    # for dev
    main(True)

