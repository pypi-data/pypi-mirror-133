from setuptools import setup

import shutil
import os.path

lpath = os.path.expandvars("$LOCAL_PATH")

shutil.copyfile(os.path.join(lpath, 'LICENCE'), os.path.join(lpath, 'products', 'lib', 'python3', 'LICENCE'))


setup()
