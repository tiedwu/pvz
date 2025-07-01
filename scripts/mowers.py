from scripts.entities import Entity
from scripts.utils import make_mower_images
from scripts.constants import MOWER_SPACE, ROAD_GRID_SIZE, MOWER_WIDTH, MOWER_HEIGHT

class Mower(Entity):
    VEL = [1, 0]
    ANIMATION_DURATION = 1 * 60
    POSITIONS = [(MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                  ROAD_GRID_SIZE * 1 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2)), 
                  (MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                   ROAD_GRID_SIZE * 2 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2)), 
                (MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                 ROAD_GRID_SIZE * 3 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2)), 
                (MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                 ROAD_GRID_SIZE * 4 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2)), 
                (MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                 ROAD_GRID_SIZE * 5 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2)), 
                (MOWER_SPACE // 2 - MOWER_WIDTH // 2, \
                 ROAD_GRID_SIZE * 6 + (ROAD_GRID_SIZE // 2 - MOWER_HEIGHT // 2))]
    
    def __init__(self, permutation, i):
        super().__init__(self.POSITIONS[i], permutation, make_mower_images(i+1))
        self.attacked = False
        self.animation_duration = self.ANIMATION_DURATION
        self.velocity = self.VEL

    def get_velocity(self):
        return self.velocity
    
    def _move(self):
        if self.action != 'walk':
            self.frame = 0
            self.action = 'walk'
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def update(self):
        if self.attacked:
            self._move()
        
        super().update()

    def attack(self):
        self.attacked = True