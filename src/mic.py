
import pyaudio
from typing import Union


class MicSingletonMeta(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class Mic(metaclass=MicSingletonMeta):

    IS_ALIVE: bool = True

    def __init__(self):

        self.CHUNK = 1024
        self.RATE = 44100
        self.WIDTH = 2
        self.CHANNELS = 2

        self.stream: Union[pyaudio.Stream, None]
        try:
            self.stream = self.__connect()
        except BaseException:
            Mic.IS_ALIVE = False
            self.stream = None

    def __connect(self) -> pyaudio.Stream:
        p = pyaudio.PyAudio()
        return p.open(format=p.get_format_from_width(self.WIDTH),
                      channels=self.CHANNELS,
                      rate=self.RATE,
                      input=True,
                      output=True,
                      frames_per_buffer=self.CHUNK // 4)

    def stream_raw_data(self) -> Union[str, None]:
        try:
            raw_data = self.stream.read(self.CHUNK // 2)
        except BaseException:
            Mic.IS_ALIVE = False
            raw_data = None
        return raw_data
