
import pygame

from scripts.cards import Generator
from scripts.constants import EDITOR_SCREEN_SIZE, MAP_WIDTH, SCREEN_WIDTH 
from scripts.utils import draw_grids, draw_panel, draw_selection_zone

pygame.display.set_caption('Map Editor')

pygame.init()

class Editor:

    def __init__(self):
        self.screen = pygame.display.set_mode(EDITOR_SCREEN_SIZE)
        self.map = 'map0'
        self.reset()

    def reset(self):
        self.scroll = 0
        self.scrolls = [False, False] # [left, right]
        self.scroll_speed = 1
        self.card_generator = Generator()
        self.card_generator.make_cards(None)

    def update(self):
        if self.scrolls[0] and self.scroll > 0:
            self.scroll -= self.scroll_speed * 5

        if self.scrolls[1] and self.scroll < (MAP_WIDTH - SCREEN_WIDTH):
            self.scroll += self.scroll_speed * 5

    def draw(self):
        draw_grids(self.screen, mode='editor', scroll=self.scroll)
        draw_panel(self.screen)
        draw_selection_zone(self.screen)

    def loop(self):
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scrolls[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.scrolls[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.scrolls[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.scrolls[1] = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    Editor().loop()
