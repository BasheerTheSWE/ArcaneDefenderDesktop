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
    window: pygame.Surface

    size: (float, float) = (32, 64)
    movement: dict[str: float] = {"x": 0, "y": 0}
    speed: float = 5
    gravity: float = 0.5
    max_gravity: float = 9

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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.movement["x"] = -self.speed

        if keys[pygame.K_RIGHT]:
            self.movement["x"] = self.speed

    def _set_gravity(self):
        if self.movement["y"] < self.max_gravity:
            self.movement["y"] += self.gravity

    def _reset_gravity(self):
        self.movement["y"] = 0

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

        # Applying gravity
        self._set_gravity()
        self.rect.y += self.movement["y"]
        print(self.movement["y"])

        for rect in MapsManager.get_hitlist(player_rect=self.rect, tiles_rects=tiles_rects):
            if self.movement["y"] > 0:
                # The player is moving down
                # The player did hit the ground
                self._reset_gravity()
                self.rect.bottom = rect.top

            if self.movement["y"] < 0:
                # The player is moving up
                self.rect.top = rect.bottom

        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(self.rect.x - camera["x"], 
                                                               self.rect.y - camera["y"], 
                                                               self.rect.width, 
                                                               self.rect.height))
