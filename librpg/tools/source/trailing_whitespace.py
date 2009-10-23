from sys import argv
import glob

def check_parameters():
    argc = len(argv)
    if argc < 2 or (argc < 3 and '--replace' in argv):
        print 'Usage: python trailing_whitespace.py [--replace] [file 1] [file 2] ...'
        exit()

def parse_parameters():
    result = []
    replace = False
    for s in argv[1:]:
        if s == '--replace':
            replace = True
        result.extend(glob.glob(s))
    return result, replace

def remove_whitespace(source, replace):
    f = file(source, 'r')
    in_file = [line for line in f]
    f.close()
    
    if replace:
        out_file = file(source, 'w')
    else:
        out_file = file(source + '.new', 'w')

    for line in in_file:
        new_line = line.rstrip()
        out_file.write(new_line + '\n')

    out_file.close()

if __name__ == '__main__':
    check_parameters()
    sources, replace = parse_parameters()
    for source in sources:
        remove_whitespace(source, replace)
    print 'Source files: %s' % ', '.join(sources)
