
import io
import os
import allure
from typing import Union, NoReturn, Optional
from PIL import Image, ImageChops

screenshots: tuple = ('screenshot_1.png', 'screenshot_2.png')


def images_are_similar(picture_1: str,
                       picture_2: str) -> bool:
    picture_obj_1: Image.Image = Image.open(picture_1)
    picture_obj_2: Image.Image = Image.open(picture_2)
    diff: Union[tuple, None] = ImageChops.difference(picture_obj_1,
                                                     picture_obj_2).getbbox()
    return not bool(diff)


def remove_image(picture: str) -> None:
    if os.path.isfile(picture):
        os.remove(picture)


def get_new_position(first_position: tuple,
                     offset: tuple) -> tuple:
    return tuple(sum(x) for x in zip(first_position, offset)) + \
           first_position[len(offset):]


def allure_attach_screenshot(picture_obj: Image.Image) -> None:
    """ Add Pillow object as a PNG file to allure """
    fp = io.BytesIO()
    picture_obj.save(fp, format='PNG')
    raw = fp.getvalue()
    allure.attach(raw, name="Screenshot",
                  attachment_type=allure.attachment_type.PNG)


def assert_screenshots(same: bool) -> Optional[NoReturn]:
    """ Assert screenshots pair and remove them """
    try:
        assert images_are_similar(*screenshots) is same
    except AssertionError as e:
        raise e
    finally:
        remove_image(screenshots[0])
        remove_image(screenshots[1])
        return None
