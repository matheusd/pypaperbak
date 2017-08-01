#!/bin/env python

import os
import shutil

exec(open('pypaperbak/_version.py').read())

shutil.rmtree('build', True)
shutil.rmtree('dist', True)
os.makedirs('releases', exist_ok=True)


os.system('pyinstaller pypaperbak.spec')
os.system('tar -C dist -cjf releases/pypaperbak-%s-linux-x64.tar.bz2 pypaperbak' % __version__)
