import numpy as np
import pygame

from utils.mathstuffs import common_factors

class Map:
    def __init__(self, game):

        self.game = game
        
        self.wall_list = []
        self.corner_list = [{'x': 'left', 'y': 'top', 'neighbour': 'no', 'angle': 0},
                            {'x': 'right', 'y': 'top', 'neighbour': 'no', 'angle': 270},
                            {'x': 'right', 'y': 'bottom', 'neighbour': 'no', 'angle': 180},
                            {'x': 'left', 'y': 'bottom', 'neighbour': 'no', 'angle': 90}]

    def generate_perimeter(self, difficulty: float, segment_size: int) -> None:

        """Generates the perimeter wall with missing segments, then associates wall type"""

        self.segment_size = segment_size

        # if the given segment size is not a factor of both display dimension, a midrange common factor is chosen
        if self.game.game_size[0] % segment_size != 0 or self.game.game_size[1] % segment_size != 0:
            cfs = common_factors(self.game.game_size[0], self.game.game_size[1])
            choice = int(3*len(cfs)/5)
            segment_size = cfs[choice]
            print("case correction")
        
        # -2 to exclude corners
        self.top_bottom_segment_count = self.game.game_size[0] // segment_size - 2
        self.sides_segment_count = self.game.game_size[1] // segment_size - 2

        # generate wall with holes
        # top
        for i in range(self.top_bottom_segment_count):
            self.wall_list.append({'side': 'top',
                                   'solid': True,
                                   'neighbour': 'no',
                                   'angle': 0,
                                   'index': 0})
            if np.random.rand() < difficulty:
                self.wall_list[-1]['solid'] = False
        # right
        for i in range(self.sides_segment_count):
            self.wall_list.append({'side': 'right',
                                   'solid': True,
                                   'neighbour': 'no',
                                   'angle': 270,
                                   'index': 0})
            if np.random.rand() < difficulty:
                self.wall_list[-1]['solid'] = False
        # bottom
        for i in range(self.top_bottom_segment_count):
            self.wall_list.append({'side': 'bottom',
                                   'solid': True,
                                   'neighbour': 'no',
                                   'angle': 180,
                                   'index': 0})
            if np.random.rand() < difficulty:
                self.wall_list[-1]['solid'] = False
        # left
        for i in range(self.sides_segment_count):
            self.wall_list.append({'side': 'left',
                                   'solid': True,
                                   'neighbour': 'no',
                                   'angle': 90,
                                   'index': 0})
            if np.random.rand() < difficulty:
                self.wall_list[-1]['solid'] = False

        # associate according image to blit
        for i, segment in enumerate(self.wall_list):

            n = len(self.wall_list)
            ccw_segment = self.wall_list[(i-1) % n]
            cw_segment = self.wall_list[(i+1) % n]

            if ccw_segment['side'] == segment['side']:
                segment['index'] = ccw_segment['index'] + 1

            # handle edge cases
            if ccw_segment['side'] != segment['side']: # segment ccw is a corner
                if not cw_segment['solid']: # cw segment is a hole
                    segment['neighbour'] = 'east'
            elif cw_segment['side'] != segment['side']: #segment cw is a corner
                if not ccw_segment['solid']: # ccw segment is a hole
                    segment['neighbour'] = 'west'
            else: # standard case, no adjacent corners
                if not ccw_segment['solid'] and not cw_segment['solid']: # both neighbours are missing
                    segment['neighbour'] = 'two'
                elif ccw_segment['solid'] and not cw_segment['solid']: # cw missing
                    segment['neighbour'] = 'east'
                elif not ccw_segment['solid'] and cw_segment['solid']: # ccw is missing
                    segment['neighbour'] = 'west'

            # handling corners
            if ccw_segment['side'] != segment['side']:
                self.corners(segment, ccw_segment)
                

    def corners(self, seg: dict, prev_seg: dict):
        """generates appropriate corner type"""
        side_to_index = {'top': 0, 'right': 1, 'bottom': 2, 'left': 3}
        i = side_to_index[seg['side']]

        if prev_seg['solid'] and seg['solid']:
            self.corner_list[i]['neighbour'] = 'no'
        elif prev_seg['solid']:
            self.corner_list[i]['neighbour'] = 'cw'
        elif seg['solid']:
            self.corner_list[i]['neighbour'] = 'ccw'
        else:
            self.corner_list[i]['neighbour'] = 'two'


    def render(self, surf: pygame.surface.Surface):
        """render the map on the surface"""
        for corner in self.corner_list:
            pos = (0 if corner['x'] == 'left' else surf.get_width() - self.segment_size, self.game.ui_offset if corner['y'] == 'top' else surf.get_height() - self.segment_size)
            surf.blit(pygame.transform.rotate(pygame.transform.scale(self.game.corners[corner['neighbour']], (self.segment_size, self.segment_size)), corner['angle']), pos)

        for segment in self.wall_list:
            if segment['solid']:
                if segment['side'] == 'top':
                    pos = (self.segment_size*(1+segment['index']), self.game.ui_offset)
                elif segment['side'] == 'bottom':
                    pos = (self.segment_size*(self.top_bottom_segment_count-segment['index']), surf.get_height() - self.segment_size/4)
                elif segment['side'] == 'left':
                    pos = (0, self.game.ui_offset + self.segment_size*(self.sides_segment_count-segment['index']))
                elif segment['side'] == 'right':
                    pos = (surf.get_width() - self.segment_size/4, self.game.ui_offset + self.segment_size*(1+segment['index']))

                surf.blit(pygame.transform.rotate(pygame.transform.scale(self.game.walls[segment['neighbour']], (self.segment_size, self.segment_size/4)), segment['angle']), pos)