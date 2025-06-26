import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, images, pos):
        super().__init__()
        self.images = images
        self.pos = list(pos)
        self.frame = 0
        self.action = 'idle'
        self.image = self.images[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

    def update(self):
        self._move()
        self.image = self.images[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=self.pos) 

    def _move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

