import pygame
import os

pygame.init()

def load_img(name: str, colorkey = None, convert = True) -> pygame.surface.Surface:
    """image loader"""
    if convert:
        img = pygame.image.load(name).convert_alpha()
    else: img = pygame.image.load(name)
    if colorkey: img.set_colorkey(colorkey)
    return img

def image_list(directory: str, common_colorkey = None) -> list:
    """returns a list of images from a directory"""
    imgs = []
    for name in os.listdir(directory):
        imgs.append(load_img(directory + '/' + name, common_colorkey))

    return imgs

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]