import pygame
import sys

from utils.images import load_img

DISPLAY_SIZE = (1280, 960)

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE)
        self.display = pygame.surface.Surface((DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]//2))
        
        self.clock = pygame.time.Clock()

        self.background = load_img("data/BACKGROUND.png")

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
            self.corners[name] = load_img("data/walls/corner_" + name + "_corner.png")

    def quit(self):
        pygame.quit()
        sys.exit()

    def main(self):

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
            self.display.blit(self.background, (0,0))

            # screen rendering
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)

if __name__ == "__main__":
    Game().main()