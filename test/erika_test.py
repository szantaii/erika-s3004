from pathlib import Path
import serial
import sys
from typing import Any
from unittest import TestCase
from unittest.mock import call, patch, MagicMock


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.erika import Erika  # noqa: E402


class ErikaTest(TestCase):
    SERIAL_DEVICE = 'whatever'
    TEST_LANGUAGE = 'test'

    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_connect(self, serial_for_url_mock: MagicMock, *_: Any) -> None:
        serial_mock = serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        serial_mock.is_open = False

        erika = Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE)

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.connect()

        self.assertListEqual(serial_mock.mock_calls, [call.open()])

        serial_mock.is_open = True

        erika.connect()
        erika.connect()
        erika.connect()

        self.assertListEqual(serial_mock.mock_calls, [call.open()])

    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_disconnect(self, serial_for_url_mock: MagicMock, *_: Any) -> None:
        serial_mock = serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        serial_mock.is_open = False

        erika = Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE)

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.disconnect()

        self.assertListEqual(serial_mock.mock_calls, [])

        serial_mock.is_open = True

        erika.disconnect()

        self.assertListEqual(serial_mock.mock_calls, [call.flush(), call.close()])

        serial_mock.is_open = False

        erika.disconnect()
        erika.disconnect()
        erika.disconnect()

        self.assertListEqual(serial_mock.mock_calls, [call.flush(), call.close()])

    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_context_manager(self, serial_for_url_mock: MagicMock, *_: Any) -> None:
        serial_mock = serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        serial_mock.is_open = False

        self.assertListEqual(serial_mock.mock_calls, [])

        with Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE) as _:
            self.assertListEqual(serial_mock.mock_calls, [call.open()])

            serial_mock.is_open = True

        self.assertListEqual(serial_mock.mock_calls, [call.open(), call.flush(), call.close()])

    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_read_bytes(self, serial_for_url_mock: MagicMock, *_: Any) -> None:
        bytes_to_read = 59
        first_read_return_value = b'\x00'
        second_read_return_value = b'\xFF' * bytes_to_read

        serial_mock = serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        serial_mock.read.side_effect = [first_read_return_value, second_read_return_value]

        erika = Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE)

        self.assertListEqual(serial_mock.mock_calls, [])
        self.assertEqual(erika.read_bytes(), first_read_return_value)
        self.assertListEqual(serial_mock.mock_calls, [call.read(size=1)])
        self.assertEqual(erika.read_bytes(size=bytes_to_read), second_read_return_value)
        self.assertListEqual(serial_mock.mock_calls, [call.read(size=1), call.read(size=bytes_to_read)])
