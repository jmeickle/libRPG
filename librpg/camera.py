
class CameraMode:
    
    # Abstract
    def calc_party_topleft(self):
        pass
    
    # Abstract
    def calc_bg_topleft(self):
        pass
    
#=================================================================================

class PartyConfinementCameraMode(CameraMode):

    """
    
    In this camera mode, the party does not go further than (horizontal_tolerance, vertical_tolerance) from the middle of the screen.
    
    """

    def __init__(self, vertical_tolerance, horizontal_tolerance):
        pass

    def calc_party_topleft(self):
        pass
        
    def calc_bg_topleft(self):
        pass

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
    
    def calc_party_topleft(self):
        pass
        
    def calc_bg_topleft(self):
        pass
