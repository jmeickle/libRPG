from config import graphics_config

class CameraMode:
    
    # Virtual
    def attach_to_map(self):
        pass
    
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
        self.current_place = None

    def attach_to_map(self):
        self.current_place = None
    
    def calc_bg_slice_topleft(self, party_pos, party_x_offset=0, party_y_offset=0):
        #if self.vertical_tolerance != 0 or self.horizontal_tolerance != 0:
        #    raise NotImplementedError, 'PartyConfinementCameraMode not implemented yet.'
        
        proj_x = party_pos.x * graphics_config.tile_size + graphics_config.tile_size / 2 + party_x_offset
        proj_y = party_pos.y * graphics_config.tile_size + graphics_config.tile_size / 2 + party_y_offset
        
        if self.current_place is not None:
            old_x, old_y = self.current_place[0], self.current_place[1]
            
            if abs(proj_x - old_x) > self.horizontal_tolerance:
                if proj_x > old_x:
                    new_x = proj_x - self.horizontal_tolerance
                else:
                    new_x = proj_x + self.horizontal_tolerance
            else:
                new_x = old_x
                
            if abs(proj_y - old_y) > self.vertical_tolerance:
                if proj_y > old_y:
                    new_y = proj_y - self.vertical_tolerance
                else:
                    new_y = proj_y + self.vertical_tolerance
            else:
                new_y = old_y
        else:
            new_x, new_y = proj_x, proj_y
            
        self.current_place = (new_x, new_y)
        return self.current_place
        
#=================================================================================

class PartyCentricCameraMode(CameraMode):

    """
    
    In this camera mode, the party does not leave the middle of the screen at all.
    
    """
    
    def calc_bg_slice_topleft(self, party_pos, party_x_offset=0, party_y_offset=0):
        
        x = party_pos.x * graphics_config.tile_size + graphics_config.tile_size / 2 + party_x_offset
        y = party_pos.y * graphics_config.tile_size + graphics_config.tile_size / 2 + party_y_offset
        return (x, y)
    
#=================================================================================

class ScreenConfinementCameraMode(CameraMode):

    """
    
    In this camera mode, the camera will never show the black area beyond the map. It will keep the party at the center of the screen while it is far from the border. When the party approaches the border, the camera will stop to avoid showing the black area.
    
    """
      
    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        pass

#=================================================================================

class FixedCameraMode(CameraMode):

    """
    
    
    
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        return graphics_config.screen_width / 2 + self.x * graphics_config.tile_size, graphics_config.screen_height / 2 + self.y * graphics_config.tile_size
