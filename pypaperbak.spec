# -*- mode: python -*-

block_cipher = None


a = Analysis(['pypaperbak/__main__.py'],
             pathex=['/home/user/projetos/pypaperbak'],
             binaries=[],
             datas=[('README.md', '.'), ('LICENSE.md', '.'), ('samples', 'samples')],
             hiddenimports=['png'],
             hookspath=['pyinstaller-hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pypaperbak',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pypaperbak')
