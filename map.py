import numpy as np
import pygame

from utils.mathstuffs import common_factors, get_distance
from entities import Entity

from walls import EdgeWall, CornerWall

class Map:
    def __init__(self, game):

        self.game = game
        
        self.wall_list = []

    def generate_perimeter(self, difficulty: float, segment_size: int) -> None:

        """Generates the perimeter wall with missing segments, then associates wall type"""

        self.segment_size = segment_size

        # if the given segment size is not a factor of both display dimension, a midrange common factor is chosen
        if self.game.game_size[0] % segment_size != 0 or self.game.game_size[1] % segment_size != 0:
            cfs = common_factors(self.game.game_size[0], self.game.game_size[1])
            choice = int(3*len(cfs)/5)
            self.segment_size = cfs[choice]
            print("case correction")

        self.corner_list = [CornerWall((0, self.game.ui_offset), (self.segment_size, self.segment_size), 0),
                            CornerWall((self.game.display.width - self.segment_size, self.game.ui_offset), (self.segment_size, self.segment_size), 270),
                            CornerWall((self.game.display.width - self.segment_size, self.game.display.height - self.segment_size), (self.segment_size, self.segment_size), 180),
                            CornerWall((0, self.game.display.height - self.segment_size), (self.segment_size, self.segment_size), 90)]
        
        # -2 to exclude corners
        self.top_bottom_segment_count = self.game.game_size[0] // segment_size - 2
        self.sides_segment_count = self.game.game_size[1] // segment_size - 2

        # generate wall with holes
        # top
        for i in range(self.top_bottom_segment_count):
            self.wall_list.append(EdgeWall((self.segment_size*(1 + i), self.game.ui_offset), (self.segment_size, self.segment_size//4), i, 'top'))
            if np.random.rand() < difficulty:
                self.wall_list[-1].solid = False
        # right
        for i in range(self.sides_segment_count):
            self.wall_list.append(EdgeWall((self.game.display.width - self.segment_size//4, self.game.ui_offset + self.segment_size*(1 + i)), (self.segment_size//4, self.segment_size), i, 'right', 270))
            if np.random.rand() < difficulty:
                self.wall_list[-1].solid = False
        # bottom
        for i in range(self.top_bottom_segment_count):
            self.wall_list.append(EdgeWall((self.game.display.width - self.segment_size*(2 + i), self.game.display.height - self.segment_size//4), (self.segment_size, self.segment_size//4), i, 'bottom', 180))
            if np.random.rand() < difficulty:
                self.wall_list[-1].solid = False
        # left
        for i in range(self.sides_segment_count):
            self.wall_list.append(EdgeWall((0, self.game.display.height - self.segment_size*(2 + i)), (self.segment_size//4, self.segment_size), i, 'left', 90))
            if np.random.rand() < difficulty:
                self.wall_list[-1].solid = False

        # associate according image to blit
        for i, segment in enumerate(self.wall_list):

            n = len(self.wall_list)
            ccw_segment = self.wall_list[(i-1) % n]
            cw_segment = self.wall_list[(i+1) % n]

            # handle edge cases
            if ccw_segment.angle != segment.angle: # segment ccw is a corner
                if not cw_segment.solid: # cw segment is a hole
                    segment.neighbours['cw'] = False
            elif cw_segment.angle != segment.angle: #segment cw is a corner
                if not ccw_segment.solid: # ccw segment is a hole
                    segment.neighbours['ccw'] = False
            else: # standard case, no adjacent corners
                if not ccw_segment.solid:
                    segment.neighbours['ccw'] = False
                if not cw_segment.solid:
                    segment.neighbours['cw'] = False

            segment.set_image_path("data/walls/edge_")

            # handling corners
            if ccw_segment.angle != segment.angle:
                self.corners(segment, ccw_segment)

    def corners(self, cw_segment: EdgeWall, ccw_segment: EdgeWall):
        """generates appropriate corner type"""
        side_to_index = {'top': 0, 'right': 1, 'bottom': 2, 'left': 3}
        i = side_to_index[cw_segment.side]

        corner = self.corner_list[i]

        if not ccw_segment.solid:
            corner.neighbours['ccw'] = False
        if not cw_segment.solid:
            corner.neighbours['cw'] = False

        self.corner_list[i].set_image_path("data/walls/corner_", (255, 0, 0))


    def render(self, surf: pygame.surface.Surface):
        """render the map on the surface"""
        for corner in self.corner_list:
            surf.blit(pygame.transform.rotate(pygame.transform.scale(corner.img, (self.segment_size, self.segment_size)), corner.angle), corner.pos)

        for segment in self.wall_list:
            if segment.solid:
                surf.blit(pygame.transform.rotate(pygame.transform.scale(segment.img, (self.segment_size, self.segment_size/4)), segment.angle), segment.pos)
    