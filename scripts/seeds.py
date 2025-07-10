from scripts.constants import SEED_PACKET_WIDTH, SEED_PACKET_HEIGHT, ENERGY_SPACE, ROAD_GRID_SIZE
from scripts.utils import make_asterisk, make_font

class SeedPacket:
    SIZE = SEED_PACKET_WIDTH
    def __init__(self, pos):
        self.image = make_asterisk(self.SIZE)
        self.pos = list(pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.seeds = 0

    def draw(self, surf):
        surf.blit(self.image, self.pos)
        text = make_font('seed', self.seeds)
        seed_x = ENERGY_SPACE // 2 - text.get_width() // 2
        seed_y = ROAD_GRID_SIZE - 30
        surf.blit(text, (seed_x, seed_y))

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)
