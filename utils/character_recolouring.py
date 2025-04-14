import os
import pygame
from images import load_img



def add_character_colour(save_to_name: str, new_colours: dict['top': {'outline': tuple, 'fill': tuple}, 'bottom': {'outline': tuple, 'fill': tuple}]) -> None:
    """function to add a new colour specifically for this game\n
    Based on the original RED CHARACTER\n
    save_to_name | name of colour to be saved to data/characters\n
    new_colours | colours to be used (RGB format)\n
    reference_path | defaulted to red since it was the one I made first\n
    returns | None. Saves new colour to directory"""

    # top
    directory = "data/characters/red/"
    for subfolder in ['top', 'bottom']:
        os.makedirs("data/characters/" + save_to_name + '/' + subfolder, exist_ok=True)
        ref_colours = reference_colours(directory + subfolder + '/')
        for name in os.listdir(directory + subfolder):
            ref_img = load_img(directory  + subfolder + '/' + name, convert=False)
            new_img = replace_colours(ref_img, ref_colours, new_colours[subfolder])
            pygame.image.save(new_img, "data/characters/" + save_to_name + '/' + subfolder + '/' + name)

def replace_colours(img: pygame.Surface, reference_colours: dict, new_colours: dict) -> pygame.Surface:
    new_img = img.copy()

    for x in range(img.width):
        for y in range(img.height):
            current_colour = img.get_at((x, y))

            if current_colour == reference_colours['outline']:
                new_img.set_at((x, y), new_colours['outline'])
            elif current_colour == reference_colours['fill']:
                new_img.set_at((x, y), new_colours['fill'])

    return new_img

def reference_colours(path: str) -> dict:
    reference = load_img(path + "00.png", convert=False)

    colours = {}
    for x in range(reference.width):
        for y in range(reference.height):
            pixel_colour = tuple(reference.get_at((x, y)))
            if pixel_colour not in colours.keys():
                colours[pixel_colour] = 1
            else: colours[pixel_colour] += 1

    del colours[(255, 255, 255, 255)]

    sorted_colours = sorted(colours.items(), key=lambda item: item[1], reverse=True)
    fill_colour = sorted_colours[0][0]
    outline_colour = sorted_colours[1][0]

    return {'outline': outline_colour, 'fill': fill_colour}


if __name__ == '__main__':
    add_character_colour("yellow", {'top': {'outline': (156, 123, 9), 'fill': (250, 228, 87)}, 'bottom': {'outline': (163, 132, 7), 'fill': (219, 177, 9)}})