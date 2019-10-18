# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['buscarPosteosFacebook.py'],
             pathex=['C:\\Users\\pepe\\Desktop\\git\\buscarPosteosFacebook', 'C:\Program Files\Python37\Lib\site-packages'],
             binaries=[ ('C:\\geckodriver.exe', '.\\selenium\\webdriver') ],
             datas=[('config.json', '.'), ( 'data', 'data' ), ( 'tldextract', 'tldextract' ), ('C:\\geckodriver.exe', '.\\selenium\\webdriver')],
             hiddenimports=['lxml.html', 'lxml.includes', 'tdlextract'],
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
          name='buscarPosteosFacebook',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='buscarPosteosFacebook')
