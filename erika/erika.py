from .codec import ErikaCodec
from .control import ErikaControl, get_control_values
import codecs
import serial
import struct
import time
from typing import Any, Optional, Self


class Erika:
    BAUD_RATE = 1200
    CONNECTION_OPEN_TIMEOUT = 1  # seconds
    CONNECTION_CLOSE_TIMEOUT = 3  # seconds
    CHARACTER_ENCODING_PREFIX = 'erika_encoding_'
    MAX_MICRO_STEP_COUNT = 127

    def __init__(self, device: str, language: str = 'hu-HU') -> None:
        self._control: ErikaControl = get_control_values()

        self._codec: ErikaCodec = ErikaCodec(language)
        self._encoding_name: str = '{}{}'.format(
            self.__class__.CHARACTER_ENCODING_PREFIX,
            id(self._codec)
        )
        self._codec_info: codecs.CodecInfo = codecs.CodecInfo(
            self._codec.encode,
            self._codec.decode,
            name=self._encoding_name
        )
        self._toggle_codec_registration()

        self._connection: serial.Serial = serial.serial_for_url(device, do_not_open=True)
        self._connection.baudrate = self.__class__.BAUD_RATE
        self._connection.rtscts = True

    def __del__(self) -> None:
        if self._connection.is_open:
            self.disconnect()

        self._toggle_codec_registration()

    def _toggle_codec_registration(self) -> None:
        def codec_search_function(encoding_name: str) -> Optional[codecs.CodecInfo]:
            if encoding_name != self._encoding_name:
                return None

            return self._codec_info

        try:
            codecs.lookup(self._encoding_name)
            codecs.unregister(codec_search_function)
        except LookupError:
            codecs.register(codec_search_function)

    def connect(self) -> None:
        if self._connection.is_open:
            return

        self._connection.open()
        time.sleep(self.__class__.CONNECTION_OPEN_TIMEOUT)

    def disconnect(self) -> None:
        if not self._connection.is_open:
            return

        self._connection.flush()
        time.sleep(self.__class__.CONNECTION_CLOSE_TIMEOUT)
        self._connection.close()

    def __enter__(self) -> Self:
        self.connect()

        return self

    def __exit__(self, *_: Any) -> None:
        self.disconnect()

    def read_bytes(self, size: int = 1) -> bytes:
        return self._connection.read(size=size)

    def write_bytes(self, data: bytes) -> None:
        self._connection.write(data)

        # Workaround because hardware flow control does not work
        # sleep_timeout = 0.25  # seconds
        # if (self._control.MICRO_STEP_LEFT_RIGHT in data
        #         or '\r'.encode(self._encoding_name) in data
        #         or '\n'.encode(self._encoding_name) in data):
        #     sleep_timeout *= 20
        # elif (self._control.MICRO_STEP_DOWN in data
        #         or self._control.MICRO_STEP_UP in data
        #         or '\t'.encode(self._encoding_name) in data):
        #     sleep_timeout *= 2
        # time.sleep(sleep_timeout)

        # Workaround because hardware flow control still does not work
        # properly for some reason :(
        self._connection.write(self._control.PRINTER_READY * 2)

    def read_string(self, size: int = 1) -> str:
        return self.read_bytes(size=size).decode(self._encoding_name)

    def write_string(self, string: str) -> None:
        data = string.encode(self._encoding_name)

        for i in range(len(data)):
            self.write_bytes(data[i: i + 1])

    def _step(self, direction: bytes, step_count: int) -> None:
        if step_count < 1:
            return

        for _ in range(step_count):
            self.write_bytes(direction)

    def _divide_micro_steps(self, micro_step_count: int) -> list[int]:
        if micro_step_count < 1:
            return []

        if micro_step_count < self.__class__.MAX_MICRO_STEP_COUNT:
            return [micro_step_count]

        micro_steps = []

        for _ in range(micro_step_count // self.__class__.MAX_MICRO_STEP_COUNT):
            micro_steps.append(self.__class__.MAX_MICRO_STEP_COUNT)

        remaining_micro_steps = micro_step_count % self.__class__.MAX_MICRO_STEP_COUNT

        if remaining_micro_steps != 0:
            micro_steps.append(remaining_micro_steps)

        return micro_steps

    def _micro_step_horizontally(self, micro_step_count: int) -> None:
        self.write_bytes(
            self._control.MICRO_STEP_LEFT_RIGHT + struct.pack('b', micro_step_count)
        )

    def half_step_up(self, half_step_count: int = 1) -> None:
        self._step(self._control.HALF_STEP_UP, half_step_count)

    def half_step_down(self, half_step_count: int = 1) -> None:
        self._step(self._control.HALF_STEP_DOWN, half_step_count)

    def half_step_left(self, half_step_count: int = 1) -> None:
        self._step(self._control.HALF_STEP_LEFT, half_step_count)

    def half_step_right(self, half_step_count: int = 1) -> None:
        self._step(self._control.HALF_STEP_RIGHT, half_step_count)

    def micro_step_up(self, micro_step_count: int = 1) -> None:
        self._step(self._control.MICRO_STEP_UP, micro_step_count)

    def micro_step_down(self, micro_step_count: int = 1) -> None:
        self._step(self._control.MICRO_STEP_DOWN, micro_step_count)

    def micro_step_left(self, micro_step_count: int = 1) -> None:
        for micro_steps in self._divide_micro_steps(micro_step_count):
            self._micro_step_horizontally(-micro_steps)

    def micro_step_right(self, micro_step_count: int = 1) -> None:
        for micro_steps in self._divide_micro_steps(micro_step_count):
            self._micro_step_horizontally(micro_steps)
