import pygame

from utils.images import load_img
from entities import Entity
from utils.mathstuffs import get_distance

class Wall:
    def __init__(self, pos: tuple, size: tuple, angle: int = 0, solid: bool = True):
        """class to handle all wall types in the game"""

        self.pos = list(pos)
        self.size = list(size)
        self.angle = angle

        self.solid = solid

        self.neighbours: dict = {
            'cw': True,
            'ccw': True
        }

    def rect(self) -> None:
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_image_path(self, basepath: str, colorkey=None) -> None:
        filepath = basepath
        if self.neighbours['cw'] and self.neighbours['ccw']:
            filepath += 'no'
        elif self.neighbours['cw'] and not self.neighbours['ccw']:
            filepath += 'ccw'
        elif self.neighbours['ccw'] and not self.neighbours['cw']:
            filepath += 'cw'
        else: filepath += 'two'
        filepath += '_corner.png'

        self.define_image(filepath, colorkey)
    
    def define_image(self, filepath: str, colorkey) -> None:
        if colorkey is not None:
            self.img = load_img(filepath, colorkey)
        else:
            self.img = load_img(filepath)
    
    def render(self, surf: pygame.Surface) -> None:
        surf.blit(pygame.transform.rotate(pygame.transform.scale(self.img, tuple(self.size)), self.angle), self.pos)

    def is_nearby(self, entity: Entity) -> bool:
        return get_distance(list(entity.rect().center), list(self.rect().center)) <= 1.5 * ((entity.size/2) + (max(self.size)/2))


class EdgeWall(Wall):
    """non-corner perimeter wall class"""
    def __init__(self, pos: tuple, size: tuple, index: int, side: str, angle: int = 0, solid: bool = True):
        super().__init__(pos, size, angle, solid)

        self.index = index
        self.side = side

class CornerWall(Wall):
    """corner perimeter wall class"""
    def __init__(self, pos: tuple, size: tuple, angle: int = 0, solid: bool = True):

        super().__init__(pos, size, angle, solid)