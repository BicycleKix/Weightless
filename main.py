import pygame
import sys

from utils.images import load_img
from map import Map

class Game:
    def __init__(self):
        pygame.init()

        self.display_size = (640, 480)
        self.game_size = (640, 440)
        self.ui_offset = self.display_size[1] - self.game_size[1]

        self.screen = pygame.display.set_mode((self.display_size[0]*2, self.display_size[1]*2), pygame.RESIZABLE)
        self.display = pygame.surface.Surface(self.display_size)
        
        self.clock = pygame.time.Clock()

        self.background = load_img("data/BACKGROUND.png")

        self.map = Map(self)

        self.walls = {
            'no': None,
            'two': None,
            'east': None,
            'west': None,
        }
        for name in self.walls.keys():
            self.walls[name] = load_img("data/walls/edge_" + name + "_corner.png")

        self.corners = {
            'no': None,
            'two': None,
            'cw': None,
            'ccw': None,
        }
        for name in self.corners.keys():
            self.corners[name] = load_img("data/walls/corner_" + name + "_corner.png", (255, 0, 0))

    def quit(self):
        pygame.quit()
        sys.exit()

    def main(self):

        self.map.generate_perimeter(0.3, 40)

        running = True

        while running:

            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

            # display rendering
            self.display.blit(self.background, (0, 0))
            
            self.map.render(self.display)
            pygame.draw.rect(self.display, (112, 146, 190), (0, 0, self.display_size[0], self.ui_offset))

            # screen rendering
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)

if __name__ == "__main__":
    Game().main()