import librpg

from map import *
from config import *
from tile import *

class MapView:

    """
    map_model: MapModel (read-only)
    MapModel with the information to be drawn.

    screen: Surface (read-only)
    Screen surface to blit to.

    background: Surface (private)
    Surface containing the static terrain and scenario layers that are drawn at the lower level.

    foreground: Surface (private)
    Surface containing the static scenario tiles that are drawn at the upper level.
    """
    
    def __init__(self, map_model):
        self.map_model = map_model
        
        self.screen = librpg.screen
        self.init_background()
        self.init_foreground()
    
    def init_background(self):
        background_width = graphics_config.tile_size * self.map_model.width + graphics_config.screen_width
        background_height = graphics_config.tile_size * self.map_model.height + graphics_config.screen_height
        self.background = pygame.Surface((background_width, background_height))
        
        BLACK = (0, 0, 0)
        self.background.fill(BLACK)
        
        for y in xrange(self.map_model.height):
            for x in xrange(self.map_model.width):
                bg_x = graphics_config.screen_width / 2 + x * graphics_config.tile_size
                bg_y = graphics_config.screen_height / 2 + y * graphics_config.tile_size
                terrain_tile_surface = self.map_model.terrain_layer.get(x, y).get_surface()
                self.background.blit(terrain_tile_surface, (bg_x, bg_y))
                
                scenario_tile = self.map_model.scenario_layer.get(x, y)
                if scenario_tile.obstacle != Tile.ABOVE:
                    scenario_tile_surface = scenario_tile.get_surface()
                    self.background.blit(scenario_tile_surface, (bg_x, bg_y))

    def init_foreground(self):
        foreground_width = graphics_config.tile_size * self.map_model.width + graphics_config.screen_width
        foreground_height = graphics_config.tile_size * self.map_model.height + graphics_config.screen_height
        self.foreground = pygame.Surface((foreground_width, foreground_height), SRCALPHA, 32)
        
        for y in xrange(self.map_model.height):
            for x in xrange(self.map_model.width):
                scenario_tile = self.map_model.scenario_layer.get(x, y)
                if scenario_tile.obstacle == Tile.ABOVE:
                    fg_x = graphics_config.screen_width / 2 + x * graphics_config.tile_size
                    fg_y = graphics_config.screen_height / 2 + y * graphics_config.tile_size
                    scenario_tile_surface = scenario_tile.get_surface()
                    self.foreground.blit(scenario_tile_surface, (fg_x, fg_y))

    def draw(self):
        party_avatar = self.map_model.party_avatar
    
        # Draw the background
        x_offset, y_offset = 0, 0
        if party_avatar:
            party_pos = party_avatar.position
            if party_avatar.movement_phase > 0:
                offset = party_avatar.movement_phase * graphics_config.tile_size / party_avatar.speed
                if party_avatar.facing == Direction.UP:
                    y_offset = offset
                elif party_avatar.facing == Direction.RIGHT:
                    x_offset = -offset
                elif party_avatar.facing == Direction.DOWN:
                    y_offset = -offset
                elif party_avatar.facing == Direction.LEFT:
                    x_offset = offset
        else:
            party_pos = Position(0, 0)
            
        bg_area = pygame.Rect((party_pos.x * graphics_config.tile_size + x_offset, party_pos.y * graphics_config.tile_size + y_offset), (graphics_config.screen_width, graphics_config.screen_height))
        self.screen.blit(self.background, (0, 0), bg_area)
        
        # Draw the party avatar
        if party_avatar:
            party_place = (graphics_config.screen_width - graphics_config.object_width + graphics_config.tile_size) / 2, (graphics_config.screen_height / 2 - graphics_config.object_height + graphics_config.tile_size)
            self.screen.blit(party_avatar.get_surface(), pygame.Rect(party_place, (graphics_config.object_width, graphics_config.object_height)))
        
        # Draw the foreground
        self.screen.blit(self.foreground, (0, 0), bg_area)
        
        # Flip display
        pygame.display.flip()

