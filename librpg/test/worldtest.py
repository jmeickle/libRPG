import librpg

from worldtest.myworld import MyWorld


def main():
    librpg.init()

    # Config graphics
    librpg.config.graphics_config.config(tile_size=32, object_height=32,
                                         object_width=32)

    # Create world
    try:
        w = MyWorld('save')
    except IOError:
        w = MyWorld()

    # Run
    w.gameloop()

    # Terminate
    exit()

if __name__ == '__main__':
    main()
