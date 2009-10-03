from distutils.core import setup
import os
import sys
import glob
import fnmatch
from os.path import join

NAME = 'LibRPG'
VERSION = '0.4'

def recursive_list_dir(dir):
    data = []
    for path, _, files in os.walk(join('librpg', dir)):
        for filename in files:
            p = path.split('\\')
            data.append(join('\\'.join(p[1:]), filename))
    return data

def get_data_files(test, tools):
    data = []

    data.extend(recursive_list_dir('data'))

    if test:
        data.append(join('test', '*.*'))
        data.append(join('test', 'worldtest', '*.*'))
    
    if tools:
        data.append(join('tools', 'charset', '*.scm'))
        data.append(join('tools', 'charset', '*.py'))
        data.append(join('tools', 'tileset', '*.py'))
    
    return data

def main():
    # if sys.version < '2.6':
        # sys.exit('ERROR: Sorry, python 2.6 is required for LibRPG.')

    if '--complete' in sys.argv:
        data = get_data_files(test=True, tools=True)
        sys.argv.remove('--complete')
    else:
        data = get_data_files(test=False, tools=False)

    setup(name=NAME,
          version=VERSION,
          provides=['librpg'],
          author='Henrique Nakashima',
          author_email='henrique.nakashima@gmail.com',
          url='http://code.google.com/p/librpg/',
          license='LGPL',
          description='A framework over Pygame for developing 2D RPGs',
          long_description='A framework based on Pygame for developing \
                            old-school 2D tile-based RPGs.',
          packages = ['librpg', 'librpg.menu'],
          package_dir={'librpg': 'librpg',
                       'librpg.menu': os.path.join('librpg', 'menu')},
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

# To include tests/ and tools/ in any dist
# Add '--complete' to the end of the command line
