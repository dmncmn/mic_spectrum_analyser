
from src.device import Mic, MockDevice


class DeviceSelectorSingletonMeta(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class DeviceSelector(metaclass=DeviceSelectorSingletonMeta):

    """ Audio device selector """

    def __init__(self, device='Mock'):
        devices = {
            'Mic': Mic,
            'Mock': MockDevice,
        }
        self._device_class = devices.get(device, MockDevice)
        self._current_device = self._device_class()

    @property
    def _device(self):
        return self._current_device

    @property
    def device_is_alive(self) -> bool:
        return self._device_class.IS_ALIVE

    @property
    def stream_data(self) -> str:
        return self._device.stream_raw_data()

    @property
    def sampling_rate(self) -> int:
        return self._device.RATE

    @property
    def size_data(self) -> int:
        return self._device.CHUNK
