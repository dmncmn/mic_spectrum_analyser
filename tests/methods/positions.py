
import src.styles as s


DESKTOP_RESOLUTION: tuple = 1920, 1080
DEFAULT_APP_REGION: tuple = (
    (DESKTOP_RESOLUTION[0] - s.WINDOW_WIDTH) // 2,
    (DESKTOP_RESOLUTION[1] - s.WINDOW_HEIGHT) // 2,
    s.WINDOW_WIDTH, s.WINDOW_HEIGHT)


DEFAULT_CLICK_POINT: tuple = 0, 0
RIGHT_SLIDER_CLICK_POINT: tuple = 0, s.WINDOW_HEIGHT // 2 - 40
LEFT_SLIDER_CLICK_POINT: tuple = -s.WINDOW_WIDTH // 2 + 40, \
                                  s.WINDOW_HEIGHT // 2 - 40
CLOSE_BUTTON_CLICK_POINT: tuple = -s.WINDOW_WIDTH // 2 + 15, \
                                  s.WINDOW_HEIGHT // 2 - 15
SIZE_GRIP_CLICK_POINT: tuple = s.WINDOW_WIDTH // 2 - 15, \
                               s.WINDOW_HEIGHT // 2 - 15
