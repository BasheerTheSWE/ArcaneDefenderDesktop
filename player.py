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
    jump_force: float = 14
    jump_count: int = 0

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

    def jump(self):
        if self.jump_count < 2:
            self.movement["y"] = -self.jump_force
            self.jump_count += 1

    def _set_gravity(self):
        """
        Sets the applied gravity to the player.

        * Must be called on each frame.
        * The function checks the players vertical movement and increases it if it's less than the maximum gravity.
        """

        if self.movement["y"] < self.max_gravity:
            self.movement["y"] += self.gravity

    def _reset_gravity(self, did_hit_ground: bool=False):
        """
        Resets the applied gravity to the player, or jumpe force back to zero. i.e. resets the player's vertical movement to zero.

        * Must be called when the player hits the ground or their head.
        """

        self.movement["y"] = 0

        if did_hit_ground:
            self.jump_count = 0

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

        for rect in MapsManager.get_hitlist(player_rect=self.rect, tiles_rects=tiles_rects):
            if self.movement["y"] > 0:
                # The player is moving down
                # The player did hit the ground
                self._reset_gravity(did_hit_ground=True)
                self.rect.bottom = rect.top

            if self.movement["y"] < 0:
                # The player is moving up
                # The player did hit his head
                self._reset_gravity()
                self.rect.top = rect.bottom

        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(self.rect.x - camera["x"], 
                                                               self.rect.y - camera["y"], 
                                                               self.rect.width, 
                                                               self.rect.height))
