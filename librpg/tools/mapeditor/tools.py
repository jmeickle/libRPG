
def str_uint32(i):
    v = 0xFF
    v1 = chr(i & v)
    i = i >> 8
    v2 = chr(i & v)
    i = i >> 8
    v3 = chr(i & v)
    i = i >> 8
    v4 = chr(i & v)
    i = i >> 8
    return v4+v3+v2+v1

def uint32_str(s):
    v  = ord(s[0]) << 24
    v += ord(s[1]) << 16
    v += ord(s[2]) << 8
    v += ord(s[3])
    return v

def str_uint8(i):
    v = 0xFF
    v1 = chr(i & v)
    return v1

def uint8_str(s):
    v = ord(s[0])
    return v
