#
# Created by Basheer Abdulmalik
#
# Mon, 27-Jan-25
#

import pygame
from maps_manager import MapsManager
from objects.enums.map_type import MapType
from player import Player

pygame.init()

class ArcaneDefender:

    run: bool = True
    fps: float = 60 
    camera: dict[str: float] = {"x": 0, "y": 0}

    screen_size: dict[str: float] = {"width": 500, "height": 500}
    window: pygame.Surface
    player_surface: pygame.Surface
    background_surface: pygame.Surface
    player: Player
    tile_map: list[list[int]]
    
    def __init__(self):
        self.tile_map = MapsManager.load_map(MapType.test)

        # Setting the game window and window components
        self._set_window()
        self._set_player()

    def _set_window(self):
        """
        Configures the game's window settings, like setting up the title and canvas size.
        """

        pygame.display.set_caption("Arcane Defender")
        self.window = pygame.display.set_mode((self.screen_size["width"], self.screen_size["height"]))

        self.player_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        self.background_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)

    def _set_player(self):
        self.player = Player(self.window, 300, 300)

    def _handle_camera_movement(self):
        """
        Camera or offset, is responsible of making the player to always be on the middle of the screen while the map behind moves in the corresponding movement direction.

        * This method takes care of the camera movement.
        * The resulting camera movement will be smooth and not rigid.
        """

        # To achieve a smooth camera movment, the camera's location won't jump immediately to where it suppose to be.
        # location_to_be = (self.player.rect.x - self.screen_size["width"]) / 2
        # Instead the distance to jump will be calculated and the camera's location will move forward by a fraction of that distance on each frame.
        # This will give the movement an elastic effect, because the distance to jump will decrease on every frame until zero.
        self.camera["x"] += ((self.player.rect.center[0] - self.screen_size["width"] / 2) - self.camera["x"]) / 10
        self.camera["y"] += ((self.player.rect.center[1] - self.screen_size["height"] / 2) - self.camera["y"]) / 10

    def activate(self):
        """
        Runs the main game loop and facilitate a safe exit.
        - This is the method to call when you want to start the Game.
        """
        
        clock = pygame.time.Clock()
        
        while self.run:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            self.window.fill((255, 255, 255))
            self.window.blit(self.background_surface, (0, 0))
            self.background_surface.fill((255, 255, 255))
            self.window.blit(self.player_surface, (0, 0))
            self.player_surface.fill((255, 255, 255, 0))

            self._handle_camera_movement()

            visible_tiles_rects = [] # this list will hold the rects of the visible tiles that would be passed to the player for collision detection.
            active_map = MapsManager.get_active_map(self.tile_map, 
                                                    self.player.rect.center, 
                                                    (self.screen_size["width"], self.screen_size["height"]))

            for row_id, row in enumerate(active_map.tiles):
                for tile_id, tile in enumerate(row):
                    if tile > -1:
                        # Since we're looping through the active map, we have to account for its starting point relative to the actual map.
                        # That's why we're adding the starting IDs x the tile size the x/y positions.
                        tile_x_position = active_map.starting_column_index * 32 + tile_id * 32
                        tile_y_position = active_map.starting_row_index * 32 + row_id * 32
                        tile_rect = pygame.Rect(tile_x_position, tile_y_position, 32, 32)
                        visible_tiles_rects.append(tile_rect)

                        pygame.draw.rect(self.background_surface, 
                                         (255, 0, 255), 
                                         pygame.Rect(tile_x_position - self.camera["x"], tile_y_position - self.camera["y"], tile_rect.w, tile_rect.h))

            self.player.update(visible_tiles_rects, self.camera)
            pygame.draw.line(self.player_surface, 
                             (230, 230, 230), 
                             (self.screen_size["width"] / 2, 0), 
                             (self.screen_size["width"] / 2, self.screen_size["height"]))
            pygame.draw.line(self.player_surface, 
                             (230, 230, 230), 
                             (0, self.screen_size["height"] / 2), 
                             (self.screen_size["width"], self.screen_size["height"] / 2))

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main = ArcaneDefender()
    main.activate()
