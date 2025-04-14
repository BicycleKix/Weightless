import pygame
import numpy as np

from utils.images import load_img
from entities import Entity
from utils.mathstuffs import get_distance

class Wall:
    def __init__(self, pos: tuple, size: tuple, angle: int, solid: bool = True):
        """class to handle all wall types in the game"""

        self.pos = list(pos)
        self.size = list(size)
        self.angle = angle

        self.solid = solid

        self.neighbours: dict = {
            'cw': True,
            'ccw': True
        }

    def rect(self) -> pygame.Rect:
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
        return get_distance(list(entity.rect().center), list(self.rect().center)) <= 1.75 * ((entity.size/2) + (max(self.size)/2))
    
    def is_nearby_point(self, point: tuple) -> bool:
        return get_distance(list(point), list(self.rect().center)) <= max(self.size) //2


class EdgeWall(Wall):
    """non-corner perimeter wall class"""
    def __init__(self, game: object, pos: tuple, size: tuple, index: int, side: str, angle: int = 0, solid: bool = True):
        super().__init__(pos, size, angle, solid)
        self.game = game

        self.index = index
        self.side = side
        
        self.suction_force = 750.0

    def collision(self, entity: Entity, web = None):

        wall = self.rect()
        entirect = entity.rect()

        if web is None:
            
            if wall.colliderect(entirect):

                wall_left_entity_right = abs(wall.left - entirect.right)
                wall_right_entity_left = abs(wall.right - entirect.left)
                wall_top_entity_bottom = abs(wall.top - entirect.bottom)
                wall_bottom_entity_top = abs(wall.bottom - entirect.top)

                overlap_x = min(wall_left_entity_right, wall_right_entity_left)
                overlap_y = min(wall_bottom_entity_top, wall_top_entity_bottom)

                if overlap_x < overlap_y: # collision came from side
                    if wall_left_entity_right < wall_right_entity_left: # collision came from left
                        entity.pos[0] = wall.left - entity.size // 2
                    else: # collision came from right
                        entity.pos[0] = wall.right + entity.size // 2
                    entity.velocity[0] *= -0.4
                else: # collision came from top / bottom
                    if wall_top_entity_bottom < wall_bottom_entity_top: # collision came from above
                        entity.pos[1] = wall.top - entity.size // 2
                    else: # collision came from below
                        entity.pos[1] = wall.bottom + entity.size // 2
                    entity.velocity[1] *= -0.4

        elif web is not None:

            dx = web['endpoint'][0] - entirect.centerx
            dy = web['endpoint'][1] - entirect.centery
            slope = dy/dx

            collision_cases = [
                self.side == 'top' and web['endpoint'][1] < self.game.ui_offset + self.size[1],
                self.side == 'bottom' and web['endpoint'][1] > self.game.display.height - self.size[1],
                self.side == 'left' and web['endpoint'][0] < self.size[0],
                self.side == 'right' and web['endpoint'][0] > self.game.display.width - self.size[0]
            ]

            if any(collision_cases):
                web['shooting'] = False
                if self.solid:
                    web['sticking'] = True
                    web['stick time'] = 15

            if collision_cases[0]:
                y_target = self.game.ui_offset + self.size[1]
                dy_target = y_target - entirect.centery
                web['endpoint'][0] = entirect.centerx + dy_target/slope
                web['endpoint'][1] = y_target
            elif collision_cases[1]:
                y_target = self.game.display.height - self.size[1]
                dy_target = y_target - entirect.centery
                web['endpoint'][0] = entirect.centerx + dy_target/slope
                web['endpoint'][1] = y_target
            elif collision_cases[2]:
                x_target = self.size[0]
                dx_target = x_target - entirect.centerx
                web['endpoint'][0] = x_target
                web['endpoint'][1] = entirect.centery + slope*dx_target
            elif collision_cases[3]:
                x_target = self.game.display.width - self.size[0]
                dx_target = x_target - entirect.centerx
                web['endpoint'][0] = x_target
                web['endpoint'][1] = entirect.centery + slope*dx_target


    def suction(self, player_pos: tuple):
        pull_force = [0, 0]
        wall_rect = self.rect()
        distance = get_distance(list(player_pos), list(wall_rect.center))
        dx = wall_rect.centerx - player_pos[0]
        dy = wall_rect.centery - player_pos[1]
        theta = np.arctan2(dy, dx)
        suction_cases = [self.side == 'top' and player_pos[1] > self.game.ui_offset + self.size[1],
                         self.side == 'right' and player_pos[0] < self.game.display.width - self.size[0],
                         self.side == 'bottom' and player_pos[1] < self.game.display.height - self.size[1],
                         self.side == 'left' and player_pos[0] > self.size[0]]
        if any(suction_cases):
            pull_force[0] = self.suction_force * np.cos(theta) / distance**2
            pull_force[1] = self.suction_force * np.sin(theta) / distance**2
        return pull_force
class CornerWall(Wall):
    """corner perimeter wall class"""
    def __init__(self, pos: tuple, size: tuple, width: int, angle: int, solid: bool = True):

        super().__init__(pos, size, angle, solid)

        self.width = width

        angle_to_positions = {
            0: ['top', 'left'],
            90: ['bottom', 'left'],
            180: ['bottom', 'right'],
            270: ['top', 'right']
        }

        self.rect_positions = angle_to_positions.get(self.angle, ['top', 'left'])

    def collision(self, entity: Entity):

        wall_slices = []

        horizontal_rect_left = self.pos[0]
        horizontal_rect_top = self.pos[1] + (0 if self.rect_positions[0] == 'top' else (self.size[0] - self.width))
        wall_slices.append(pygame.Rect(horizontal_rect_left, horizontal_rect_top, self.size[0], self.width))

        vertical_rect_left = self.pos[0] + (0 if self.rect_positions[1] == 'left' else (self.size[0] - self.width))
        vertical_rect_top = self.pos[1]
        wall_slices.append(pygame.Rect(vertical_rect_left, vertical_rect_top, self.width, self.size[1]))

        self.wall_slices = wall_slices

        for wall in wall_slices:
            entirect = entity.rect()

            if wall.colliderect(entirect):

                wall_left_entity_right = abs(wall.left - entirect.right)
                wall_right_entity_left = abs(wall.right - entirect.left)
                wall_top_entity_bottom = abs(wall.top - entirect.bottom)
                wall_bottom_entity_top = abs(wall.bottom - entirect.top)

                overlap_x = min(wall_left_entity_right, wall_right_entity_left)
                overlap_y = min(wall_bottom_entity_top, wall_top_entity_bottom)

                if overlap_x < overlap_y: # collision came from side
                    if wall_left_entity_right < wall_right_entity_left: # collision came from left
                        entity.pos[0] = wall.left - entity.size // 2
                    else: # collision came from right
                        entity.pos[0] = wall.right + entity.size // 2
                    entity.velocity[0] *= -0.4
                else: # collision came from top / bottom
                    if wall_top_entity_bottom < wall_bottom_entity_top: # collision came from above
                        entity.pos[1] = wall.top - entity.size // 2
                    else: # collision came from below
                        entity.pos[1] = wall.bottom + entity.size // 2
                    entity.velocity[1] *= -0.4