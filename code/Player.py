import pygame

from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Definir tamanho dos quadros corretamente
        self.frame_width = 127  # Largura de cada quadro na spritesheet
        self.frame_height = 127  # Altura de cada quadro na spritesheet

        # Carregar a spritesheet
        self.spritesheet = pygame.image.load(f'./assets/{name}.png').convert_alpha()

        # Definir os quadros da animação (supondo 4 quadros para andar para a direita)
        self.walk_frames = []
        for i in range(7):
            walk_frame = self.spritesheet.subsurface(i * self.frame_width, 0, self.frame_width, self.frame_height)
            self.walk_frames.append(walk_frame)

        # Começar com o primeiro quadro da animação
        self.surf = self.walk_frames[0]  # Iniciar com o primeiro quadro da animação
        self.rect = self.surf.get_rect()
        self.rect.center = (50, 460)
        self.surf = pygame.transform.scale(self.surf, (200, 200))
        self.current_frame = 0  # Índice do quadro atual da animação
        self.is_walking = False  # Controlar se está andando ou não

    def move(self, ):
        """Controlar o movimento do jogador e as animações"""
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_RIGHT]:
            self.is_walking = True
            self.rect.centerx += ENTITY_SPEED[self.name]
        elif pressed_key[pygame.K_LEFT] and self.rect.left > 0:
            self.is_walking = True
            self.rect.centerx -= ENTITY_SPEED[self.name]
        else:
            self.is_walking = False

        # Atualizar a animação
        if self.is_walking:
            self.walk()

    def walk(self):
        """Atualizar a animação de caminhada"""
        # Atualizar o quadro atual
        self.current_frame += 1
        if self.current_frame >= len(self.walk_frames):
            self.current_frame = 0  # Volta para o primeiro quadro
        self.surf = self.walk_frames[self.current_frame]  # Atualizar a imagem do player
        self.surf = pygame.transform.scale(self.surf, (200, 200))
