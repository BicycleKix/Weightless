import pygame

pygame.init()

def load_img(name: str, colorkey = None) -> pygame.surface.Surface:
    """image loader"""
    img = pygame.image.load(name)
    if colorkey: img.set_colorkey(colorkey)
    return img