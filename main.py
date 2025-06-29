import pygame
from scripts.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scripts.spawner import Spawner

# see grids
from scripts.utils import draw_grids

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Plants VS Zombies')
        self.zombies = Spawner('zombie')
        self.plants = Spawner('plant')

    def update(self):
        self.zombies.group.update()
        self.plants.group.update()

    def draw(self):
        draw_grids(self.screen)

        self.zombies.group.draw(self.screen)
        self.plants.group.draw(self.screen)
        for plant in self.plants.group:
            plant.draw(self.screen)


    def loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.zombies.generate()

                    if event.key == pygame.K_p:
                        self.plants.generate()

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()

def main():

    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
