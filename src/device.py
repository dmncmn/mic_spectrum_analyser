
import pyaudio
import numpy as np
from typing import Optional, Any
from abc import ABCMeta, abstractmethod


class DeviceSingletonABCMeta(ABCMeta):

    __instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class AbstractDevice(metaclass=DeviceSingletonABCMeta):

    """ Default audio device as a singleton """

    @abstractmethod
    def _connect(self) -> pyaudio.Stream: ...

    @abstractmethod
    def stream_raw_data(self) -> Optional[bytes]: ...


class Mic(AbstractDevice):

    """ Mic audio device """

    IS_ALIVE: bool = True

    def __init__(self) -> None:
        self.CHUNK = 1024
        self.RATE = 44100
        self.WIDTH = 2
        self.CHANNELS = 1

        self.stream: pyaudio.Stream
        try:
            self.stream = self._connect()
        except BaseException:
            Mic.IS_ALIVE = False
            self.stream = None

    def _connect(self) -> pyaudio.Stream:
        p = pyaudio.PyAudio()
        return p.open(format=p.get_format_from_width(self.WIDTH),
                      channels=self.CHANNELS,
                      rate=self.RATE,
                      input=True,
                      output=True,
                      frames_per_buffer=self.CHUNK)

    def stream_raw_data(self) -> Optional[bytes]:
        try:
            raw_data = self.stream.read(self.CHUNK,
                                        exception_on_overflow=False)
        except BaseException:
            Mic.IS_ALIVE = False
            raw_data = None
        return raw_data


class MockDevice(AbstractDevice):

    """ Mock audio device """

    IS_ALIVE: bool = True

    def __init__(self) -> None:
        self.CHUNK = 1024
        self.RATE = 44100
        self.stream = None

    def _connect(self) -> pyaudio.Stream: ...

    def stream_raw_data(self) -> bytes:
        data: np.ndarray = \
            np.full(shape=(self.CHUNK,), fill_value=100, dtype=np.int16)
        return np.ndarray.tobytes(data)
