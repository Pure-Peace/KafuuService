# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.2
@date: 2020-4-16

CertHandler with .net love
'''

from Utils import logg
from SystemHandler import base_path
import DllLoader as _d
import os


class CertManager:
    def __init__(self):
        logg('初始化证书管理器...')
        try:
            self.cert_file = base_path('cert\\cert.crt')
            self.subject_name = '*.ppy.sh'
            self.OpenFlags = _d.OpenFlags
            self.X509Certificate2 = _d.X509Certificate2
            self.X509FindType = _d.X509FindType
            self.store = _d.X509Store(_d.StoreName.Root, _d.StoreLocation.CurrentUser)
            logg('证书管理器初始化完毕！')
        except Exception as err:
            logg(f'证书管理器初始化失败，错误：{err}')


    def add_cert(self):
        logg('正在安装证书...')
        try:
            self.store.Open(self.OpenFlags.ReadWrite)
            cert = self.X509Certificate2(self.cert_file)
            logg(f'安装证书：{cert.Subject}')
            self.store.Add(cert)
            self.store.Close()
            return True
        except Exception as err:
            logg(f'证书安装失败：{err}')
            self.store.Close()
            return False
    
    
    def remove_cert(self):
        logg('正在移除证书...')
        done = 0
        try:
            self.store.Open(self.OpenFlags.ReadWrite)
            certificates = self.store.Certificates.Find(self.X509FindType.FindBySubjectName, self.subject_name, True)
            for cert in certificates:
                logg(f'找到证书：{cert}\n尝试删除...')
                self.store.Remove(cert)
                done += 1
            self.store.Close()
            logg(f'处理完毕，共移除证书{done}张！')
            return True
        except Exception as err:
            logg(f'删除证书时出现错误：{err}，处理完成数量：{done}')
            self.store.Close()
            return False

    
    def cert_status(self):
        logg('正在查询证书安装情况...')
        try:
            self.store.Open(self.OpenFlags.ReadOnly)
            certificates = self.store.Certificates.Find(self.X509FindType.FindBySubjectName, self.subject_name, True)
            self.store.Close()
            if len([i for i in certificates]) > 0:
                logg('证书已安装！')
                return True
            logg('证书未安装！')
            return False
        except Exception as err:
            logg(f'查询证书安装状态时失败：{err}')
            return False
        

if __name__ == '__main__':
    cm = CertManager()

