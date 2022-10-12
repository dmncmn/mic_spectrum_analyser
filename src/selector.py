
from src.device import Mic, MockDevice


class DeviceSelectorSingletonMeta(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class DeviceSelector(metaclass=DeviceSelectorSingletonMeta):

    """ Audio device selector """

    IS_ALIVE: bool = True

    def __init__(self, device='Mock'):
        devices = {
            'Mic': Mic,
            'Mock': MockDevice,
        }
        self._device_class = devices.get(device, MockDevice)
        self._current_device = self._device_class()

    def device(self):
        DeviceSelector.IS_ALIVE = self._device_class.IS_ALIVE
        return self._current_device
