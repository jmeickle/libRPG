:mod:`config` -- Components configuration
=========================================

.. automodule:: librpg.config
   :members:
   :show-inheritance:

Usage
-----

To change the default global configurations, either set members of the
global configuration objects individually or use their config() method
passing the attributes to be changed as keyword arguments.

The default values are:

**graphics_config**

    :attr:`camera_mode` - PartyCentricCameraMode()

    :attr:`display_mode` - 0
    
    :attr:`screen_width` - 400
    
    :attr:`screen_height` - 300
    
    :attr:`object_width` - 24
    
    :attr:`object_height` - 32
    
    :attr:`tile_size` - 16
    
    :attr:`scale` - 2

    :attr:`animation_frame_period` - 15

**dialog_config**

    :attr:`font_name` - 'Verdana'
    
    :attr:`font_size` - 12
    
    :attr:`border_width` - 15 
    
    :attr:`line_spacing` - 2
    
    :attr:`choice_line_spacing` - 2
    
    :attr:`bg_color` - (128, 0, 128, 128)
    
    :attr:`font_color` - (255, 255, 255)
    
    :attr:`selected_font_color` - (255, 0, 0)
    
    :attr:`not_selected_font_color` - (128, 128, 128)
    
**game_config**

    :attr:`fps` - 30

    :attr:`key_up` - set([K_UP])
    
    :attr:`key_down` - set([K_DOWN])
    
    :attr:`key_left` - set([K_LEFT]) 
    
    :attr:`key_right` - set([K_RIGHT])
    
    :attr:`key_action` - set([K_RETURN, K_SPACE])
    
    :attr:`key_cancel` - set([K_ESCAPE])
    
Examples
--------

::

    librpg.config.graphics_config.config(screen_width=200,
                                         screen_height=200,
                                         scale=2.5)

::

    librpg.config.dialog_config.config(bg_color=(0, 0, 255))
    librpg.config.dialog_config.config(font_color=(90, 90, 90, 180))

::

    librpg.config.dialog_config.line_spacing = 4
    librpg.config.dialog_config.font_size = 14

::

    librpg.config.graphics_config.config(tile_size=32,
                                         object_height=32,
                                         object_width=32)

::

    librpg.config.game_config.config(fps=24,
                                     key_up=set([K_w]),
                                     key_left=set([K_a]),
                                     key_down=set([K_s]),
                                     key_right=set([K_d]),
                                     key_action=set([K_e]),
                                     key_cancel=set([K_q]))

::

    mode = int(sys.argv[1])
    if mode == 1:
        pass
    elif mode == 2:
        librpg.config.graphics_config.config(camera_mode=librpg.camera.FixedCameraMode(50, 50),
                                             screen_width=480,
                                             screen_height=480,
                                             scale=1)
    elif mode == 3:
        librpg.config.graphics_config.config(camera_mode=librpg.camera.PartyConfinementCameraMode(50, 40),
                                             screen_width=450,
                                             screen_height=400)
    elif mode == 4:
        librpg.config.graphics_config.config(camera_mode=librpg.camera.ScreenConfinementCameraMode(),
                                             screen_width=200,
                                             screen_height=200,
                                             scale=3)
    elif mode == 5:
        librpg.config.graphics_config.config(camera_mode=librpg.camera.ScreenConfinementCameraMode(),
                                             screen_width=400,
                                             screen_height=400)
    else:
        print 'Pass a number from 1 to 5 for the screen and camera mode.'
        exit()
