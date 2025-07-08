from scripts.entities import Entity

from scripts.projectiles import PeaShooter_Bullet
from scripts.utils import get_plants, shootable_plants

class Plant(Entity):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
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


    def _bullet(self):
        if self.name == 'PeaShooter':
            bullet = PeaShooter_Bullet((self.rect.x + self.rect.width, self.rect.y), None, self.name)
        self.projectiles.append(bullet)

    def hit(self, objs):
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
        






