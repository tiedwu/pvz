import pygame
from scripts.constants import SCREEN_WIDTH, SCREEN_HEIGHT

# see grids
from scripts.utils import draw_grids

pygame.init()




class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Plants VS Zombies')

    def loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            draw_grids(self.screen)
            pygame.display.update()

        pygame.quit()

def main():

    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
