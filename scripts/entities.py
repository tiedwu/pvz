import pygame

from scripts.utils import get_pos_from_permutation

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, permutation, images):
        super().__init__()
        self.images = images
        self.action = 'idle'
        self.image = self.images[self.action][0]
        self.frame = 0
        if pos:
            self.pos = list(pos)
        else:
            self.pos = list(get_pos_from_permutation(self.image, permutation))
        self.rect = self.image.get_rect(topleft=self.pos)

        self.velocity = (0, 0)
        self.frame_count = 0
        
        self.live = False

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

        if self.live:
            width = 64 # suitable obj width 
            pygame.draw.rect(surf, (0, 255, 0), (self.rect.x, self.rect.y - 10, width, 5))
            width = width * (1 - self.hp / self.max_hp)
            if width > 0:
                pygame.draw.rect(surf, (255, 0, 0), (self.rect.x + self.rect.width - width, self.rect.y - 10, width, 5))

    def update(self):
        self._update_animation()
        self.image = self.images[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=self.pos) 
        self.mask = pygame.mask.from_surface(self.image)

    def _update_animation(self):
        self.frame_count += 1
        if self.frame_count > self.animation_duration:
            self.frame += 1
            if self.frame >= len(self.images[self.action]):
                self.frame = 0
            self.frame_count = 0

        

    

