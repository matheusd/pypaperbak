#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import warnings
import subprocess

exec(open('pypaperbak/_version.py').read())

package_dir = 'pypaperbak'

# convert the README and format in restructured text (only when registering)
long_desc = ""
if os.path.exists("README.md"):
    try:
        cmd = ['pandoc', '--pypaperbakfrom=markdown', '--to=rst', 'README.md']
        long_desc = subprocess.check_output(cmd).decode("utf8")
    except Exception as e:
        warnings.warn("Exception when converting the README format: %s" % e)


setup(name='pypaperbak',
      version = __version__, 
      description = 'Backup and Restore from paper-based datastore',
      long_description = long_desc,
      author = 'Matheus Degiovani',
      author_email = 'opensource@matheusd.com',
      url = 'https://github.com/matheusd/pypaperbak',
      license = 'MIT',      
      packages = ['pypaperbak', ],
      package_dir = {'pypaperbak': package_dir},
      package_data = {'pypaperbak': ['samples/*']},
      install_requires = [
          'pyqrcode', 
          'zbarlight',
          'fpdf',
          'python-magic',
          'pypng'
      ],
      classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",            
            "Topic :: Software Development :: Libraries :: Python Modules",            
      ],
      keywords=["pdf", "qrcode", "png", "jpg"],
     )