import pygame
import sys

from utils.images import load_img
from map import Map
from entities import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        # display initialization
        self.display_size = (640, 480)
        self.game_size = (640, 440)
        self.ui_offset = self.display_size[1] - self.game_size[1]

        self.screen = pygame.display.set_mode((self.display_size[0]*2, self.display_size[1]*2), pygame.RESIZABLE)
        self.display = pygame.surface.Surface(self.display_size)

        # clock initialization
        self.clock = pygame.time.Clock()

        # audio loading
        self.music = {
            'load_up': "data/loading.wav"
        }
        
        # main image loading
        self.background = load_img("data/BACKGROUND.png")
        self.logo = load_img("data/MW_logo.png", (255, 255, 255))

        # map initialization
        self.map = Map(self)
        self.wall_segment_size = 40

        # controller and player initialization
        pygame.joystick.init()
        self.controllers = []
        self.players = []
        for i in range(pygame.joystick.get_count()):
            self.controllers.append(pygame.joystick.Joystick(i))
            self.players.append(Player())

    def load_up(self):

        pygame.mixer.music.load(self.music['load_up'])
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

            self.display.fill((63, 72, 204))
            self.display.blit(pygame.transform.scale(self.logo, (self.display.height/2, self.display.height/2)), ((self.display.width - self.display.height/2) / 2, self.display.height / 4))

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

        self.main()

    def quit(self):
        pygame.quit()
        sys.exit()

    def main(self):

        self.map.generate_perimeter(0.5, self.wall_segment_size)

        for player in self.players:
            player.set_images("yellow")

        running = True

        while running:

            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    
            
            for i, controller in enumerate(self.controllers):

                player = self.players[i]

                input_accel = [controller.get_axis(0), controller.get_axis(1)]

                player.aim_direction = [controller.get_axis(2), controller.get_axis(3)]

                if controller.get_button(0):
                    if not player.buttons_pressed['A']:
                        player.pos[0] = 200
                        player.pos[1] = 200
                    player.buttons_pressed['A'] = True
                else:
                    player.buttons_pressed['A'] = False

                if controller.get_button(1):
                    if not player.buttons_pressed['B']:
                        player.web_shot()
                    player.buttons_pressed['B'] = True
                else:
                    if player.buttons_pressed['B']:
                        player.web_shot()
                    player.buttons_pressed['B'] = False

            # display rendering
            self.display.blit(self.background, (0, self.ui_offset))
            pygame.draw.rect(self.display, (36, 31, 38), (0, self.ui_offset, self.display.width, self.display.height - self.ui_offset), width=self.wall_segment_size//4)
            pygame.draw.rect(self.display, (49, 49, 74), (self.wall_segment_size//4 - 2, self.ui_offset + self.wall_segment_size//4 - 2, self.display.width - self.wall_segment_size//2 + 4, self.display.height - self.ui_offset - self.wall_segment_size//2 + 4), width=2)
            pygame.draw.rect(self.display, (36, 31, 38), (0, 0, self.display.width, self.ui_offset))
            
            self.map.render(self.display)

            for player in self.players:

                player.external_forces = [0, 0]

                for wall in self.map.wall_list:
                    if wall.is_nearby(player):
                        if not wall.solid:
                            suction = wall.suction(player.rect().center)
                            player.external_forces[0] += suction[0]
                            player.external_forces[1] += suction[1]
                        else:
                            wall.collision(player)

                    if player.web['shooting'] and wall.is_nearby_point(player.web['endpoint']):
                        wall.collision(player, player.web)

                for corner in self.map.corner_list:
                    if corner.is_nearby(player):
                        corner.collision(player)

                player.update(input_accel)
                player.render(self.display)

            
            # screen rendering
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)

if __name__ == "__main__":
    Game().main()