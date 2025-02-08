import sys

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import COLOR_WHITE, WIN_HEIGHT
from code.Entity import Entity
from code.EntityFractory import EntityFactory


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1bg'))
        self.entity_list.append(EntityFactory.get_entity('WalkPlayer'))
        self.timeout = 20000  # 20 segundos

    def run(self):
        pygame.mixer_music.load('./assets/level1music.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            deltaTime = clock.tick(60) / 1000  # tempo entre quadros (em segundos)

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Exibir informações do nível
            self.level_text(16, f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(16, f'fps: {clock.get_fps() :.0f}', COLOR_WHITE, (10, 17))
            self.level_text(16, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, 27))
            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
