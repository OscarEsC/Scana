from distutils.core import setup
import py2exe, sys, os

# Tomado de
# http://www.py2exe.org/index.cgi/SingleFileExecutable

sys.argv.append('py2exe')

setup(
options={'py2exe':{'bundle_files': 1, 'compressed': True}},
windows=[{'script': 'scana.py'}],
zipfile = None,	
)