import pygame
from scripts.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, NUMBER_OF_MOWERS
from scripts.spawner import Spawner
from scripts.mowers import Mower
from scripts.cards import Generator

# see grids
from scripts.utils import draw_grids

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Plants VS Zombies')
        self.zombies = Spawner('zombie')
        self.plants = Spawner('plant')
        self.mowers = self._create_mowers()
        self.card_generator = Generator()
        self.cards = []

    def _create_mowers(self):
        mowers = []
        pass
        for i in range(NUMBER_OF_MOWERS):
            mowers.append(Mower(None, i))
        return mowers

    def generate_card(self):
        print(self.card_generator.get_occupies())
        card = self.card_generator.get_card()
        if card != None:
            self.cards.append(card)

    def update(self):
        self.zombies.group.update()
        self.plants.group.update()

        for mower in self.mowers:
            mower.update()
            

    def draw(self):
        draw_grids(self.screen)

        for mower in self.mowers:
            mower.draw(self.screen)

        for card in self.cards:
            card.draw(self.screen)

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

                    if event.key ==pygame.K_1:
                        self.mowers[0].attack()
                    if event.key ==pygame.K_2:
                        self.mowers[1].attack()
                    if event.key ==pygame.K_3:
                        self.mowers[2].attack()
                    if event.key ==pygame.K_4:
                        self.mowers[3].attack()
                    if event.key ==pygame.K_5:
                        self.mowers[4].attack()
                    if event.key ==pygame.K_6:
                        self.mowers[5].attack()
                    
                    if event.key == pygame.K_c:
                        self.generate_card()

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()

def main():

    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
