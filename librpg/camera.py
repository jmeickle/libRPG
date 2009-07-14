from config import graphics_config

class CameraMode:
    
    def calc_object_topleft(self, bg_slice_topleft, object_pos, object_x_offset, object_y_offset):
        object_pixel_x = object_pos.x * graphics_config.tile_size - (graphics_config.object_width - graphics_config.tile_size) / 2
        object_pixel_y = object_pos.y * graphics_config.tile_size - (graphics_config.object_height - graphics_config.tile_size)
        x = graphics_config.screen_width / 2 + object_pixel_x - bg_slice_topleft[0] + object_x_offset
        y = graphics_config.screen_height / 2 + object_pixel_y - bg_slice_topleft[1] + object_y_offset
        return (x, y)
        
    # Abstract
    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        raise NotImplementedError, 'CameraMode.calc_bg_slice_topleft() is abstract'
    
#=================================================================================

class PartyConfinementCameraMode(CameraMode):

    """
    
    In this camera mode, the party does not go further than (horizontal_tolerance, vertical_tolerance) from the middle of the screen.
    
    """

    def __init__(self, vertical_tolerance, horizontal_tolerance):
        self.vertical_tolerance = vertical_tolerance
        self.horizontal_tolerance = horizontal_tolerance

    def calc_bg_slice_topleft(self, party_pos, party_x_offset=0, party_y_offset=0):
        if self.vertical_tolerance != 0 or self.horizontal_tolerance != 0:
            raise NotImplementedError, 'PartyConfinementCameraMode not implemented yet.'

        x = party_pos.x * graphics_config.tile_size + party_x_offset
        y = party_pos.y * graphics_config.tile_size + party_y_offset
        return (x, y)
        
#=================================================================================

class PartyCentricCameraMode(PartyConfinementCameraMode):

    """
    
    In this camera mode, the party does not leave the middle of the screen at all.
    
    """
    
    def __init__(self):
        PartyConfinementCameraMode.__init__(self, 0, 0)
    
#=================================================================================

class ScreenConfinementCameraMode(CameraMode):

    """
    
    In this camera mode, the camera will never show the black area beyond the map. It will keep the party at the center of the screen while it is far from the border. When the party approaches the border, the camera will stop to avoid showing the black area.
    
    """
      
    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        pass
