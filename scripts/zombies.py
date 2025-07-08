import random

from scripts.entities import Entity
from scripts.constants import ZOMBIES_APPEARS, SCREEN_WIDTH, SCREEN_HEIGHT
from scripts.utils import make_object_images, shootable_zombies
from scripts.projectiles import Zombie_2_Bullet

class ZombieGenerator:
    ZOMBIES_APPEARS = ZOMBIES_APPEARS
    def __init__(self, map='map0'):
        self.map = map

    def set_map(self, map):
        self.map = map

    def get_zombie(self, permutation):
        zombie = None
        choices = [key for key in self.ZOMBIES_APPEARS[self.map].keys()]
        weights = self.ZOMBIES_APPEARS['map0'].values()
        choosed = random.choices(population=choices, weights=weights)
        if choosed[0] == 'zombie_1':
            zombie = Zombie_1(permutation)
        elif choosed[0] == 'zombie_2':
            zombie = Zombie_2(permutation)

        return zombie

class Zombie(Entity):
    def __init__(self, permutation, images=make_object_images('zombie')):
        super().__init__(None, permutation, images)
        self.live = True
        self.max_hp = self.hp = 100
        self.hp = 80
        self.projectiles = []
        self.shoot_count = 0

    def get_velocity(self):
        return self.velocity
    
    def _move(self):
        if self.action != 'walk':
            self.frame = 0
            self.action = 'walk'
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def _bullet(self):
        if self.name == 'Zombie_2':
            bullet = Zombie_2_Bullet((self.rect.x, self.rect.y), None, self.name)
        self.projectiles.append(bullet)

    def hit(self, objs):
        for projectile in self.projectiles:
            if projectile.collided(objs):
                self.projectiles.remove(projectile)

    def _shoot(self):
        
        for projectile in self.projectiles:
            projectile.update()

        if self.name in shootable_zombies() and self._in_screen():
            self.shoot_count += 1
            if self.shoot_count >= self.shoot_duration:
                self._bullet()
                self.shoot_count = 0

    def _in_screen(self):
        if self.pos[0] < SCREEN_WIDTH and self.pos[1] < SCREEN_HEIGHT:
            return True

        return False


    def update(self):
        self._move()
        super().update()
        self._shoot()

    def draw(self, surf):
        super().draw(surf)
        
        for projectile in self.projectiles:
            projectile.draw(surf)

class Zombie_1(Zombie):
    #IMAGES = {'idle': make_walk_images('zombie', 1), 'walk': make_walk_images('zombie', 1)}
    IMAGES = make_object_images('zombie', 1)
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    NAME = 'Zombie_1'
    def __init__(self, permutation):
        super().__init__(permutation, images=self.IMAGES)
        self.velocity = self.VEL
        self.animation_duration = self.ANIMATION_DURATION
        self.name = self.NAME

class Zombie_2(Zombie):
    #IMAGES = {'idle': [make_object_image('zombie', 2)]}
    #IMAGES = {'idle': make_walk_images('zombie', 2), 'walk': make_walk_images('zombie', 2)}
    IMAGES = make_object_images('zombie', 2)
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    NAME = 'Zombie_2'
    SHOOT_DURATION = 2 * 60
    def __init__(self, permutation):
        super().__init__(permutation, images=self.IMAGES)
        self.velocity = self.VEL
        self.animation_duration = self.ANIMATION_DURATION
        self.name = self.NAME
        self.shoot_duration = self.SHOOT_DURATION


