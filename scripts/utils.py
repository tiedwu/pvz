
import pygame
from scripts.constants import *
from itertools import batched



pygame.font.init()
OBJECT_FONT = pygame.font.SysFont('comicsans', 30)
COST_FONT = pygame.font.SysFont('comicsans', 20)
ASTERISK_FONT = pygame.font.SysFont('comicsans', 60)
SEED_FONT = pygame.font.SysFont('comicsans', 20)
GAMEOVER_FONT = pygame.font.SysFont('comicsans', 100)
COLUMN_FONT = pygame.font.SysFont('comicsans', 10)


def occupied_place(family='plant', occupied={}, pos=(0, 0)):
    if pos in occupied.keys():
        return True
    return False

def get_plants():
    plants = {"PeaShooter": {'id': 0, 'images': make_object_images('plant', 1), 'cost': 100,},
              "SunFlower": {'id': 1, 'images': make_object_images('plant', 2), 'cost': 50},
              "CherryBomb": {'id': 2, 'images': make_object_images('plant', 3), 'cost': 150},
              "Chomper": {'id': 3, 'images': make_object_images('plant', 4), 'cost': 150},
              "HypnoShroom": {'id': 4, 'images': make_object_images('plant', 5), 'cost': 75},
              "IceShroom": {'id': 5, 'images': make_object_images('plant', 6), 'cost': 75},
              "Jalapeno": {'id': 6, 'images': make_object_images('plant', 7), 'cost': 125},
              "PotatoMine": {'id': 7, 'images': make_object_images('plant', 8), 'cost': 25},
              "PuffShroom": {'id': 8, 'images': make_object_images('plant', 9), 'cost': 0},
              "WallNut": {'id': 9, 'images': make_object_images('plant', 10), 'cost': 50},
              "RepeaterPea": {'id': 10, 'images': make_object_images('plant', 11), 'cost': 200},
              "ScaredyShroom": {'id': 11, 'images': make_object_images('plant', 12), 'cost': 25},
              "SnowPea": {'id': 12, 'images': make_object_images('plant', 13), 'cost': 175},
              "Spikeweed": {'id': 13, 'images': make_object_images('plant', 14), 'cost': 100},
              "Squash": {'id': 14, 'images': make_object_images('plant', 15), 'cost': 50},
              "SunShroom": {'id': 15, 'images': make_object_images('plant', 16), 'cost': 25},
              "ThreepeaShooter": {'id': 16, 'images': make_object_images('plant', 17), 'cost': 325},
              "ThornyNut": {'id': 17, 'images': make_object_images('plant', 18), 'cost': 150}}
    
    return plants

def get_zombies():
    zombies = {"Zombie": {'id': 0, 'images': make_object_images('zombie', 1)}, 
               "PeaZombie": {'id': 1, 'images': make_object_images('zombie', 2)},
               "BucketheadZombie": {'id': 2, 'images': make_object_images('zombie', 3)},
               "ConeheadZombie": {'id': 3, 'images': make_object_images('zombie', 4)},
               "FlagZombie": {'id': 4, 'images': make_object_images('zombie', 5)},
               "NewspaperZombie": {'id': 5, 'images': make_object_images('zombie', 6)},
               }
    return zombies

def plants_by_id():
    return order_by_id('plants')

def zombies_by_id():
    return order_by_id('zombies')

def order_by_id(family):
    if family == 'plants':
        f = get_plants
    elif family == 'zombies':
        f = get_zombies
        
    g = lambda x: f()[x]['id']
    keys = f().keys()
    return (sorted([x for x in keys], key=g, reverse=False))
        

def shootable_plants():
    shootable = ['PeaShooter']
    return shootable

def hitable_plants():
    hitable = ['ThornyNut']
    return hitable

def seed_producing_plants():
    return ['SunFlower']

def shootable_zombies():
    shootable = ['PeaZombie']
    return shootable

def hitable_zombies():
    hitable = ['Zombie']
    return hitable

def cards_by_map(map):
    card = []
    if map == 'map0':
        return ['SunFlower', 'PeaShooter', 'ThornyNut']

def seeds_by_map(map):
    if map == 'map0':
        return 100

def draw_grids(display, mode='game', scroll=0):
    #display.fill(GRASS_COLOR)
    display.fill(GROUND_COLOR)

    # horizontal lines
    for i in range(ROAD_ROWS + 1):
        pygame.draw.line(display, LINE_COLOR, (0, i * ROAD_GRID_SIZE), \
                (SCREEN_WIDTH, i * ROAD_GRID_SIZE))

    # mower space
    pygame.draw.line(display, LINE_COLOR, (MOWER_SPACE - scroll, ROAD_GRID_SIZE), \
            (MOWER_SPACE - scroll, SCREEN_HEIGHT))

    if mode == 'game' or mode == 'editor':
        # energy space
        pygame.draw.line(display, LINE_COLOR, (ENERGY_SPACE, 0), (ENERGY_SPACE, ROAD_GRID_SIZE))

        # cards
        for i in range(MAX_CARD_AMOUNT):
            x = ENERGY_SPACE + CARD_WIDTH * (i + 1)
            pygame.draw.line(display, LINE_COLOR, (x, 0), (x, ROAD_GRID_SIZE))

    # road grids
    if mode == 'editor':
        cols = EDITOR_COLS
    else:
        cols = ROAD_COLS

    for i in range(cols):
        x = MOWER_SPACE + ROAD_GRID_SIZE * (i + 1)
        pygame.draw.line(display, LINE_COLOR, (x -scroll, ROAD_GRID_SIZE), (x - scroll, SCREEN_HEIGHT))

    if mode == 'editor':
        # draw column numbers
        for i in range(cols):
            font_img = COLUMN_FONT.render(str(i+1), 1, (0, 0, 0))
            x = MOWER_SPACE + ROAD_GRID_SIZE * i + ROAD_GRID_SIZE  // 2 -\
                    (font_img.get_width()) / 2 - scroll
            y = ROAD_GRID_SIZE
            display.blit(font_img, (x, y))

def draw_selection_zone(display):
    pygame.draw.rect(display, GRASS_COLOR, PLANT_SELECTION_RECT)
    pygame.draw.rect(display, ZOMBIE_SELECTION_BG_COLOR, ZOMBIE_SELECTION_RECT)

def draw_panel(display):
    pygame.draw.rect(display, GROUND_COLOR, (SCREEN_WIDTH + 10, 0, SELECT_ZONE - 10, SCREEN_HEIGHT))

def place_object(display, obj, permulation):
    row, col = permulation
    x = MOWER_SPACE + row * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_width() // 2)
    y = CARD_HEIGHT + col * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_height() // 2)
    display.blit(obj, (x, y))

def make_object_image(name='plant', obj_type=1):
    if name == 'plant':
        color = (0, 255, 255)
    elif name == 'zombie':
        color = ZOMBIE_COLOR 
    obj_width = obj_height = 64
    surface = make_rectangle(color, obj_width, obj_height)
    text = OBJECT_FONT.render(str(obj_type), 1, (255, 255, 255))
    surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            surface.get_height() // 2 - text.get_height() // 2))
    return surface

def make_idle_image(name='plant', obj_type=1):
    if name == 'plant':
        color = (0, 255, 255)
    elif name == 'zombie':
        color = ZOMBIE_COLOR
    obj_width = obj_height = 64
    surface = make_rectangle(color, obj_width, obj_height)
    text = OBJECT_FONT.render(str(obj_type), 1, (255, 255, 255))
    surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            surface.get_height() // 2 - text.get_height() // 2))
    return surface

def make_walk_images(name='plant', obj_type=1):
    images = []
    if name == 'plant':
        color = (0, 255, 255)
    elif name == 'zombie':
        color = ZOMBIE_COLOR
    obj_width = obj_height = 64

    for i in range(4):
        surface = make_rectangle(color, obj_width, obj_height).copy()
        text = OBJECT_FONT.render(str(obj_type), 1, (255, 255, 255))
        surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            surface.get_height() // 2 - text.get_height() // 2))
    
        images.append(make_walk_animation(surface, i))
    
    return images

def make_attack_images(name='plant', obj_type=1):
    images = []
    if name == 'plant':
        color = (0, 255, 255)
    elif name == 'zombie':
        color = ZOMBIE_COLOR
    obj_width = obj_height = 64

    for i in range(3):
        surface = make_rectangle(color, obj_width, obj_height).copy()
        text = OBJECT_FONT.render(str(obj_type), 1, (255, 255, 255))
        surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            surface.get_height() // 2 - text.get_height() // 2))
    
        images.append(make_attack_animation(surface, name, i))
    
    return images

def make_attack_animation(surface, family, index):
    circle = make_circle((255, 0, 0), 10)
    if family == 'zombie':
        x = 0
    elif family == 'plant':
        x = surface.get_width() - circle.get_width()

    y = surface.get_height() // 4 * (index + 1) - circle.get_height() // 2

    surface.blit(circle, (x, y))
    return surface

def make_walk_animation(surface, index):
    if index == 0:
        #surface.blit(circle, (0, surface.get_height() // 2 - circle.get_height() // 2))
        pygame.draw.line(surface, (0, 0, 0), \
            (0, surface.get_height() // 2), (surface.get_width() // 2, 0), 5)
    elif index == 1:
        pygame.draw.line(surface, (0, 0, 0), \
            (surface.get_width() // 2, 0), (surface.get_width(), surface.get_height() // 2), 5)  
    elif index == 2:
        pygame.draw.line(surface, (0, 0, 0), \
            (surface.get_width(), surface.get_height() // 2), \
            (surface.get_width() // 2, surface.get_height()), 5)  
    elif index == 3:
        pygame.draw.line(surface, (0, 0, 0), \
            (0, surface.get_height() // 2), (surface.get_width() // 2, surface.get_height()), 5)  

    return surface
    

def make_object_images(name='plant', obj_type=1):
    images = {}
    images['idle'] = [make_idle_image(name, obj_type)]
    images['walk'] = make_walk_images(name, obj_type)
    images['attack'] = make_attack_images(name, obj_type)
    images['damaged'] = [make_idle_image(name, obj_type)]
    return images

def make_rectangle(color, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(surface, color, rect)
    return surface

def make_bullet_images(radius):
    images = {}
    images['idle'] = [make_circle((255, 0, 0), radius)]
    images['walk'] = [make_circle((255, 0, 0), radius)]
    return images

def make_circle(color, radius):
    surface = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

def make_font(font='seed', value=0):
    if font == 'seed':
        font = SEED_FONT
        color = (9, 153, 214)
    elif font == 'gameover':
        font = GAMEOVER_FONT
        color = (255, 0, 0)
    font_image = font.render(str(value), 1, color)
    return font_image


def make_asterisk(scale):
    ASPECT_WIDTH = 400
    ASPECT_HEIGHT = 400
    STARRY = (230, 255, 80)
    DARK_BLUE = (3, 5, 54)
    CIRCLE_COLOR = (237, 163, 14)
    
    surface = pygame.Surface((ASPECT_WIDTH, ASPECT_HEIGHT), pygame.SRCALPHA, 32)
    pygame.draw.circle(surface, CIRCLE_COLOR, (ASPECT_WIDTH // 2, ASPECT_HEIGHT // 2), \
            ASPECT_WIDTH // 2)
    points = [(165, 151), (200, 20), (235, 151), (371, 144), (257, 219), \
            (306, 346), (200, 260), (94, 346), (143, 219), (29, 144)]
    pygame.draw.polygon(surface, STARRY, points)
    surface = pygame.transform.scale(surface, (scale, scale))
    return surface

def make_mower_object(width, height, number):
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    pygame.draw.rect(surface, (255, 255, 0), (10, 10, width - 20, height - 25))
    pygame.draw.circle(surface, (0, 0, 0), (10 + 10, height - 20), 10)
    pygame.draw.circle(surface, (0, 0, 0), (width - 20, height - 20), 10)
    text = OBJECT_FONT.render(str(number), 1, (0, 0, 255))
    surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            10 + ((height - 25) // 2 - text.get_height() // 2)))
    return surface

def make_mower_images(i):
    images = {}
    images['idle'] = [make_mower_object(64, 64, i)]
    images['walk'] = images['idle']
    return images

def make_card_image(card_type, width, height, name, cost):
    if card_type == 'plants':
        return make_plant_card_image(width, height, name, cost)
    elif card_type == 'zombies':
        return make_zombie_card_image(width, height, name) 


def make_plant_card_image(width, height, name, cost):
    surface = _make_card_image('plants', name, width, height)
    text = COST_FONT.render(str(cost), 1, (0, 0, 0))
    surface.blit(text, (width * 0.8 - text.get_width() + 10, \
            height * 0.8 - text.get_height() + 10))
    
    return surface

def make_zombie_card_image(width, height, name):
    return _make_card_image('zombies', name, width, height)

# cards (plant card and zombie card)
def _make_card_image(family, name, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    if family == 'zombies':
        objs = get_zombies()
    elif family == 'plants':
        objs = get_plants()
    image = objs[name]['images']['idle'][0]
    image = pygame.transform.scale(image, (width * 0.8, height * 0.8))
    surface.blit(image, (10, 10))
    return surface

def over_card(card, pos):
    if card.get_rect().collidepoint(pos):
        return True
    return False

def over_plant_selection(pos):
    if PLANT_SELECTION_RECT.collidepoint(pos):
        return True
    return False

# index begin from 1..N
def get_pos_from_permutation(obj, permutation):
    row, col = permutation
    x = MOWER_SPACE + (col - 1) * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_width() // 2)
    y = CARD_HEIGHT + (row - 1) * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_height() // 2)
    return x, y

def get_permutation_from_pos(pos):
    find_it = False
    rowIndex, colIndex = -1, -1
    for row in range(ROAD_ROWS):
        #for col in range(ROAD_COLS):
        for col in range(EDITOR_COLS):
            rect = pygame.Rect(MOWER_SPACE + col * ROAD_GRID_SIZE, ROAD_GRID_SIZE + row * ROAD_GRID_SIZE \
                               , ROAD_GRID_SIZE, ROAD_GRID_SIZE)
            if rect.collidepoint(pos):
                find_it = True
                break
        if find_it == True:
                break
    if find_it:
        rowIndex = row + 1
        colIndex = col + 1
    
    return find_it, rowIndex, colIndex

def place_zombie_card(exists, obj_name, pos):
    _, row, col = get_permutation_from_pos(pos)
    print(row, col)
    exists[(row, col)] = obj_name
    return exists

def get_card_batches(plants, zombies):
    return get_plant_batches(plants), get_zombie_batches(zombies)


def get_batches(objs, batch_size):
    return batched(objs, batch_size)

def get_plant_batches(objs):
    return get_batches(objs, PLANT_SELECTION_BATCH)

def get_zombie_batches(objs):
    return get_batches(objs, ZOMBIE_SELECTION_BATCH)
