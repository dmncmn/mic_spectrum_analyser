
import os
from typing import Union
from PIL import Image, ImageChops

screenshots: tuple = ('screenshot_1.png', 'screenshot_2.png')


def images_are_similar(picture_1: str,
                       picture_2: str) -> bool:
    picture_obj_1: Image.Image = Image.open(picture_1)
    picture_obj_2: Image.Image = Image.open(picture_2)
    diff: Union[tuple, None] = ImageChops.difference(picture_obj_1,
                                                     picture_obj_2).getbbox()
    if diff is None:
        return True
    return False


def remove_image(picture: str) -> None:
    if os.path.isfile(picture):
        os.remove(picture)


def get_new_position(first_position: tuple,
                     offset: tuple) -> tuple:
    return tuple(sum(x) for x in zip(first_position, offset)) + \
           first_position[len(offset):]
