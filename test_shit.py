import pygame
from utils.images import load_img

BASE_PATH = "data/characters/red/bottom/0"
END_PATH = ".png"

def test():
    # Testing results of segment size logic
    surface = pygame.display.set_mode((400, 400))

    run = True
    clicking = False
    i = 1
    while run:
        img = load_img(BASE_PATH + str(i) + END_PATH, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not clicking:
                    i = (i + 1) % 4
                    clicking = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    clicking = False

        surface.fill((0, 0, 0))
        surface.blit(pygame.transform.scale(img, (300, 300)), (50, 50))
        pygame.display.update()


if __name__ == "__main__":
    test()