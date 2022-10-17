
TITLE: str = "Microphone Spectrum Analyser"

WINDOW_WIDTH: int = 640
WINDOW_HEIGHT: int = 480

TIMER_SHOW_MESSAGE_MS: int = 2000
TIMER_UPDATE_BAR_MS: int = 25
TIMER_LISTEN_MIC_MS: int = 25

SLIDER_RESOLUTION_TEXT_TOOLTIP: str = "Decimation"
SLIDER_RESOLUTION_LABEL_TEXT: str = "Decimation"
SLIDER_RESOLUTION_STEP: int = 1
SLIDER_RESOLUTION_MIN_VALUE: int = 0
SLIDER_RESOLUTION_MAX_VALUE: int = 6
SLIDER_RESOLUTION_CURRENT_VALUE: int = 0

SLIDER_SENSITIVITY_TEXT_TOOLTIP: str = "Sensitivity"
SLIDER_SENSITIVITY_LABEL_TEXT: str = "Sensitivity"
SLIDER_SENSITIVITY_STEP: int = 1
SLIDER_SENSITIVITY_MIN_VALUE: int = 1
SLIDER_SENSITIVITY_MAX_VALUE: int = 100
SLIDER_SENSITIVITY_CURRENT_VALUE: int = 1

CLOSE_BUTTON_TEXT_TOOLTIP: str = "Quit"

PLOT_X_MIN_VALUE: int = 0
PLOT_X_MAX_VALUE: int = 22050
PLOT_Y_MIN_VALUE: int = 0
PLOT_Y_MAX_VALUE: int = 100
PLOT_LEFT_LABEL: str = "Amplitude"
PLOT_BOTTOM_LABEL: str = "Frequency, Hz"
PLOT_BAR_WIDTH: float = 0.8
PLOT_BAR_COLOR: str = 'blue'
PLOT_BAR_COLOR_OVERLOAD: str = 'red'
PLOT_THRESHOLD_OVERLOAD: int = 1000
PLOT_HIDE_AXIS_X: bool = True
PLOT_HIDE_AXIS_Y: bool = True
PLOT_SHOW_GRID_X: bool = True
PLOT_SHOW_GRID_Y: bool = True

LABEL_INIT_TEXT: str = TITLE
LABEL_FULLSCREEN_TEXT: str = "Fullscreen"
LABEL_OVERLOAD_TEXT: str = "Overload"
LABEL_EXCEPTION_TEXT: str = "Microphone is disconnected"
LABEL_OPACITY_TEXT: str = "Opacity"

DEFAULT_OPACITY: int = 10
OPACITY_MIN_VALUE: int = 2
OPACITY_MAX_VALUE: int = 10
OPACITY_STEP_VALUE: int = 1
OPACITY_DIV_FACTOR: int = 10

CSS_MAIN_WINDOW: str = """
    QMainWindow {
        background: rgba(0, 0, 0, 1);
    }
"""

CSS_SLIDERS: str = """
     QSlider::groove:horizontal {
         height: 2px;
         background: tomato;
     }
     QSlider::handle:horizontal {
         background: tomato;
         border: 2px tomato;
         height: 18px;
         width: 18px;
         margin: -5px 0;
         border-radius: 2px;
     }
"""

CSS_QUIT_BUTTON: str = """
     QPushButton {
         background-color: tomato;
         border-radius: 2px;
         height: 10px;
         width: 10px;
     }
"""

CSS_MESSAGE_LABEL: str = """
    QLabel {
        font-size: 12px;
        color: white;
    }
"""
