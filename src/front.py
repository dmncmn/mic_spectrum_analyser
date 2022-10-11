
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QWidget, QGridLayout, QPushButton, QSlider, QSizeGrip, QLabel

from src.styles import *
from src.stream import Stream
from src.fft import FFT


class WidgetsWindow:

    def __init__(self):
        super().__init__()

        self.decimation: int = FFT.FFT_DEFAULT_DECIMATION_FACTOR
        self.sensitivity: int = FFT.FFT_DEFAULT_LEVEL_FACTOR

        self.YDATA: np.ndarray = np.empty(1)

        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.close_button = QPushButton()
        self.close_button.setStyleSheet(CSS_QUIT_BUTTON)
        self.close_button.setToolTip(CLOSE_BUTTON_TEXT_TOOLTIP)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button, 3, 0)

        self.plot = pg.PlotWidget()
        self.bargraph = pg.BarGraphItem(x=[], height=[], width=1)
        self.plot.addItem(self.bargraph)
        self.plot.setMenuEnabled(False)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.showGrid(x=False, y=False)
        self.plot.setXRange(PLOT_X_MIN_VALUE, PLOT_X_MAX_VALUE, padding=0)
        self.plot.setYRange(PLOT_Y_MIN_VALUE, PLOT_Y_MAX_VALUE, padding=0)
        self.plot.setLabel('left', PLOT_LEFT_LABEL)
        self.plot.setLabel('bottom', PLOT_BOTTOM_LABEL)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.layout.addWidget(self.plot, 1, 1, 1, 2)

        self.slider_sens = QSlider()
        self.slider_sens.setOrientation(QtCore.Qt.Horizontal)
        self.slider_sens.setRange(SLIDER_SENSITIVITY_MIN_VALUE,
                                  SLIDER_SENSITIVITY_MAX_VALUE)
        self.slider_sens.setValue(SLIDER_SENSITIVITY_CURRENT_VALUE)
        self.slider_sens.setSingleStep(SLIDER_SENSITIVITY_STEP)
        self.slider_sens.valueChanged.connect(self.sens_setter)
        self.slider_sens.setToolTip(SLIDER_SENSITIVITY_TEXT_TOOLTIP)
        self.slider_sens.setStyleSheet(CSS_SLIDERS)
        self.layout.addWidget(self.slider_sens, 2, 1)

        self.slider_res = QSlider()
        self.slider_res.setOrientation(QtCore.Qt.Horizontal)
        self.slider_res.setRange(SLIDER_RESOLUTION_MIN_VALUE,
                                 SLIDER_RESOLUTION_MAX_VALUE)
        self.slider_res.setValue(SLIDER_RESOLUTION_CURRENT_VALUE)
        self.slider_res.setSingleStep(SLIDER_RESOLUTION_STEP)
        self.slider_res.valueChanged.connect(self.res_setter)
        self.slider_res.setToolTip(SLIDER_RESOLUTION_TEXT_TOOLTIP)
        self.slider_res.setStyleSheet(CSS_SLIDERS)
        self.layout.addWidget(self.slider_res, 2, 2)

        self.sizegrip = QSizeGrip(self)
        self.layout.addWidget(self.sizegrip, 3, 3)

        self.label_message = QLabel()
        self.label_message.setStyleSheet(CSS_MESSAGE_LABEL)
        self.label_message.setText(LABEL_INIT_TEXT)
        self.layout.addWidget(self.label_message, 3, 1)

        self.timer_listen_stream = QtCore.QTimer()
        self.timer_listen_stream.timeout.connect(self.listen_stream)
        self.timer_listen_stream.start(TIMER_LISTEN_MIC_MS)

        self.timer_update_bar = QtCore.QTimer()
        self.timer_update_bar.timeout.connect(self.update_bar)
        self.timer_update_bar.start(TIMER_UPDATE_BAR_MS)

        self.timer_show_message = QtCore.QTimer()
        self.timer_show_message.timeout.connect(self.show_message)
        self.timer_show_message.start(TIMER_SHOW_MESSAGE_MS)

    @property
    def message(self) -> None:
        return None

    @message.setter
    def message(self, value):
        self.label_message.setText(f"{value}")
        self.timer_show_message.start()

    def sens_setter(self, value):
        self.sensitivity = value / 10
        self.message = f"{SLIDER_SENSITIVITY_LABEL_TEXT}: {value}"

    def res_setter(self, value):
        self.decimation = 2 ** value
        self.message = f"{SLIDER_RESOLUTION_LABEL_TEXT}: {self.decimation}"

    def show_message(self):
        self.message = LABEL_INIT_TEXT
        self.timer_show_message.stop()

    def listen_stream(self):

        if not Stream.IS_ALIVE:
            self.message = LABEL_EXCEPTION_TEXT
            self.timer_update_bar.stop()
            self.timer_listen_stream.stop()
            return

        self.YDATA = Stream.get_data_ready_to_plot(self.decimation,
                                                   self.sensitivity)

    def update_bar(self):

        if self.YDATA is None:
            return

        if max(self.YDATA) > PLOT_THRESHOLD_OVERLOAD:
            color = PLOT_BAR_COLOR_OVERLOAD
            self.message = LABEL_OVERLOAD_TEXT
        else:
            color = PLOT_BAR_COLOR

        XDATA_STEP = PLOT_X_MAX_VALUE / len(self.YDATA) * 2
        XDATA = np.arange(PLOT_X_MIN_VALUE, PLOT_X_MAX_VALUE, XDATA_STEP)
        self.bargraph.setOpts(x=XDATA,
                              height=self.YDATA,
                              width=XDATA_STEP * PLOT_BAR_WIDTH,
                              brush=color, pen=color)


class WindowFrameless(WidgetsWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.opacity = DEFAULT_OPACITY
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet(CSS_MAIN_WINDOW)
        self.setWindowOpacity(DEFAULT_OPACITY / OPACITY_DIV_FACTOR)


class WindowOverrideEvents(WindowFrameless):

    def __init__(self):
        super().__init__()
        self.drag_pos = QtCore.QPoint()
        self.sizegrip.mouseMoveEvent = self.dummyEventOverride
        self.plot.mousePressEvent = self.mousePressEvent
        self.plot.mouseReleaseEvent = self.mouseReleaseEvent
        self.plot.mouseMoveEvent = self.mouseMoveEvent
        self.plot.wheelEvent = self.wheelEvent

    def dummyEventOverride(self, event) -> None:
        ...

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.timer_update_bar.stop()
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event) -> None:
        self.timer_update_bar.start()

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            if self.opacity < OPACITY_MAX_VALUE:
                self.opacity += OPACITY_STEP_VALUE
        else:
            if self.opacity >= OPACITY_MIN_VALUE:
                self.opacity -= OPACITY_STEP_VALUE

        self.setWindowOpacity(self.opacity / OPACITY_DIV_FACTOR)
        self.message = \
            f"{LABEL_OPACITY_TEXT}: {self.opacity * OPACITY_DIV_FACTOR}%"

    def mouseDoubleClickEvent(self, event) -> None:
        if not (self.windowState() & QtCore.Qt.WindowMaximized):
            self.message = LABEL_FULLSCREEN_TEXT
            self.showMaximized()
            return
        self.showNormal()


class AppFront(WindowOverrideEvents):

    @staticmethod
    def run():
        app = QApplication(sys.argv)

        desktop_resolution = app.desktop().screenGeometry().width(), \
                             app.desktop().screenGeometry().height()

        center = (desktop_resolution[0] - WINDOW_WIDTH) // 2, \
                 (desktop_resolution[1] - WINDOW_HEIGHT) // 2

        app_window = WindowOverrideEvents()
        app_window.setGeometry(*center, WINDOW_WIDTH, WINDOW_HEIGHT)
        app_window.show()

        sys.exit(app.exec())
