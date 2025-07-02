from scripts.entities import Entity

from scripts.projectiles import Bullet
from scripts.utils import get_plants

class Plant(Entity):
    def __init__(self, permutation, images=get_plants()['PeaShooter']):
        super().__init__(None, permutation, images)
        self.projectiles = []

    def _shoot(self):

        # print(self.rect)
        
        bullet = Bullet((self.rect.x + self.rect.width, self.rect.y), None, self.name)
        # bullet = Bullet((100, 200), None, self.name)
        #bullet.action = 'walk's
        self.projectiles.append(bullet)

    def draw(self, surf):
        super().draw(surf)
        
        for projectile in self.projectiles:
            projectile.draw(surf)

    def update(self):
        super().update()
        for projectile in self.projectiles:
            projectile.update()

class PeaShooter(Plant):
    ANIMATION_DURATION = 1 * 60
    SHOOT_DURATION = 2 * 60
    NAME = 'PeaShooter'
    IMAGES=get_plants()[NAME]
    def __init__(self, permutation):
        super().__init__(permutation, self.IMAGES)
        self.animation_duration = self.ANIMATION_DURATION
        self.name = self.NAME
        self.shoot_duration = self.SHOOT_DURATION
        self.shoot_count = 0

    def update(self):
        super().update()
        self.shoot_count += 1
        if self.shoot_count >= self.shoot_duration:
            self.shoot_count = 0
            self._shoot()

    def draw(self, surf):
        super().draw(surf)






