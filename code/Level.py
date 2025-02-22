import sys
import random

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import COLOR_WHITE, WIN_HEIGHT, WIN_WIDTH
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFractory import EntityFactory
from code.Player import Player


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Posição do player (usando o mesmo valor para a altura 'y' do player)
        self.player_y_position = 430

        # Adicionar fundo, player e os inimigos
        self.entity_list.extend(EntityFactory.get_entity('Level1bg'))
        self.entity_list.append(EntityFactory.get_entity('WalkPlayer'))
        self.entity_list.append(EntityFactory.get_entity('PlayerAttack'))

        # Adicionando 3 zumbis ao nível
        self.entity_list.append(Enemy('WalkZombie1', (770, 430)))  # Zumbi 1
        self.entity_list.append(Enemy('WalkZombie2', (720, 430)))  # Zumbi 2
        self.entity_list.append(Enemy('WalkZombie3', (680, 430)))  # Zumbi 3

        # Definir temporizador de spawn
        self.last_spawn_time = pygame.time.get_ticks()  # Hora do último spawn
        self.spawn_interval = 4000  # Intervalo de spawn em milissegundos (4 segundos)

        # Definir limite de zumbis no jogo (caso você queira limitar o número de zumbis na tela)
        self.max_zumbis = 50
        self.zumbi_spawn_limit = 5  # Limite de zumbis sendo spawnados de cada vez

    def run(self):
        pygame.mixer_music.load('./assets/level1music.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(45)
            current_time = pygame.time.get_ticks()

            # Checar se o tempo de spawn passou
            if current_time - self.last_spawn_time >= self.spawn_interval and len(
                    [e for e in self.entity_list if isinstance(e, Enemy)]) < self.max_zumbis:
                self.spawn_zumbis()

            # Detectar colisão entre o ataque do jogador e os inimigos
            player = [e for e in self.entity_list if isinstance(e, Player)][0]  # Encontrar o jogador
            for enemy in [e for e in self.entity_list if isinstance(e, Enemy)]:
                if player.attack_rect.colliderect(enemy.rect):  # Verifica se o retângulo de ataque do jogador colidiu com o inimigo
                    self.handle_enemy_hit(enemy)  # Chama a função para remover o inimigo

            # Mover e desenhar as entidades
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level_text(16, f'fps: {clock.get_fps() :.0f}', COLOR_WHITE, (10, 17))
            self.level_text(16, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, 27))
            pygame.display.flip()

    def handle_enemy_hit(self, enemy):
        """Função para lidar quando o inimigo é atingido pelo ataque do jogador."""
        print("Inimigo atingido!")

        # Remover o inimigo da lista (matar o zumbi)
        self.entity_list.remove(enemy)

        pygame.mixer.Sound('./assets/EnemyDeathSound.wav').play()

    def spawn_zumbis(self):
        """Função para spawnar múltiplos zumbis"""
        spawn_x = random.randint(WIN_WIDTH + 50, WIN_WIDTH + 200)  # Iniciar fora da tela (à direita)

        spawn_y = self.player_y_position  # Usar a variável player_y_position para manter a altura igual à do player

        # Spawnar 3 zumbis ao invés de um só
        for _ in range(3):
            new_zumbi = Enemy('WalkZombie2', (spawn_x, spawn_y))
            self.entity_list.append(new_zumbi)
            spawn_x += random.randint(100, 150)  # Variar a posição X dos zumbis para evitar sobreposição

        # Atualizar o último tempo de spawn
        self.last_spawn_time = pygame.time.get_ticks()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
