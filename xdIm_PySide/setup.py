'''
Created on 2011-1-4

@author: x00163361
'''
#from distutils.core import setup
#import py2exe
###setup(windows=["im.py"] )
#setup(windows=["serverManager.py"] ,)


import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "IM",
        version = "0.1",
        description = "IM.PY cx_Freeze  script",
#        executables = [Executable("im.py", base = base),Executable("serverManager.py", base = base)])
        executables = [Executable("serverManager.py", base = base)])
