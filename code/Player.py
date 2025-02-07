import pygame

from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.surf = pygame.transform.scale(self.surf, (200,200))
        self.rect = self.surf.get_rect()
        self.rect.center = (50, 480)

    def update(self, ):
        pass

    def move(self, ):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_RIGHT]:
            self.rect.centerx += ENTITY_SPEED[self.name]
        if pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.centerx -= 5
        pass
