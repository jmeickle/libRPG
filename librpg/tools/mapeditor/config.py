
width = 640
height = 480
depth = 32
#display flags -- see pygame display documentation section
#all flags: fullscreen doublebuf hwsurface opengl resizable noframe
flags = 'fullscreen doublebuf hwsurface'

tilesets = [
  {
    'name': 'castle',
    'image': 'tile/castle.bmp',
    'tilewidth': 32,
    'tileheight': 32,
    'anim':[{'start': 0,'end': 10,'milisec': 250},]
  },
  {
    'name': 'TREE',
    'image': 'tile/TREE.png',
    'tilewidth': 32,
    'tileheight': 32,
    'anim':[]
  }
]
