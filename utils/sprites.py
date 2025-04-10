# png image requires one pixel after all images to be the colorkey, so that it can be automatic

import numpy as np
import pygame
pygame.init()

from .images import load_img

def get_borders(img, border_color, dims):
    borders = np.zeros(dims)

    for x in range(borders.shape[0]):
        for y in range(borders.shape[1]):
            if img.get_at((x, y)) == border_color:
                borders[x][y] = 1

    return borders

def sprite(path, colorkey=None):
    sprite_sheet = load_img(path)
    img_height = sprite_sheet.get_height()
    img_width = sprite_sheet.get_width()
    border_color = sprite_sheet.get_at((0, 0))
    for i in range(sprite_sheet.get_width()):
        if sprite_sheet.get_at((i, 1)) == border_color and sprite_sheet.get_at((i+1, 1)) == border_color:
            img_width = i + 1
            if colorkey is None:
                colorkey = sprite_sheet.get_at((i+2, 0))
            else:
                colorkey = (255, 255, 255)
            break

    for j in range(sprite_sheet.get_height()):
        if sprite_sheet.get_at((1, j)) == border_color and sprite_sheet.get_at((1, j+1)) == border_color:
            img_height = j + 1
            break


    borders = get_borders(sprite_sheet, border_color, (img_width, img_height))
    
    in_borders = np.zeros_like(borders)

    imgs = []

    for x in range(borders.shape[0]):
        for y in range(borders.shape[1]):
            if not borders[x][y] and not in_borders[x][y]:
                y_search = y
                x_search = x
                while not borders[x][y_search]:
                    y_search += 1
                while not borders[x_search][y]:
                    x_search += 1
                in_borders[x:x_search, y:y_search] = 1
                sub_img = sprite_sheet.subsurface(pygame.Rect(x, y, x_search-x, y_search-y))

                sub_img.set_colorkey(colorkey)

                imgs.append(sub_img)


    return imgs