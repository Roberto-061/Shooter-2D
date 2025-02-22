import pygame

from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Definir os quadros da animação de caminhada dos zumbis
        self.walk_frame_width = 128  # Largura de cada quadro na spritesheet
        self.walk_frame_height = 128  # Altura de cada quadro na spritesheet

        # Carregar a spritesheet dos zumbis
        self.walk_spritesheet = pygame.image.load(f'./assets/{name}.png').convert_alpha()

        # Definir os quadros da animação de caminhada dos inimigos
        self.walk_frames = []
        for i in range(9):  # Número de quadros de caminhada
            walk_frame = self.walk_spritesheet.subsurface(i * self.walk_frame_width, 0, self.walk_frame_width, self.walk_frame_height)
            walk_frame = pygame.transform.scale(walk_frame, (200, 200))  # Redimensionamento
            self.walk_frames.append(walk_frame)

        # Começar com o primeiro quadro da animação
        self.surf = self.walk_frames[0]  # Iniciar com o primeiro quadro de caminhada
        self.rect = self.surf.get_rect()
        self.rect.center = position

        # Controle de animação
        self.current_frame = 0
        self.is_walking = True  # Zumbis estão sempre andando
        self.speed = 2  # Velocidade do inimigo (ajustar conforme necessário)

    def move(self):
        """Movimentação do inimigo"""
        if self.is_walking:
            self.walk()

        # Movimento simples do zumbi: movendo-se para a esquerda (pode ser alterado para se mover em direção ao jogador)
            self.rect.centerx -= self.speed  # Zumbi anda da direita para a esquerda

    def walk(self):
        """Atualizar a animação de caminhada"""
        self.current_frame += 1
        if self.current_frame >= len(self.walk_frames):
            self.current_frame = 0  # Volta para o primeiro quadro
        self.surf = self.walk_frames[self.current_frame]  # Atualiza a imagem do zumbi