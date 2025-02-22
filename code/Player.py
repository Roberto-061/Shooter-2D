import pygame

from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Definir o tamanho dos quadros corretamente
        self.walk_frame_width = 128
        self.walk_frame_height = 128
        self.attack_frame_width = 128
        self.attack_frame_height = 128

        # Carregar as spritesheets separadas para caminhar, atacar e jogar granada
        self.walk_spritesheet = pygame.image.load(f'./assets/WalkPlayer.png').convert_alpha()
        self.attack_spritesheet = pygame.image.load(f'./assets/PlayerAttack.png').convert_alpha()

        # Definir os quadros da animação de caminhada
        self.walk_frames = []
        for i in range(7):  # Número de quadros de caminhada
            walk_frame = self.walk_spritesheet.subsurface(i * self.walk_frame_width, 0, self.walk_frame_width,
                                                          self.walk_frame_height)
            walk_frame = pygame.transform.scale(walk_frame, (200, 200))  # Redimensionamento apenas aqui
            self.walk_frames.append(walk_frame)

        # Definir os quadros da animação de ataque
        self.attack_frames = []
        for i in range(4):  # Número de quadros de ataque
            attack_frame = self.attack_spritesheet.subsurface(i * self.attack_frame_width, 0, self.attack_frame_width,
                                                              self.attack_frame_height)
            attack_frame = pygame.transform.scale(attack_frame, (200, 200))  # Redimensionamento apenas aqui
            self.attack_frames.append(attack_frame)

            # Carregar o efeito sonoro de ataque
            self.attack_sound = pygame.mixer.Sound('./assets/AttackSound.wav')

        # Começar com o primeiro quadro da animação
        self.surf = self.walk_frames[0]  # Iniciar com o primeiro quadro de caminhada
        self.rect = self.surf.get_rect()
        self.rect.center = (50, 430)

        # Variáveis de controle de animação
        self.current_frame = 0
        self.is_walking = False
        self.is_attacking = False
        self.attack_counter = 0

        self.attack_rect = pygame.Rect(0, 0, 0, 0)  # Inicializar o retângulo de ataque com tamanho zero

    def move(self):
        """Controlar o movimento do jogador e as animações"""
        pressed_key = pygame.key.get_pressed()

        # Verifica se o jogador apertou a tecla de ataque (espaço, por exemplo)
        if pressed_key[pygame.K_SPACE]:
            self.start_attack()  # Inicia o ataque, se não estiver atacando já
            self.is_walking = False  # Interrompe a caminhada enquanto ataca

        # Movimento do jogador (só ocorre se não estiver atacando)
        elif not self.is_attacking:
            if pressed_key[pygame.K_RIGHT]:
                self.is_walking = True
                self.rect.centerx += ENTITY_SPEED['WalkPlayer']
                self.surf = pygame.transform.flip(self.walk_frames[self.current_frame], False,
                                                  False)  # Direção para a direita
            elif pressed_key[pygame.K_LEFT] and self.rect.left > 0:
                self.is_walking = True
                self.rect.centerx -= ENTITY_SPEED['WalkPlayer']
                self.surf = pygame.transform.flip(self.walk_frames[self.current_frame], True,
                                                  False)  # Direção para a esquerda
            else:
                self.is_walking = False

        # Atualizar animações
        if self.is_attacking:
            self.attack()  # Executa a animação de ataque
        elif self.is_walking:
            self.walk()  # Executa a animação de caminhada
        else:
            self.idle()  # Caso o jogador esteja parado

    def walk(self):
        """Atualizar a animação de caminhada"""
        self.current_frame += 1
        if self.current_frame >= len(self.walk_frames):
            self.current_frame = 0  # Volta para o primeiro quadro
        self.surf = self.walk_frames[self.current_frame]  # Atualiza a imagem do player sem redimensionar

    def attack(self):
        """Atualizar a animação de ataque"""
        # Atualiza o quadro de ataque
        self.attack_counter += 1
        if self.attack_counter >= len(self.attack_frames) * 5:  # Controla a velocidade da animação
            self.attack_counter = 0
            self.is_attacking = False  # Termina a animação de ataque após o último quadro

            # Após o ataque, desativa o retângulo de ataque (reseta o tamanho)
            self.attack_rect.width = 0
            self.attack_rect.height = 0

        self.surf = self.attack_frames[self.attack_counter // 5]  # Atualiza a imagem do player para o quadro de ataque

    def start_attack(self):
        """Iniciar a animação de ataque"""
        if not self.is_attacking:  # Impede iniciar o ataque enquanto já estiver atacando
            self.is_attacking = True
            self.attack_counter = 0  # Reinicia o contador de animação de ataque
            self.current_frame = 0  # Reinicia a animação de caminhada, caso tenha parado para atacar

            # Atualizar o retângulo de ataque para a posição do jogador
            self.attack_rect.center = self.rect.centerx + 100, self.rect.centery  # Ajuste o valor conforme necessário
            self.attack_rect.width = 300  # Defina o tamanho adequado do retângulo de ataque
            self.attack_rect.height = 50  # Defina a altura adequada para o ataque

            # Tocar o efeito sonoro de ataque
            self.attack_sound.play()

    def idle(self):
        """Caso o jogador não esteja se movendo nem atacando, exibe o quadro de descanso"""
        self.surf = self.walk_frames[0]  # Pode ser o primeiro quadro de caminhada ou um quadro de descanso
