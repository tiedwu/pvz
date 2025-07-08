import pygame

from scripts.entities import Entity
from scripts.utils import make_bullet_images
from scripts.constants import DAMAGE_PLANTS, DAMAGE_ZOMBIES

class Projectile(Entity):
    def __init__(self, pos, permutation, images):
        super().__init__(pos, permutation, images)


    def _move(self):
        # if self.action != 'walk':
        #     self.frame = 0
        #     self.action = 'walk'
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def update(self):
        super().update()
        self._move()
    
    def collided(self, objs):
        damage = 0
        if self.owner in DAMAGE_PLANTS.keys():
            damage = DAMAGE_PLANTS[self.owner]
        elif self.owner in DAMAGE_ZOMBIES.keys():
            damage = DAMAGE_ZOMBIES[self.owner]
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                obj.hp -= damage
                if obj.hp < 0:
                    obj.hp = 0
                return True
        return False


    def draw(self, surf):
        if self.direction == 'LEFT':
            self.rect.x -= self.image.get_width()
        super().draw(surf)

class PeaShooter_Bullet(Projectile):
    IMAGES = make_bullet_images(10)
    VEL = (3, 0)
    ANIMATION_DURATION = 1 * 60
    DIRECTION = 'RIGHT'
    def __init__(self, pos, permutation, owner):
        super().__init__(pos, permutation, self.IMAGES)
        self.owner = owner
        self.velocity = list(self.VEL)
        self.animation_duration = self.ANIMATION_DURATION
        self.direction = self.DIRECTION

class Zombie_2_Bullet(Projectile):
    IMAGES = make_bullet_images(20)
    VEL = (-3, 0)
    ANIMATION_DURATION = 1 * 60
    DIRECTION = 'LEFT'
    def __init__(self, pos, permutation, owner):
        super().__init__(pos, permutation, self.IMAGES)
        self.owner = owner
        self.velocity = list(self.VEL)
        self.animation_duration = self.ANIMATION_DURATION
        self.direction = self.DIRECTION
