import pygame

class Entity:
    def __init__(self, pos: tuple, size: int):

        self.pos = list(pos)
        self.size = size

    def rect(self):
        return pygame.Rect(self.pos[0] - self.size//2, self.pos[1] - self.size//2, self.size, self.size)
        

class Player(Entity):
    def __init__(self, pos: tuple = (0, 0), deadzone: float = 0.2, size: int = 20):
        super().__init__(pos, size)

        self.velocity = [0.0, 0.0]

        self.controller_deadzone = deadzone

        self.acceleration = 0.004
        self.max_speed = 20.0
        self.drag = 0.002

    def rect(self):
        """generates a pygame.rect of an object when necessary using entity position and size"""
        return pygame.Rect(self.pos[0] - self.size//2, self.pos[1] - self.size//2, self.size, self.size)

    def update(self, accel):

        for i, a in enumerate(accel):
            a_mag = (abs(a) - self.controller_deadzone) / (1 - self.controller_deadzone) if abs(a) > self.controller_deadzone else 0
            a_tot = a_mag * (1 if a >= 0 else -1) * self.acceleration
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

    def render(self, surf: pygame.surface.Surface):
        pygame.draw.circle(surf, (255, 0, 0), self.pos, self.size // 2)