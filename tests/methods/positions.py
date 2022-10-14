
from src.styles import *

DESKTOP_RESOLUTION: tuple = 1920, 1080
DEFAULT_APP_REGION: tuple = (
    (DESKTOP_RESOLUTION[0] - WINDOW_WIDTH) // 2,
    (DESKTOP_RESOLUTION[1] - WINDOW_HEIGHT) // 2,
    WINDOW_WIDTH, WINDOW_HEIGHT)


DEFAULT_CLICK_POINT: tuple = 0, 0
RIGHT_SLIDER_CLICK_POINT: tuple = 0, WINDOW_HEIGHT // 2 - 40
LEFT_SLIDER_CLICK_POINT: tuple = -WINDOW_WIDTH // 2 + 40, \
                                  WINDOW_HEIGHT // 2 - 40
CLOSE_BUTTON_CLICK_POINT: tuple = -WINDOW_WIDTH // 2 + 15, \
                                  WINDOW_HEIGHT // 2 - 15
