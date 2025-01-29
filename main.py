import pygame
from player import Player

pygame.init()

class ArcaneDefender:

    run: bool = True
    fps: float = 60 

    screen_size: tuple[int, int]
    window: pygame.Surface
    player: Player
    
    def __init__(self):
        self.screen_size = (500, 500)

        # Setting the game window and window components
        self._set_window()
        self._set_player()

    def _set_window(self):
        """
        Configures the game's window settings, like setting up the title and canvas size.
        """

        pygame.display.set_caption("Arcane Defender")
        self.window = pygame.display.set_mode(self.screen_size)

    def _set_player(self):
        self.player = Player(self.window, 100, 100)
        pass

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

            self.window.fill((255, 255, 255))
            self.player.update()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main = ArcaneDefender()
    main.activate()
