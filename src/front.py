import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QWidget, QGridLayout, QPushButton, QSlider, QSizeGrip, QLabel

import src.styles as s
from src.stream import StreamAdapter


class WidgetsWindow:

    def __init__(self) -> None:
        super().__init__()

        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.close_button = QPushButton()
        self.close_button.setStyleSheet(s.CSS_QUIT_BUTTON)
        self.close_button.setToolTip(s.CLOSE_BUTTON_TEXT_TOOLTIP)
        self.close_button.clicked.connect(self.quit)
        self.layout.addWidget(self.close_button, 3, 0, QtCore.Qt.AlignLeft)

        self.plot = pg.PlotWidget()
        self.bar_x: np.ndarray = np.array([1])
        self.bar_y: np.ndarray = np.array([1])
        self.bar_x_res: float = .0
        self.bar_graph = pg.BarGraphItem(x0=self.bar_x,
                                         height=self.bar_y,
                                         width=self.bar_x_res)
        self.plot.addItem(self.bar_graph)
        self.plot.setMenuEnabled(False)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setXRange(s.PLOT_X_MIN_VALUE, s.PLOT_X_MAX_VALUE, padding=0)
        self.plot.setYRange(s.PLOT_Y_MIN_VALUE, s.PLOT_Y_MAX_VALUE, padding=0)
        self.plot.setLabel('left', s.PLOT_LEFT_LABEL)
        self.plot.setLabel('bottom', s.PLOT_BOTTOM_LABEL)
        self.plot.showGrid(x=s.PLOT_SHOW_GRID_X, y=s.PLOT_SHOW_GRID_Y)
        if s.PLOT_HIDE_AXIS_X:
            self.plot.hideAxis('bottom')
        if s.PLOT_HIDE_AXIS_Y:
            self.plot.hideAxis('left')
        self.layout.addWidget(self.plot, 1, 1, 1, 2)

        self.slider_sens = QSlider()
        self.slider_sens.setOrientation(QtCore.Qt.Horizontal)
        self.slider_sens.setRange(s.SLIDER_SENSITIVITY_MIN_VALUE,
                                  s.SLIDER_SENSITIVITY_MAX_VALUE)
        self.slider_sens.setValue(s.SLIDER_SENSITIVITY_CURRENT_VALUE)
        self.slider_sens.setSingleStep(s.SLIDER_SENSITIVITY_STEP)
        self.slider_sens.valueChanged.connect(self.sens_setter)
        self.slider_sens.setToolTip(s.SLIDER_SENSITIVITY_TEXT_TOOLTIP)
        self.slider_sens.setStyleSheet(s.CSS_SLIDERS)
        self.layout.addWidget(self.slider_sens, 2, 1)

        self.slider_res = QSlider()
        self.slider_res.setOrientation(QtCore.Qt.Horizontal)
        self.slider_res.setRange(s.SLIDER_RESOLUTION_MIN_VALUE,
                                 s.SLIDER_RESOLUTION_MAX_VALUE)
        self.slider_res.setValue(s.SLIDER_RESOLUTION_CURRENT_VALUE)
        self.slider_res.setSingleStep(s.SLIDER_RESOLUTION_STEP)
        self.slider_res.valueChanged.connect(self.res_setter)
        self.slider_res.setToolTip(s.SLIDER_RESOLUTION_TEXT_TOOLTIP)
        self.slider_res.setStyleSheet(s.CSS_SLIDERS)
        self.layout.addWidget(self.slider_res, 2, 2)

        self.sizegrip = QSizeGrip(self.central_widget)
        self.layout.addWidget(self.sizegrip, 3, 3)

        self.label_message = QLabel()
        self.label_message.setStyleSheet(s.CSS_MESSAGE_LABEL)
        self.label_message.setText(s.LABEL_INIT_TEXT)
        self.layout.addWidget(self.label_message, 3, 1)

        self.timer_listen_stream = QtCore.QTimer()
        self.timer_listen_stream.timeout.connect(self.listen_stream)
        self.timer_listen_stream.start(s.TIMER_LISTEN_MIC_MS)

        self.timer_update_bar = QtCore.QTimer()
        self.timer_update_bar.timeout.connect(self.update_bar)
        self.timer_update_bar.start(s.TIMER_UPDATE_BAR_MS)

        self.timer_show_message = QtCore.QTimer()
        self.timer_show_message.timeout.connect(self.show_message)
        self.timer_show_message.start(s.TIMER_SHOW_MESSAGE_MS)

    @staticmethod
    def quit() -> None:
        sys.exit(0)

    @property
    def message(self) -> str:
        return ''

    @message.setter
    def message(self, value: str) -> None:
        self.label_message.setText(f"{value}")
        self.timer_show_message.start()

    def sens_setter(self, value: int) -> None:
        StreamAdapter.LEVEL = value / \
                              (s.SLIDER_SENSITIVITY_MAX_VALUE - value + 1)
        self.message = f"{s.SLIDER_SENSITIVITY_LABEL_TEXT}: " \
                       f"{round(StreamAdapter.LEVEL, 1)}"

    def res_setter(self, value: int) -> None:
        StreamAdapter.DECIMATION = 2 ** value
        self.message = f"{s.SLIDER_RESOLUTION_LABEL_TEXT}: " \
                       f"{StreamAdapter.DECIMATION}"

    def show_message(self) -> None:
        self.message = s.LABEL_INIT_TEXT
        self.timer_show_message.stop()

    def listen_stream(self) -> None:
        plot_data = StreamAdapter.get_data_ready_to_plot()
        if not StreamAdapter.IS_ALIVE:
            self.message = s.LABEL_EXCEPTION_TEXT
            self.timer_update_bar.stop()
            self.timer_listen_stream.stop()
            return
        if plot_data:
            self.bar_x_res, self.bar_x, self.bar_y = plot_data

    def update_bar(self) -> None:
        if max(self.bar_y) > s.PLOT_THRESHOLD_OVERLOAD:
            color = s.PLOT_BAR_COLOR_OVERLOAD
            self.message = s.LABEL_OVERLOAD_TEXT
        else:
            color = s.PLOT_BAR_COLOR
        self.bar_graph.setOpts(x0=self.bar_x, height=self.bar_y,
                               width=self.bar_x_res * s.PLOT_BAR_WIDTH,
                               brush=color, pen=color)


# TODO fix layout in base class "QWidget"
class WindowFrameless(WidgetsWindow, QMainWindow):  # type: ignore

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.opacity = s.DEFAULT_OPACITY
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet(s.CSS_MAIN_WINDOW)
        self.setWindowOpacity(s.DEFAULT_OPACITY / s.OPACITY_DIV_FACTOR)


class WindowOverrideEvents(WindowFrameless):

    def __init__(self) -> None:
        super().__init__()
        self.drag_pos = QtCore.QPoint()
        self.plot.mousePressEvent = self.mousePressEvent
        self.plot.mouseReleaseEvent = self.mouseReleaseEvent
        self.plot.mouseMoveEvent = self.mouseMoveEvent
        self.plot.wheelEvent = self.wheelEvent

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.timer_update_bar.stop()
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.timer_update_bar.start()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            if self.opacity < s.OPACITY_MAX_VALUE:
                self.opacity += s.OPACITY_STEP_VALUE
        else:
            if self.opacity >= s.OPACITY_MIN_VALUE:
                self.opacity -= s.OPACITY_STEP_VALUE

        self.setWindowOpacity(self.opacity / s.OPACITY_DIV_FACTOR)
        self.message = \
            f"{s.LABEL_OPACITY_TEXT}: {self.opacity * s.OPACITY_DIV_FACTOR}%"

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if not (self.windowState() & QtCore.Qt.WindowMaximized):
            self.message = s.LABEL_FULLSCREEN_TEXT
            self.showMaximized()
            return
        self.showNormal()


class AppFront(WindowOverrideEvents):

    @staticmethod
    def run() -> None:
        app = QApplication(sys.argv)

        screen_geometry = app.desktop().screenGeometry()
        desktop_resolution = screen_geometry.width(), screen_geometry.height()

        center = (desktop_resolution[0] - s.WINDOW_WIDTH) // 2, \
                 (desktop_resolution[1] - s.WINDOW_HEIGHT) // 2

        app_window = WindowOverrideEvents()
        app_window.setGeometry(*center, s.WINDOW_WIDTH, s.WINDOW_HEIGHT)
        app_window.show()

        sys.exit(app.exec())
