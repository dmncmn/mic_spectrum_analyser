
TITLE = "Microphone Spectrum Analyser"

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

TIMER_SHOW_MESSAGE_MS = 2000
TIMER_UPDATE_BAR_MS = 25
TIMER_LISTEN_MIC_MS = 10

SLIDER_RESOLUTION_TEXT_TOOLTIP = "Decimation"
SLIDER_RESOLUTION_LABEL_TEXT = "Decimation"
SLIDER_RESOLUTION_STEP = 1
SLIDER_RESOLUTION_MIN_VALUE = 0
SLIDER_RESOLUTION_MAX_VALUE = 6
SLIDER_RESOLUTION_CURRENT_VALUE = 0

SLIDER_SENSITIVITY_TEXT_TOOLTIP = "Sensitivity"
SLIDER_SENSITIVITY_LABEL_TEXT = "Sensitivity"
SLIDER_SENSITIVITY_STEP = 1
SLIDER_SENSITIVITY_MIN_VALUE = 1
SLIDER_SENSITIVITY_MAX_VALUE = 100
SLIDER_SENSITIVITY_CURRENT_VALUE = 1

CLOSE_BUTTON_TEXT_TOOLTIP = "Quit"

PLOT_X_MIN_VALUE = 0
PLOT_X_MAX_VALUE = 10000
PLOT_Y_MIN_VALUE = 0
PLOT_Y_MAX_VALUE = 100
PLOT_LEFT_LABEL = "Amplitude"
PLOT_BOTTOM_LABEL = "Frequency, Hz"
PLOT_BAR_WIDTH = 0.8
PLOT_BAR_COLOR = 'blue'
PLOT_BAR_COLOR_OVERLOAD = 'red'
PLOT_THRESHOLD_OVERLOAD = 1000
PLOT_HIDE_AXIS_X = True
PLOT_HIDE_AXIS_Y = True
PLOT_SHOW_GRID_X = True
PLOT_SHOW_GRID_Y = True

LABEL_INIT_TEXT = TITLE
LABEL_FULLSCREEN_TEXT = "Fullscreen"
LABEL_OVERLOAD_TEXT = "Overload"
LABEL_EXCEPTION_TEXT = "Microphone is disconnected"
LABEL_OPACITY_TEXT = "Opacity"

DEFAULT_OPACITY = 10
OPACITY_MIN_VALUE = 2
OPACITY_MAX_VALUE = 10
OPACITY_STEP_VALUE = 1
OPACITY_DIV_FACTOR = 10

CSS_MAIN_WINDOW = """
    QMainWindow {
        background: rgba(0, 0, 0, 1);
    }
"""

CSS_SLIDERS = """
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

CSS_QUIT_BUTTON = """
     QPushButton {
         background-color: tomato; 
         border-radius: 2px; 
         height: 10px; 
         width: 10px;
     }
"""

CSS_MESSAGE_LABEL = """
    QLabel {
        font-size: 12px; 
        color: white;
    }
"""
