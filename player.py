#
# Created by Basheer Abdulmalik
#
# Mon, 27-Jan-25
#

import pygame
from maps_manager import MapsManager
pygame.init()

class Player:

    rect: pygame.Rect
    movement: dict[str: float] = {"x": 0, "y": 0}
    speed: float = 5
    size: (float, float) = (32, 64)
    window: pygame.Surface

    def __init__(self, window: pygame.Surface, x: float, y: float):
        self.window = window
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])

    def _set_controls(self):
        """
        Handles keyboard inputs
        """

        # Resetting the movement to zero
        # When the user releases the arrow button the x-movement will be zero and the player would stop
        self.movement["x"] = 0
        self.movement["y"] = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.movement["x"] = -self.speed

        if keys[pygame.K_RIGHT]:
            self.movement["x"] = self.speed

        if keys[pygame.K_UP]:
            self.movement["y"] = -self.speed
        
        if keys[pygame.K_DOWN]:
            self.movement["y"] = self.speed

    def update(self, tiles_rects: list[pygame.Rect], camera: dict[str: float]):
        self._set_controls()

        self.rect.x += self.movement["x"]

        for rect in MapsManager.get_hitlist(player_rect=self.rect, tiles_rects=tiles_rects):
            if self.movement["x"] > 0:
                # The player is moving right
                self.rect.right = rect.left

            if self.movement["x"] < 0:
                # The player is moving up
                self.rect.left = rect.right

        self.rect.y += self.movement["y"]

        for rect in MapsManager.get_hitlist(player_rect=self.rect, tiles_rects=tiles_rects):
            if self.movement["y"] > 0:
                # The player is moving down
                self.rect.bottom = rect.top

            if self.movement["y"] < 0:
                # The player is moving up
                self.rect.top = rect.bottom

        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(self.rect.x - camera["x"], 
                                                               self.rect.y - camera["y"], 
                                                               self.rect.width, 
                                                               self.rect.height))
