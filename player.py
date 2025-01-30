import pygame
pygame.init()

class Player:

    rect: pygame.Rect
    camera: dict[str: float]
    movement: dict[str: float] = {"x": 0, "y": 0}
    speed: float = 5
    size: (float, float) = (32, 64)
    window: pygame.Surface

    def __init__(self, window: pygame.Surface, x: float, y: float, camera: dict[str: float]):
        self.window = window
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.camera = camera

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

    def update(self):
        self._set_controls()

        self.rect.x += self.movement["x"]
        self.rect.y += self.movement["y"]
        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(self.rect.x - self.camera["x"], self.rect.y - self.camera["y"], self.rect.width, self.rect.height))
        print(self.camera)
