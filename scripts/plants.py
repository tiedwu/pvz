import pygame

from scripts.entities import Entity

from scripts.projectiles import PeaShooter_Bullet
from scripts.utils import get_plants, shootable_plants, hitable_plants

from scripts.constants import DAMAGE_PLANTS

class Plant(Entity):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
    ATTACK_COUNT = 2 * 60
    def __init__(self, name, permutation):
        super().__init__(None, permutation, images=get_plants()[name]['images'])
        self.projectiles = []
        self.shoot_count = 0
        self.animation_duration = self.ANIMATION_DURATION
        self.name = name
        self.shoot_duration = self.SHOOT_DURATION
        self.live = True

        self.max_hp = self.hp = 100
        self.hp = 100
        self.attack_count = 0

    def hit(self, objs):
        if self.name not in hitable_plants():
            return
        damage = 0
        if self.name in DAMAGE_PLANTS.keys():
            damage = DAMAGE_PLANTS[self.name]
        collided = False
        for obj in objs:
            if pygame.sprite.collide_mask(self, obj):
                collided = True
                if self.name not in hitable_plants():
                    if self.action != 'damaged':
                        self.action = 'damaged'
                        self.frame = 0
                else:
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
            if self.action == 'attack':
                self.action = "idle"
                self.frame = 0

    def _bullet(self):
        if self.name == 'PeaShooter':
            bullet = PeaShooter_Bullet((self.rect.x + self.rect.width, self.rect.y), None, self.name)
        self.projectiles.append(bullet)

    def shoot(self, objs):
        for projectile in self.projectiles:
            if projectile.collided(objs):
                self.projectiles.remove(projectile)


    def _shoot(self):
        
        for projectile in self.projectiles:
            projectile.update()

        if self.name in shootable_plants():
            self.shoot_count += 1
            if self.shoot_count >= self.shoot_duration:
                self._bullet()
                self.shoot_count = 0

    def draw(self, surf):
        super().draw(surf)
        
        for projectile in self.projectiles:
            projectile.draw(surf)

    def update(self):
        super().update()
        self._shoot()

    def stop(self):
        super().stop()
        for projectile in self.projectiles:
            projectile.stop()

class PeaShooter(Plant):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
    NAME = 'PeaShooter'
    def __init__(self, permutation):
        super().__init__(self.NAME, permutation)
        self.shoot_duration = self.SHOOT_DURATION
       
class SunFlower(Plant):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
    NAME = 'SunFlower'
    def __init__(self, permutation):
        super().__init__(self.NAME, permutation)
        
class ThornyNut(Plant):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
    NAME = 'ThornyNut'
    def __init__(self, permutation):
        super().__init__(self.NAME, permutation)





