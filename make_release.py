import os
import shutil

from subprocess import check_call
from setup import NAME, VERSION

def get_filename(extension):
    return '%s-%s.%s' % (NAME, VERSION, extension)

def cleanup():
    shutil.rmtree('dist', True)
    shutil.rmtree('build', True)

def main():
    # Clean previous build
    cleanup()

    # Create bundle .exe installer (includes tools and tests)
    check_call(['python', 'setup.py', 'bdist', '--formats=wininst',
                '--complete'])
    os.rename('dist/%s' % get_filename('win32.exe'),
              'dist/%s' % get_filename('bundle.win32.exe'))

    # Create standard .exe installer
    check_call(['python', 'setup.py', 'bdist', '--formats=wininst'])
    os.rename('dist/%s' % get_filename('win32.exe'),
              'dist/%s' % get_filename('standard.win32.exe'))

    # Create source distribution
    check_call(['python', 'setup.py', 'sdist', '--formats=zip'])

if __name__ == '__main__':
    main()

