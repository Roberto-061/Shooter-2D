from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'Level1bg':
                list_bg = []
                for i in range(8):
                    list_bg.append(Background(f'Level1bg{i}', (0, 0)))
                    list_bg.append(Background(f'Level1bg{i}', (WIN_WIDTH, 0)))
                return list_bg
            case 'WalkPlayer':
                return Player('WalkPlayer', (0, 0))
            case 'PlayerAttack':
                return Player('PlayerAttack', (0, 0))
            case 'WalkZombie1':
                return Enemy('WalkZombie1', position)
            case 'WalkZombie2':
                return Enemy('WalkZombie2', position)
            case 'WalkZombie3':
                return Enemy('WalkZombie3', position)

