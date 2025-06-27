
import pygame
from scripts.constants import *

pygame.font.init()
OBJECT_FONT = pygame.font.SysFont('comicsans', 30)

def draw_grids(display):
    display.fill(GRASS_COLOR)

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
        color = (255, 0, 0)
    obj_width = obj_height = 64
    surface = pygame.Surface((obj_width, obj_height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, obj_width, obj_height)
    pygame.draw.rect(surface, color, rect)
    text = OBJECT_FONT.render(str(obj_type), 1, (255, 255, 255))
    surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, \
            surface.get_height() // 2 - text.get_height() // 2))
    return surface

# index begin from 1..N
def get_pos_from_permutation(obj, permutation):
    row, col = permutation
    x = MOWER_SPACE + (col - 1) * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_width() // 2)
    y = CARD_HEIGHT + (row - 1) * ROAD_GRID_SIZE + (ROAD_GRID_SIZE // 2 - obj.get_height() // 2)
    return x, y
