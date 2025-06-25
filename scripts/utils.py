
import pygame
from scripts.constants import *

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


