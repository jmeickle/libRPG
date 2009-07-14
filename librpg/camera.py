from config import graphics_config

class CameraMode:
    
    # Abstract
    def calc_object_topleft(self, object_pos):
        raise NotImplementedError, 'CameraMode.calc_object_topleft() is abstract'
    
    # Abstract
    def calc_bg_slice_topleft(self, party_pos, x_offset, y_offset):
        raise NotImplementedError, 'CameraMode.calc_bg_slice_topleft() is abstract'
    
#=================================================================================

class PartyConfinementCameraMode(CameraMode):

    """
    
    In this camera mode, the party does not go further than (horizontal_tolerance, vertical_tolerance) from the middle of the screen.
    
    """

    def __init__(self, vertical_tolerance, horizontal_tolerance):
        self.vertical_tolerance = vertical_tolerance
        self.horizontal_tolerance = horizontal_tolerance

    def calc_object_topleft(self, object_pos):
        if self.vertical_tolerance != 0 or self.horizontal_tolerance != 0:
            raise NotImplementedError, 'PartyConfinementCameraMode not implemented yet.'
        result = (graphics_config.screen_width - graphics_config.object_width + graphics_config.tile_size) / 2, (graphics_config.screen_height / 2 - graphics_config.object_height + graphics_config.tile_size)
        return result
        
    def calc_bg_slice_topleft(self, party_pos, x_offset, y_offset):
        if self.vertical_tolerance != 0 or self.horizontal_tolerance != 0:
            raise NotImplementedError, 'PartyConfinementCameraMode not implemented yet.'

        result = (party_pos.x * graphics_config.tile_size + x_offset, party_pos.y * graphics_config.tile_size + y_offset)
        
        return result
        
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
    
    def calc_object_topleft(self, object_pos):
        pass
        
    def calc_bg_slice_topleft(self, party_pos, x_offset, y_offset):
        pass
