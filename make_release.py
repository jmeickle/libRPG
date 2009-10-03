import os
import shutil

from subprocess import check_call
from setup import NAME, VERSION

def get_filename(extension):
    return '%s-%s.%s' % (NAME, VERSION, extension)

def move(source_path, target_path, os_type):
    src = os.path.join(*source_path.split('/'))
    tgt = os.path.join(*target_path.split('/'))
    print 'move (%s, %s)' % (src, tgt)
    if os_type == 'win':
        print 'win'
        print os.listdir('dist')
        src = 'dist\\LibRPG-0.4.win32.exe'
        tgt = 'dist\\LibRPG-0.4.bundle.win32.exe'
        check_call(['dir'])
        check_call(['move', src, tgt])
    elif os_type == 'unix':
        print 'unix'
        check_call(['mv', src, tgt])

def cleanup():
    shutil.rmtree('dist')
    shutil.rmtree('build')

def main():
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

    check_call(['python', 'setup.py', 'sdist', '--formats=zip'])

if __name__ == '__main__':
    main()

