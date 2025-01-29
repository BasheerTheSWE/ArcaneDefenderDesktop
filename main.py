import pygame

class ArcaneDefender:

    run: bool = True

    screen_size: tuple[int, int]
    window: pygame.Surface
    
    def __init__(self):
        self.screen_size = (500, 500)

        # Setting the game window
        self.setWindow()

    def setWindow(self):
        pygame.display.set_caption("Arcane Defender")
        
        self.window = pygame.display.set_mode(self.screen_size)

    def activate(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

            self.window.fill((255, 255, 0))
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main = ArcaneDefender()
    main.activate()
