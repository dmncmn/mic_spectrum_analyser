
from typing import Union, Any
from src.device import Mic, MockDevice


DeviceObj = Union[Mic, MockDevice]


class DeviceSelectorSingletonMeta(type):

    __instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> DeviceObj:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class DeviceSelector(metaclass=DeviceSelectorSingletonMeta):

    """ Audio device selector """

    def __init__(self, device: str = 'Mock') -> None:
        devices = {
            'Mic': Mic,
            'Mock': MockDevice,
        }
        self._device_class = devices.get(device, MockDevice)
        self._current_device: DeviceObj = self._device_class()

    @property
    def _device(self) -> DeviceObj:
        return self._current_device

    @property
    def device_is_alive(self) -> bool:
        return self._device_class.IS_ALIVE

    @property
    def stream_data(self) -> bytes:
        return self._device.stream_raw_data()

    @property
    def sampling_rate(self) -> int:
        return self._device.RATE

    @property
    def size_data(self) -> int:
        return self._device.CHUNK
