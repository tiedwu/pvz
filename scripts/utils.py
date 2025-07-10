
import pygame
from scripts.constants import *



pygame.font.init()
OBJECT_FONT = pygame.font.SysFont('comicsans', 30)
COST_FONT = pygame.font.SysFont('comicsans', 10)
ASTERISK_FONT = pygame.font.SysFont('comicsans', 60)
SEED_FONT = pygame.font.SysFont('comicsans', 20)
GAMEOVER_FONT = pygame.font.SysFont('comicsans', 100)

def get_plants():
    plants = {"PeaShooter": {'images': make_object_images('plant', 1), 'cost': 100,},
              "SunFlower": {'images': make_object_images('plant', 2), 'cost': 50},
              "ThornyNut": {'images': make_object_images('plant', 3), 'cost': 150}}
    return plants

def shootable_plants():
    shootable = ['PeaShooter']
    return shootable

def hitable_plants():
    hitable = ['ThornyNut']
    return hitable

def shootable_zombies():
    shootable = ['Zombie_2']
    return shootable

def hitable_zombies():
    hitable = ['Zombie_1']
    return hitable

def cards_by_map(map):
    card = []
    if map == 'map0':
        return ['SunFlower', 'PeaShooter', 'ThornyNut']

def draw_grids(display):
    #display.fill(GRASS_COLOR)
    display.fill(GROUND_COLOR)

    # horizontal lines
    for i in range(ROAD_ROWS + 1):
        pygame.draw.line(display, LINE_COLOR, (0, i * ROAD_GRID_SIZE), \
                (SCREEN_WIDTH, i * ROAD_GRID_SIZE))

    # mower space
    pygame.draw.line(display, LINE_COLOR, (MOWER_SPACE, ROAD_GRID_SIZE), (MOWER_SPACE, SCREEN_HEIGHT))

    # energy space
    pygame.draw.line(display, LINE_COLOR, (ENERGY_SPACE, 0), (ENERGY_SPACE, ROAD_GRID_SIZE))

    # cards
    for i in range(MAX_CARD_AMOUNT):
        x = ENERGY_SPACE + CARD_WIDTH * (i + 1)
        pygame.draw.line(display, LINE_COLOR, (x, 0), (x, ROAD_GRID_SIZE))

    # road grids
    for i in range(ROAD_COLS):
        x = MOWER_SPACE + ROAD_GRID_SIZE * (i + 1)
        pygame.draw.line(display, LINE_COLOR, (x, ROAD_GRID_SIZE), (x, SCREEN_HEIGHT))

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

def make_plant_image(name, width, height):
    plants = get_plants()
    image = plants[name]['images']['idle'][0]
    image = pygame.transform.scale(image, (width, height))
    return image

def make_card_image(width, height, name, cost):
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    image = make_plant_image(name, width * 0.8, height * 0.8)
    surface.blit(image, (10, 10))
    text = COST_FONT.render(str(cost), 1, (0, 0, 0))
    surface.blit(text, (width * 0.8 - text.get_width() + 10, \
            height * 0.8 - text.get_height() + 10))
    
    return surface


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
        for col in range(ROAD_COLS):
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
