# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.4
@date: 2020-4-16

HostHandler nice to manage hosts
'''

from Utils import logg
from SystemHandler import system_root
from os.path import isfile


class HostManager:
    def __init__(self):
        sys_root = system_root()
        self.sys_root = sys_root
        self.hosts_path = f'{sys_root}\\system32\\drivers\\etc\\hosts'
        self.open_path = self.hosts_path
        if isfile(self.hosts_path) != True:
            logg('请手动选择hosts文件')
        self.server_ip = '127.0.0.1'
        self.addresses = [
            'osu.ppy.sh',
            'c.ppy.sh',
            'c1.ppy.sh',
            'c2.ppy.sh',
            'c3.ppy.sh',
            'c4.ppy.sh',
            'c5.ppy.sh',
            'c6.ppy.sh',
            'ce.ppy.sh',
            'a.ppy.sh',
            'osukafuu-service.net'
        ]


    # 装饰器，用于打开hosts文件
    def open_hosts(func):
        def wrapper(self, *args):
            try:
                action = 'w' if 'write' in func.__name__ else 'r'
                with open(self.open_path, action, encoding='utf-8') as hosts:
                    return func(self, hosts, *args)
            except Exception as err:
                logg(f'处理时出错！函数：{func.__name__}，文件打开方式：{action}，错误：{err}')
                return False
        return wrapper
    
    
    # 尝试删除有关服务器的hosts记录
    @open_hosts
    def delete_hosts(self, hosts):
        done = 0
        lines = hosts.readlines()
        for index, line in enumerate(lines):
            host = line.replace('\n', '').split(' '*4)
            if host[0] == self.server_ip and host[1] in self.addresses:
                lines[index] = ''
                done += 1
        if done > 0:
            hosts.close()
            if self.__write_hosts(lines) == True:
                logg(f'已清除相关hosts记录共{done}条！')
                return True
            else:
                logg(f'清楚hosts失败！可能是没有管理员权限')
                return False
        else:
            logg(f'未找到相关hosts记录，无需删除！')
            return True

    
    
    # 添加服务器到hosts文件中
    def add_hosts(self):
        check = self.check_hosts()
        if check != 1:
            if check == 0:
                self.backup_hosts()
                self.delete_hosts()
            try:
                logg(f'添加服务器到hosts中...')
                origin_hosts = self.get_hosts()
                make_hosts = ['{}{}{}\n'.format(self.server_ip, ' '*4, i) for i in self.addresses]
                return self.__write_hosts(origin_hosts + make_hosts)
            except Exception as err:
                logg(f'添加hosts时出错：{err}')
                return False
        else:
            logg(f'无需添加hosts！已经添加过了！')
            return True
    
    
    @open_hosts
    def get_hosts(self, hosts):
        logg(f'获取原hosts文件...')
        content = hosts.readlines()
        hosts.close()
        return content
    
    
    # 备份hosts文件
    @open_hosts
    def backup_hosts(self, hosts):
        logg(f'备份hosts文件...')
        content = hosts.readlines()
        hosts.close()
        self.open_path = self.hosts_path + '.backup'
        result = self.__write_hosts(content)
        self.open_path = self.hosts_path
        if result == True:
            logg(f'备份hosts文件成功！')
        else:
            logg(f'备份hosts文件失败！')
        return result
    
    
    # 检查服务器是否已经在hosts文件中
    @open_hosts
    def check_hosts(self, hosts):
        done = 0
        lines = hosts.readlines()
        logg(f'检查hosts文件完整性...')
        for line in lines:
            host = line.replace('\n', '').split(' '*4)
            if host[0] == self.server_ip and host[1] in self.addresses:
                done += 1
        if done == 0:
            logg(f'未找到hosts记录！')
            return -1
        elif done < len(self.addresses):
            logg(f'hosts记录不完整，需要进行修复！')
            return 0
        elif done >= len(self.addresses):
            logg(f'...ok！hosts记录完整')
            return 1
    
    
    # 写入hosts
    @open_hosts
    def __write_hosts(self, hosts, lines):
        try:
            hosts.writelines(lines)
            logg(f'hosts文件内容已更新！')
            return True
        except:
            logg(f'hosts文件更新失败！')
            return False
        

