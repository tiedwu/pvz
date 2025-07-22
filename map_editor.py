
import pygame

from scripts.cards import Generator
from scripts.constants import (EDITOR_SCREEN_SIZE, MAP_WIDTH, SCREEN_WIDTH, \
        PLANT_SELECTION_BATCH, MAX_CARD_AMOUNT) 
from scripts.utils import draw_grids, draw_panel, draw_selection_zone, place_zombie_card
from scripts.utils import get_card_batches, over_card, over_plant_selection, over_map_screen

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
        self.zombies_batch = 0
        self.plants_batch = 0
        self.plants_to_show = []
        self.zombies_to_show = []
        #self.card_box = [0] * MAX_CARD_AMOUNT
        self.card_generator = Generator()
        #self.plant_card_box = self.card_generator.occupied
        #self.plant_cards = []

        # [['PeaZombie', (2, 2)], []]
        #self.zombie_cards = []
        self.zombie_card_info = {}
        self.plant_card_info = {}
        self.zombie_card_selected = None
        self._show_cards()

    def _show_cards(self):
        plant_cards, zombie_cards = self.card_generator.get_cards()
        
        plant_shows, zombie_shows = get_card_batches(plant_cards, zombie_cards)
        #plant_shows = get_batches_by_lib(plant_cards, PLANT_SELECTION_BATCH)
        for batch in plant_shows:
            self.plants_to_show.append(batch)

        for batch in zombie_shows:
            self.zombies_to_show.append(batch)


    def place_card_by_order(self, name):
        index, card = self.card_generator.get_card_in_box(name)
        if card != None and index != -1:
            self.plant_card_info[index] = card

    def _draw_cards(self):
        for _, card in self.plant_card_info.items():
            card.draw(self.screen)

        for card in self.zombie_card_info.values():
            card.draw(self.screen, self.scroll)
                
    def update(self):
        if self.scrolls[0] and self.scroll > 0:
            self.scroll -= self.scroll_speed * 5

        if self.scrolls[1] and self.scroll < (MAP_WIDTH - SCREEN_WIDTH):
            self.scroll += self.scroll_speed * 5

    def draw(self):
        draw_grids(self.screen, mode='editor', scroll=self.scroll)
        draw_panel(self.screen)
        draw_selection_zone(self.screen)
        #draw_zombie_selection_zone(self.screen)
        self._draw_cards()

        self._draw_cards_to_select()

    def _draw_cards_to_select(self):
        for card in self.plants_to_show[self.plants_batch]:
            card.draw(self.screen)

        for card in self.zombies_to_show[self.zombies_batch]:
            card.draw(self.screen)

    def _select_card_on_zone(self, pos):
        cards = self.plants_to_show[self.plants_batch]
        selected = None
        for card in cards:
            if over_card(card, pos):
                selected = card
                break
        if not selected:
            cards = self.zombies_to_show[self.zombies_batch]
            for card in cards:
                if over_card(card, pos):
                    selected = card
                    break
        return selected

    def _remove_card_on_map(self, pos):
        
        # plants
        for index, card in self.plant_card_info.items():
            if over_card(card, pos):
                del self.plant_card_info[index]
                self.card_generator.remove_card(index)
                break

        # zombies
        for permutation, card in self.zombie_card_info.items():
            if over_card(card, (pos[0] + self.scroll, pos[1])):
                del self.zombie_card_info[permutation]
                break



        
    def handle_mousebutton(self, left, right):
        pos = pygame.mouse.get_pos()
        if left:
            if not self.zombie_card_selected:
                selected = self._select_card_on_zone(pos)
                if selected != None:
                    if selected.family == 'zombies':
                        self.zombie_card_selected = selected.name
            else:
                if over_map_screen(pos):
                    permutation, card = self.card_generator.make_zombie_card(self.zombie_card_selected, (pos[0] + self.scroll, pos[1]))
                    self.zombie_card_info[permutation] = card
                    self.zombie_card_selected = None
            
            # plant_card
            selected = self._select_card_on_zone(pos)
            if selected != None:
                if selected.family == 'plants':
                    self.place_card_by_order(selected.name)    
                

        elif right:
            self._remove_card_on_map(pos)



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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mousebutton(True, False)

                    if event.button == 3:
                        self.handle_mousebutton(False, True)

                    if event.button == 4:
                        if self.plants_batch >= 1 and over_plant_selection(pygame.mouse.get_pos()):
                            self.plants_batch -= 1
                    if event.button == 5:
                        if self.plants_batch < len(self.plants_to_show) - 1 and \
                                over_plant_selection(pygame.mouse.get_pos()):
                            self.plants_batch += 1

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    Editor().loop()
