
import pygame
#import pickle

from scripts.cards import Generator
from scripts.constants import (EDITOR_SCREEN_SIZE, MAP_WIDTH, SCREEN_WIDTH, \
        PLANT_SELECTION_BATCH, MAX_CARD_AMOUNT, SAVE_BUTTON_IMG, LOAD_BUTTON_IMG, \
        LOAD_BUTTON_RECT, SAVE_BUTTON_RECT, MAPS) 
from scripts.utils import draw_grids, draw_panel, draw_selection_zone, place_zombie_card, draw_map_id
from scripts.utils import get_card_batches, over_card, over_plant_selection, over_map_screen
from scripts.button import Button

pygame.display.set_caption('Map Editor')

pygame.init()

class Editor:

    def __init__(self):
        self.screen = pygame.display.set_mode(EDITOR_SCREEN_SIZE)
        self.map_index = 0
        self.load_button = Button(LOAD_BUTTON_RECT.x, LOAD_BUTTON_RECT.y, pygame.image.load(LOAD_BUTTON_IMG).convert_alpha(), 1)
        self.save_button = Button(SAVE_BUTTON_RECT.x, SAVE_BUTTON_RECT.y, pygame.image.load(SAVE_BUTTON_IMG).convert_alpha(), 1)
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
        #plant_cards, zombie_cards = self.card_generator.get_cards()
        plant_cards, zombie_cards = self.card_generator.make_cards_()
        
        plant_shows, zombie_shows = get_card_batches(plant_cards, zombie_cards)
        #plant_shows = get_batches_by_lib(plant_cards, PLANT_SELECTION_BATCH)
        for batch in plant_shows:
            self.plants_to_show.append(batch)

        for batch in zombie_shows:
            self.zombies_to_show.append(batch)


    def place_card_by_order(self, name):
        self.card_generator.make_plant_card_(name)

    def _draw_cards(self):
        for _, card in self.plant_card_info.items():
            if card != None:
                card.draw(self.screen)

        for _, card in self.zombie_card_info.items():
            if card != None:
                card.draw(self.screen, self.scroll)
                
    def update(self):
        if self.scrolls[0] and self.scroll > 0:
            self.scroll -= self.scroll_speed * 5

        if self.scrolls[1] and self.scroll < (MAP_WIDTH - SCREEN_WIDTH):
            self.scroll += self.scroll_speed * 5

        designate_objs = self.card_generator.designate()

        self.plant_card_info = designate_objs['plants']
        self.zombie_card_info = designate_objs['zombies']


    def _draw_map_id(self):
        draw_map_id(self.screen, MAPS[self.map_index]) 


    def draw(self):
        draw_grids(self.screen, mode='editor', scroll=self.scroll)
        draw_panel(self.screen)
        draw_selection_zone(self.screen)
        #draw_zombie_selection_zone(self.screen)
        self._draw_cards()

        self._draw_cards_to_select()

        self._draw_map_id()


        if self.load_button.draw(self.screen):
            self.load()
            
        if self.save_button.draw(self.screen):
            self.save()

    def load(self):
        self.card_generator.load(MAPS[self.map_index])

    def save(self):
        self.card_generator.save(MAPS[self.map_index])

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
            if card != None:
                if over_card(card, pos):
                #del self.plant_card_info[index]
                    self.card_generator.remove_card('plants', index)
                    break

        # zombies
        for permutation, card in self.zombie_card_info.items():
            if over_card(card, (pos[0] + self.scroll, pos[1])):
                #del self.zombie_card_info[permutation]
                self.card_generator.remove_card('zombies', permutation)
                break

    def _select_map(self, selected):
        if selected == 'prev':
            if self.map_index !=  0:
                self.map_index -= 1

        elif selected == 'next':
            if self.map_index == len(MAPS) - 1:
                self.map_index = 0
            else:
                self.map_index += 1
        

        
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
                    self.card_generator.make_zombie_card_(self.zombie_card_selected, (pos[0] + self.scroll, pos[1]))
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
                    if event.key == pygame.K_UP:
                        self._select_map('prev')
                    if event.key == pygame.K_DOWN:
                        self._select_map('next')

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
