
import io
import os
import allure
from typing import NoReturn, Optional
from PIL import Image

screenshots: tuple = ('screenshot_1.png', 'screenshot_2.png')


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


def remove_image(picture: str) -> None:
    if os.path.isfile(picture):
        os.remove(picture)


def assert_screenshots(picture_1: Image.Image,
                       picture_2: Image.Image,
                       same: bool) -> Optional[NoReturn]:
    """ Assert screenshots pair and remove them """
    try:
        with io.BytesIO() as fp:
            picture_1.save(fp, format='PNG')
            picture_1_raw = fp.getvalue()
        with io.BytesIO() as fp:
            picture_2.save(fp, format='PNG')
            picture_2_raw = fp.getvalue()
        assert (picture_1_raw == picture_2_raw) is same
    except AssertionError as e:
        raise e
    else:
        return None
    finally:
        remove_image(screenshots[0])
        remove_image(screenshots[1])
