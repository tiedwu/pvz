import pygame
from scripts.constants import SCREEN_WIDTH, SCREEN_HEIGHT

# see grids
from scripts.utils import draw_grids, make_object

pygame.init()


def draw(display, obj):
    draw_grids(display)
    
    display.blit(obj, (200, 300))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Plants VS Zombies')

    def loop(self):
        run = True
        obj = make_object()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            draw(self.screen, obj)
            pygame.display.update()

        pygame.quit()

def main():

    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
