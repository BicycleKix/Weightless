import pygame
import numpy as np

from utils.images import image_list, load_img, Animation

class Entity:
    def __init__(self, pos: tuple, size: int):

        self.pos = list(pos)
        self.size = size

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0] - self.size//2, self.pos[1] - self.size//2, self.size, self.size)
        

class Player(Entity):
    def __init__(self, pos: tuple = (100, 100), deadzone: float = 0.2, size: int = 20):
        super().__init__(pos, size)

        self.external_forces = [0, 0]
        self.acceleration = [0, 0]
        self.velocity = [0.0, 0.0]

        self.controller_deadzone = deadzone

        self.player_acceleration_magnitude = 0.004
        self.max_speed = 20.0
        self.drag = 0.002

        self.aim_direction = [0, 0]

        self.web = {
            "shooting": False,
            "sticking": False,
            "stick time": 0,
            "endpoint": [0, 0],
            "cooldown": 0,
            "angle": 0
        }

        self.blits = {
            'web': load_img("data/web.png", (0, 0, 0))
        }

        self.buttons_pressed = {
            'A': False,
            'B': False,
        }

    def set_images(self, colour_choice: str):
        path = "data/characters/" + colour_choice + '/'
        bottom_dims = load_img(path + "bottom/00.png").get_size()
        top_dims = load_img(path + "top/00.png").get_size()
        self.animations = {
            'bottom': {'animation': Animation(image_list(path + 'bottom', (255, 255, 255)), 90), 'offset': (bottom_dims[0]//2, bottom_dims[1]//2)},
            'top': {'animation': Animation(image_list(path + 'top', (255, 255, 255)), 20), 'offset': (top_dims[0]//2, top_dims[1]//2)}
        }

    def update(self, player_accel: list):

        # update animation frames
        for anim in self.animations.values():
            anim['animation'].update()

        # update abilities
        if self.web['cooldown']:
            self.web['cooldown'] = max(0, self.web['cooldown'] - 1)
        if self.web['cooldown'] < 175 and self.web['shooting']:
            self.web['shooting'] = False
            if not self.web['sticking']:
                self.web['sticking'] = True
                self.web['stick time'] = 15
        if self.web['sticking']:
            self.web['stick time'] = max(0, self.web['stick time'] - 1)
            if self.web['stick time'] == 0:
                self.web['sticking'] = False

        if self.web['shooting']:
            self.web['endpoint'][0] += 10*np.cos(self.web['angle'])
            self.web['endpoint'][1] += 10*np.sin(self.web['angle'])
        if self.web['sticking']:
            self.external_forces[0] = 20*np.cos(self.web['angle'])
            self.external_forces[1] = 20*np.sin(self.web['angle'])

        # update movement
        self.acceleration = [player_accel[0] + self.external_forces[0], player_accel[1] + self.external_forces[1]]

        for i, a in enumerate(self.acceleration):
            a_mag = (abs(a) - self.controller_deadzone) / (1 - self.controller_deadzone) if abs(a) > self.controller_deadzone else 0
            a_tot = a_mag * (1 if a >= 0 else -1) * self.player_acceleration_magnitude
            if a_tot > 0:
                self.velocity[i] = min(self.velocity[i] + a_tot, self.max_speed)
            elif a_tot < 0:
                self.velocity[i] = max(self.velocity[i] + a_tot, -self.max_speed)
            else:
                if self.velocity[i] > 0:
                    self.velocity[i] = max(self.velocity[i] - self.drag, 0)
                elif self.velocity[i] < 0:
                    self.velocity[i] = min(self.velocity[i] + self.drag, 0)
            self.pos[i] += self.velocity[i]
        
        # update eye / aim direction
        for i, vec in enumerate(self.aim_direction):
            vec_mag = (abs(vec) - self.controller_deadzone) / (1 - self.controller_deadzone) if abs(vec) > self.controller_deadzone else 0
            vec_tot = vec_mag * (1 if vec >= 0 else -1) * 2
            if vec_tot > 0:
                self.aim_direction[i] = vec_tot
            elif vec_tot < 0:
                self.aim_direction[i] = vec_tot
            else:
                self.aim_direction[i] = 0

    def web_shot(self):
        if not self.web["cooldown"]:
            if not self.web['shooting']:
                self.web["cooldown"] = 200
                self.web["shooting"] = True
                self.web["endpoint"] = self.pos.copy()
                self.web["angle"] = np.arctan2(self.aim_direction[1], self.aim_direction[0])
        elif self.web['shooting'] and not self.web['sticking']:
            self.web["shooting"] = False
            self.web["sticking"] = True
            self.web["stick time"] = 15


    def render(self, surf: pygame.surface.Surface):

        # render abilities
        if self.web['shooting'] or self.web['sticking']:
            pygame.draw.line(surf, "White", self.pos, self.web['endpoint'])
            if self.web['sticking']:
                surf.blit(pygame.transform.scale(self.blits['web'], (self.blits['web'].width//2, self.blits['web'].height//2)), (self.web['endpoint'][0] - self.blits['web'].width//4, self.web['endpoint'][1] - self.blits['web'].height//4))

        # render player
        for anim in self.animations.values():
            surf.blit(anim['animation'].img(), (self.pos[0] - anim['offset'][0], self.pos[1] - anim['offset'][1]))
        pygame.draw.circle(surf, (255, 255, 255), self.pos, 7)
        pygame.draw.circle(surf, (21, 114, 235), (self.pos[0] + self.aim_direction[0], self.pos[1] + self.aim_direction[1]), 5)
        pygame.draw.circle(surf, (0, 0, 0), (self.pos[0] + self.aim_direction[0], self.pos[1] + self.aim_direction[1]), 4)