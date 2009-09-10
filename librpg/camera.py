"""
The :mod:`camera` module defines a couple of ways to follow the party
avatar around the map. Each of these ways is represented by a class, and
changing the camera mode is done by the config.graphics_config object.

This module also defines a CameraMode abstract class that can be used to
write custom camera modes.
"""

from librpg.config import graphics_config


class CameraMode(object):

    """
    Base abstract class for creating new camera modes.
    """

    def attach_to_map(self, map_model):
        """
        *Virtual.*
        
        Callback called when a map is initialized to be used with the
        camera. Typically, map-specific initialization is be done here.
        
        *map_model* is a handle to the MapModel, so that information such
        as the map size can be retrieved.
        """
        pass

    def calc_object_topleft(self, bg_slice_topleft, object_pos, object_width,
                            object_height, object_x_offset, object_y_offset):
        object_pixel_x = (object_pos.x * graphics_config.tile_size -
                          (object_width - graphics_config.tile_size) / 2)
        object_pixel_y = (object_pos.y * graphics_config.tile_size -
                          (object_height - graphics_config.tile_size))

        x = (graphics_config.map_border_width + object_pixel_x -
             bg_slice_topleft[0] + object_x_offset)
        y = (graphics_config.map_border_height + object_pixel_y -
             bg_slice_topleft[1] + object_y_offset)
        return (x, y)

    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        """
        *Abstract.*
        
        Return the position to which the top left corner of the screen
        should be aligned in the background.
        
        The background is the map plus black borders in every side, as
        thick as half the screen size in that direction. For example, a
        screen with width=640 and height=480 has 320 black lines in each
        side and 240 black lines up and down.
        
        Given the *party_pos* (position of the party in tiles),
        *party_x_offset* and *party_y_offset* (offset in pixels to apply to
        *party_pos* due to animation), this function should return an
        (x, y) tuple representing where the top left of the camera should
        aim for in the background.
        """
        raise NotImplementedError, \
              'CameraMode.calc_bg_slice_topleft() is abstract'


class PartyConfinementCameraMode(CameraMode):
    """
    Flexible centered camera mode.

    In this camera mode, the party does not go further than
    (*horizontal_tolerance*, *vertical_tolerance*) from the middle of
    the screen.

    This will decrease the frequency of scrolling, especially when the
    party is switching directions frequently.
    """

    def __init__(self, vertical_tolerance, horizontal_tolerance):
        self.vertical_tolerance = vertical_tolerance
        self.horizontal_tolerance = horizontal_tolerance
        self.current_place = None

    def _normalize(self, current, proj, tolerance):
        new_value = current
        if abs(proj - current) > tolerance:
            if proj > current:
                new_value = proj - tolerance
            else:
                new_value = proj + tolerance
        return new_value

    def attach_to_map(self, map_model):
        self.current_place = None

    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        proj_x = (party_pos.x * graphics_config.tile_size +
                  graphics_config.tile_size / 2 + party_x_offset)
        proj_y = (party_pos.y * graphics_config.tile_size +
                  graphics_config.tile_size / 2 + party_y_offset)

        if self.current_place is not None:
            old_x, old_y = (self.current_place[0], self.current_place[1])

            new_x = self._normalize(old_x, proj_x, self.horizontal_tolerance)
            new_y = self._normalize(old_y, proj_y, self.vertical_tolerance)
        else:
            new_x, new_y = proj_x, proj_y

        self.current_place = (new_x, new_y)
        return self.current_place


class PartyCentricCameraMode(CameraMode):
    """
    Centered camera mode.

    In this camera mode, the party does not leave the middle of the
    screen at all. Therefore, whenever the party would move, it is
    actually the background that moves.
    """

    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        x = (party_pos.x * graphics_config.tile_size +
             graphics_config.tile_size / 2 + party_x_offset)
        y = (party_pos.y * graphics_config.tile_size +
             graphics_config.tile_size / 2 + party_y_offset)
        return (x, y)


class ScreenConfinementCameraMode(CameraMode):
    """
    No black area camera.

    In this camera mode, the camera will never show the black area
    beyond the map. It will keep the party at the center of the screen
    while it is far from the border. When the party approaches the
    border, the camera will stop to avoid showing the black area.
    """

    def attach_to_map(self, map_model):
        self.map_width_in_pixels = graphics_config.tile_size * map_model.width
        self.map_height_in_pixels = graphics_config.tile_size * map_model.height
        self.x_max = self.map_width_in_pixels - graphics_config.map_border_width
        self.y_max = self.map_height_in_pixels - graphics_config.map_border_height

    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        x = (party_pos.x * graphics_config.tile_size +
             graphics_config.tile_size / 2 + party_x_offset)
        y = (party_pos.y * graphics_config.tile_size +
             graphics_config.tile_size / 2 + party_y_offset)

        if self.map_width_in_pixels <= graphics_config.screen_width:
            x = self.map_width_in_pixels / 2
        elif x < graphics_config.map_border_width:
            x = graphics_config.map_border_width
        elif x > self.x_max:
            x = self.x_max

        if self.map_height_in_pixels <= graphics_config.screen_height:
            y = self.map_height_in_pixels / 2
        elif y < graphics_config.map_border_height:
            y = graphics_config.map_border_height
        elif y > self.y_max:
            y = self.y_max

        return (x, y)


class FixedCameraMode(CameraMode):
    """
    Still camera mode.

    The camera will not move in this mode, but stay fixed, at the
    given (*x*, *y*) position. *x* and *y* are in tiles, from the top left
    corner of the map.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc_bg_slice_topleft(self, party_pos, party_x_offset, party_y_offset):
        return (graphics_config.map_border_width -
                self.x, graphics_config.map_border_height - self.y)

