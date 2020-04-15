# -*- mode: python ; coding: utf-8 -*-
# KafuuService packaging

block_cipher = None


a = Analysis(['Entrance.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ('cert', 'cert'), 
                 ('static\\jquery.min.js', 'static'), 
                 ('static\\MainPage.html', 'static'), 
                 ('static\\icon.ico', 'static'), 
                 ('static\\System.Security.dll', 'static'), 
                 ('nginx', 'nginx')],
             hiddenimports=[
                 'DllLoader', 
                 'Entrance', 
                 'CertHandler', 
                 'SystemHandler', 
                 'KafuuService', 
                 'HostsHandler', 
                 'ApiHandler', 
                 'Utils', 
                 'WebService', 
                 'wmi', 
                 'json', 
                 'tornado.web', 
                 'tornado.ioloop', 
                 'clr'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='KafuuService',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , version='static\\version', uac_admin=True, icon='static/icon.ico', resources=['static/KafuuService.exe.manifest,1'])
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='KafuuService')
