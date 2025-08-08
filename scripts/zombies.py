import random
import pygame

from scripts.entities import Entity
from scripts.constants import ZOMBIES_APPEARS, DAMAGE_ZOMBIES, SCREEN_WIDTH, SCREEN_HEIGHT
from scripts.utils import make_object_images, shootable_zombies, hitable_zombies, get_zombies
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
        if choosed[0] == 'Zombie':
            zombie = Zombie(permutation)
        elif choosed[0] == 'PeaZombie':
            zombie = PeaZombie(permutation)

        return zombie



class AbstractZombie(Entity):
    def __init__(self, name, permutation):
        super().__init__(None, permutation, images=get_zombies()[name]['images'])
        self.live = True
        self.max_hp = self.hp = 100
        self.hp = 80
        self.projectiles = []
        self.shoot_count = 0
        self.attack_count = 0

        # zombies properties
        self.velocity = self.VEL
        self.animation_duration = self.ANIMATION_DURATION
        self.name = name

    def get_velocity(self):
        return self.velocity
    
    def _move(self):
        if self.action == 'idle':
            self.action = 'walk'
            self.frame = 0

        if self.action == 'walk':
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]

    def hit(self, objs):
        if self.name not in hitable_zombies():
            return
        damage = 0
        if self.name in DAMAGE_ZOMBIES.keys():
            damage = DAMAGE_ZOMBIES[self.name]
        collided = False
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                collided = True
                self.attack_count += 1
                if self.action != 'attack':
                    self.action = 'attack'
                    self.frame = 0

                if self.attack_count > self.ATTACK_COUNT:
                    self.attack_count = 0
                    obj.hp -= damage
                
                    if obj.hp < 0:
                        obj.hp = 0

        if collided == False:
            if self.action != 'walk':
                self.action = 'walk'
                self.frame = 0

    def _bullet(self):
        if self.name == 'PeaZombie':
            bullet = Zombie_2_Bullet((self.rect.x, self.rect.y), None, self.name)
        self.projectiles.append(bullet)

    def shoot(self, objs):
        for projectile in self.projectiles:
            if projectile.collided(objs):
                self.projectiles.remove(projectile)

        # check any plants was collided
        collided = False
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                collided = True

        if collided == True:
            self.action = 'idle'
            self.velocity = (0, 0)

        else:
            self.action = 'walk'
            self.velocity = self.VEL
        

    def collided(self, objs):
        pass

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

    def inner_home(self):
        if self.pos[0] < 0:
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

    def stop(self):
        super().stop()
        for projectile in self.projectiles:
            projectile.stop()

#1
class Zombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'Zombie'
    #NAME = type(self).__name__
    ATTACK_COUNT = 1 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.NAME = type(self).__name__

#2
class PeaZombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'PeaZombie'
    #NAME = type(self).__name__
    SHOOT_DURATION = 2 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.shoot_duration = self.SHOOT_DURATION
        self.NAME = type(self).__name__

#3
class BucketheadZombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'Zombie'
    #NAME = type(self).__name__
    ATTACK_COUNT = 1 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.NAME = type(self).__name__

#4
class ConeheadZombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'Zombie'
    #NAME = type(self).__name__
    ATTACK_COUNT = 1 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.NAME = type(self).__name__

#5
class FlagZombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'Zombie'
    #NAME = type(self).__name__
    ATTACK_COUNT = 1 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.NAME = type(self).__name__

#6
class NewspaperZombie(AbstractZombie):
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    #NAME = 'Zombie'
    #NAME = type(self).__name__
    ATTACK_COUNT = 1 * 60
    def __init__(self, permutation):
        super().__init__(type(self).__name__, permutation)
        self.NAME = type(self).__name__
