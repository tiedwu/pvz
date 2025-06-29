from scripts.entities import Entity
from scripts.utils import make_bullet_images

class Projectile(Entity):
    def _move(self):
        # if self.action != 'walk':
        #     self.frame = 0
        #     self.action = 'walk'
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def update(self):
        super().update()
        self._move()

    def draw(self, surf):
        super().draw(surf)

class Bullet(Projectile):
    IMAGES = make_bullet_images(10)
    VEL = (3, 0)
    ANIMATION_DURATION = 1 * 60
    def __init__(self, pos, permutation, owner):
        super().__init__(pos, permutation, self.IMAGES)
        self.owner = owner
        self.velocity = list(self.VEL)
        self.animation_duration = self.ANIMATION_DURATION

    