from scripts.entities import Entity

from scripts.utils import make_object_image
from scripts.projectiles import Bullet

class Plant(Entity):
    def __init__(self, permutation, images={'idle': [make_object_image('plant')]}):
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
    def __init__(self, permutation):
        super().__init__(permutation)
        self.animation_duration = self.ANIMATION_DURATION
        self.name = 'PeaShooter'
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






