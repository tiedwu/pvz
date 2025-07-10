import pygame
import random

from scripts.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, NUMBER_OF_MOWERS, \
        ENERGY_SPACE, SEED_PACKET_WIDTH, SEED_PACKET_HEIGHT, ROAD_GRID_SIZE)
from scripts.spawner import Spawner
from scripts.mowers import Mower
from scripts.cards import Generator
from scripts.seeds import SeedPacket

# see grids
from scripts.utils import draw_grids, make_font

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Plants VS Zombies')
        self.seedpacket = SeedPacket((ENERGY_SPACE // 2 - SEED_PACKET_WIDTH // 2, \
                ROAD_GRID_SIZE // 2 - SEED_PACKET_HEIGHT // 2))
        self._reset('map0')

    def _reset(self, map):
        self.gameover = False
        self.map = map
        self.zombies = Spawner('zombie')
        self.plants = Spawner('plant')
        self.mowers = self._create_mowers()
        self.card_generator = Generator()
        # self.cards = []
        self.plant_taken = None
        self.cards = self._make_cards()
        
    def _make_cards(self):
        return self.card_generator.make_cards(self.map)

    def _create_mowers(self):
        mowers = []
        
        for i in range(NUMBER_OF_MOWERS):
            mowers.append(Mower(None, i))
        return mowers

    def generate_card(self):
        
        card = self.card_generator._get_card()
        if card != None:
            self.cards.append(card)

    def _check_live(self):
        for plant in self.plants.group:
            if plant.hp == 0:
                self.plants.group.remove(plant)

        for zombie in self.zombies.group:
            if zombie.hp == 0:
                self.zombies.group.remove(zombie)

    def handle_collision(self):
        for plant in self.plants.group:
            plant.shoot(self.zombies.group)
            plant.hit(self.zombies.group)

        for zombie in self.zombies.group:
            zombie.shoot(self.plants.group)
            zombie.hit(self.plants.group)

        self._check_live()

    def update(self):
        self.handle_collision()

        self.zombies.group.update()
        self.plants.group.update()


        for mower in self.mowers:
            mower.collided(self.zombies.group)
            if not mower.in_screen():
                self.mowers.remove(mower)
            mower.update()

        if self.check_gameover():
            self.gameover = True

            # all thing stop moving
            self.stop_objs()

    def stop_objs(self):
        for zombie in self.zombies.group:
            zombie.stop()

        for plant in self.plants.group:
            plant.stop()

    def check_gameover(self):
        gameover = False
        for zombie in self.zombies.group:
            if zombie.inner_home():
                gameover = True
                break
        return gameover

            
    def draw(self):
        draw_grids(self.screen)

        self.seedpacket.draw(self.screen)

        for card in self.cards:
            card.draw(self.screen)

        self.zombies.group.draw(self.screen)
        self.plants.group.draw(self.screen)
        for plant in self.plants.group:
            plant.draw(self.screen)
        for zombie in self.zombies.group:
            zombie.draw(self.screen)

        for mower in self.mowers:
            mower.draw(self.screen)

        if self.gameover:
            self.draw_gameover()

    def draw_gameover(self):
        font_image = make_font('gameover', 'Gameover !!!')
        self.screen.blit(font_image, (SCREEN_WIDTH // 2 - font_image.get_width() // 2, \
                SCREEN_HEIGHT // 2 - font_image.get_height() // 2))

    def handle_choice(self):
        pos = pygame.mouse.get_pos()
        if not self.plant_taken:
            for card in self.cards:
                if card.get_rect().collidepoint(pos):
                    self.plant_taken = card.name
                    break
        else:
            self.plants.make_plant(self.plant_taken, pos)
            self.plant_taken = None

    def loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 1:
                        self.handle_choice()

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
                        # self.generate_card()
                        pass

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

def main():

    game = Game()
    game.loop()


if __name__ == '__main__':
    main()
