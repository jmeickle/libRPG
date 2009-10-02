from distutils.core import setup
import os
import sys
import glob
import fnmatch
from os.path import join

def recursive_list_dir(dir):
    data = []
    for path, _, files in os.walk(join('librpg', dir)):
        for filename in files:
            p = path.split('\\')
            data.append(join('\\'.join(p[1:]), filename))
    return data

def  get_data_files():
    data = []

    data.extend(recursive_list_dir('data'))

    data.append(join('docs', 'roadmap.txt'))
    data.append(join('docs', 'faq.txt'))
    
    data.append(join('test', '*.*'))
    data.append(join('test', 'worldtest', '*.*'))
    
    data.append(join('tools', 'charset', '*.scm'))
    data.append(join('tools', 'charset', '*.py'))
    data.append(join('tools', 'tileset', '*.py'))
    
    return data

def main():
    if sys.version < '2.6':
           sys.exit('ERROR: Sorry, python 2.6 is required for LibRPG.')

    data = get_data_files()
    
    setup(name='LibRPG',
          version='0.4',
          provides=['librpg'],
          author='Henrique Nakashima',
          author_email='henrique.nakashima@gmail.com',
          url='http://code.google.com/p/librpg/',
          license='LGPL',
          description='A framework over Pygame for developing 2D RPGs',
          long_description='A framework based on Pygame for developing \
                       old-school 2D tile-based RPGs.',
          packages = ['librpg'],
          package_dir={'librpg': 'librpg'},
          package_data={'librpg': data})

if __name__ == '__main__':
    main()

# To install
# python setup.py install

# To build a .zip
# python setup.py bdist --format=zip

# To build an .exe Windows installer
# python setup.py bdist --formats=wininst

# To build an .exe Windows 64-bit installer
# python setup.py build --plat-name=win-amd64 bdist_wininst
