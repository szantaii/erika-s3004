from pathlib import Path
import serial
import struct
import sys
from types import MappingProxyType
from unittest import TestCase
from unittest.mock import call, patch, MagicMock


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.erika import Erika  # noqa: E402


class ErikaTest(TestCase):
    SERIAL_DEVICE = 'whatever'
    TEST_LANGUAGE = 'test'
    CHAR_ENCODED_CHAR_PAIRS = (
        ('\u0000', b'\x00'),  # Null (nul) (U+0000)
        ('\u0004', b'\x04'),  # End of transmission (eot) (U+0004)
        ('a', b'a'),
        ('b', b'b'),
        ('c', b'c'),
        ('\U0010FFFF', b'\xf1\x03'),  # Largest Unicode code point
    )
    CONTROL_FIELDS = MappingProxyType(
        {
            'HALF_STEP_UP': b'v',
            'HALF_STEP_DOWN': b'u',
            'HALF_STEP_LEFT': b't',
            'HALF_STEP_RIGHT': b's',
            'MICRO_STEP_UP': b'\x82',
            'MICRO_STEP_DOWN': b'\x81',
            'MICRO_STEP_LEFT_RIGHT': b'\xa5',
            'PRINTER_READY': b'\x96',
            'NO_CGE_ADVANCE': b'\xa9',
        }
    )

    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def _get_test_instance_and_serial_mock(
        self,
        serial_for_url_mock: MagicMock,
    ) -> tuple[Erika, MagicMock]:
        return (
            Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE),
            serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        )

    @patch('time.sleep')
    def test_connect(self, _: MagicMock) -> None:
        erika, serial_mock = self._get_test_instance_and_serial_mock()
        serial_mock.is_open = False

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.connect()

        self.assertListEqual(serial_mock.mock_calls, [call.open()])

        serial_mock.is_open = True

        erika.connect()
        erika.connect()
        erika.connect()

        self.assertListEqual(serial_mock.mock_calls, [call.open()])

    @patch('time.sleep')
    def test_disconnect(self, _: MagicMock) -> None:
        erika, serial_mock = self._get_test_instance_and_serial_mock()
        serial_mock.is_open = False

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
    def test_context_manager(self, serial_for_url_mock: MagicMock, _: MagicMock) -> None:
        serial_mock = serial_for_url_mock(self.__class__.SERIAL_DEVICE, do_not_open=True)
        serial_mock.is_open = False

        self.assertListEqual(serial_mock.mock_calls, [])

        with Erika(self.__class__.SERIAL_DEVICE, language=self.__class__.TEST_LANGUAGE) as _:
            self.assertListEqual(serial_mock.mock_calls, [call.open()])

            serial_mock.is_open = True

        self.assertListEqual(serial_mock.mock_calls, [call.open(), call.flush(), call.close()])

    @patch('time.sleep')
    def test_read_bytes(self, _: MagicMock) -> None:
        bytes_to_read = 59
        first_read_return_value = b'\x00'
        second_read_return_value = b'\xFF' * bytes_to_read

        erika, serial_mock = self._get_test_instance_and_serial_mock()
        serial_mock.read.side_effect = [first_read_return_value, second_read_return_value]

        self.assertListEqual(serial_mock.mock_calls, [])
        self.assertEqual(erika.read_bytes(), first_read_return_value)
        self.assertListEqual(serial_mock.mock_calls, [call.read(size=1)])
        self.assertEqual(erika.read_bytes(size=bytes_to_read), second_read_return_value)
        self.assertListEqual(serial_mock.mock_calls, [call.read(size=1), call.read(size=bytes_to_read)])

    @patch('time.sleep')
    def test_read_string(self, _: MagicMock) -> None:
        first_read_return_value = self.__class__.CHAR_ENCODED_CHAR_PAIRS[0][1]
        first_read_expected_value = self.__class__.CHAR_ENCODED_CHAR_PAIRS[0][0]
        second_read_return_value = self.__class__.CHAR_ENCODED_CHAR_PAIRS[1][1] \
            + self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1] \
            + self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][1]
        second_read_expected_value = self.__class__.CHAR_ENCODED_CHAR_PAIRS[1][0] \
            + self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][0] \
            + self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][0]

        erika, serial_mock = self._get_test_instance_and_serial_mock()
        serial_mock.read.side_effect = [first_read_return_value, second_read_return_value]

        self.assertListEqual(serial_mock.mock_calls, [])
        self.assertEqual(erika.read_string(), first_read_expected_value)
        self.assertListEqual(serial_mock.mock_calls, [call.read(size=1)])
        self.assertEqual(
            erika.read_string(size=len(second_read_expected_value)),
            second_read_expected_value
        )
        self.assertListEqual(
            serial_mock.mock_calls,
            [call.read(size=1), call.read(size=len(second_read_return_value))]
        )

    @patch('time.sleep')
    def test_write_bytes(self, _: MagicMock) -> None:
        bytes_to_write = 59
        write_values = [b'\x00', b'\xFF' * bytes_to_write]
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.write_bytes(write_values[0])

        self.assertListEqual(
            serial_mock.mock_calls,
            [
                call.write(write_values[0]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
            ]
        )

        erika.write_bytes(write_values[1])

        self.assertListEqual(
            serial_mock.mock_calls,
            [
                call.write(write_values[0]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(write_values[1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
            ]
        )

    @patch('time.sleep')
    def test_write_char(self, _: MagicMock) -> None:
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.write_char(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][0])

        self.assertListEqual(
            serial_mock.mock_calls,
            [
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
            ]
        )

        erika.write_char(self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][0], carriage_advance=False)

        self.assertListEqual(
            serial_mock.mock_calls,
            [
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(
                    self.CONTROL_FIELDS['NO_CGE_ADVANCE'] + self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][1]
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
            ]
        )

    @patch('time.sleep')
    def test_write_char_with_non_characters(self, _: MagicMock) -> None:
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, [])

        non_characters = [
            0,
            -0.001,
            'this is a multi-character string, not a single character with str type',
            None,
        ]

        for non_character in non_characters:
            with self.subTest("Call write_char with non-character value '{}'".format(non_character)):
                self.assertRaisesRegex(
                    ValueError,
                    (
                        r"^First argument of Erika\.write_char must be a single character with 'str' type, "
                        r"but '.*?' of type '.*?' was provided instead\.$"
                    ),
                    erika.write_char,
                    non_character
                )

    @patch('time.sleep')
    def test_write_string(self, _: MagicMock) -> None:
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, [])

        erika.write_string(
            self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][0] * 3 + self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][0] * 2
        )

        self.assertListEqual(
            serial_mock.mock_calls,
            [
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[2][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
                call.write(self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][1]),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),  # Due to applied workaround
            ]
        )

    @patch('time.sleep')
    def test_half_steps(self, _: MagicMock) -> None:
        expected_serial_mock_calls = []
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.half_step_up(half_step_count=0)
        erika.half_step_down(half_step_count=0)
        erika.half_step_left(half_step_count=0)
        erika.half_step_right(half_step_count=0)

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.half_step_up()

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['HALF_STEP_UP']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ]
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.half_step_down()

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['HALF_STEP_DOWN']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ]
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.half_step_left()

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['HALF_STEP_LEFT']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ]
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.half_step_right(half_step_count=3)

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['HALF_STEP_RIGHT']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ] * 3
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

    @patch('time.sleep')
    def test_micro_step_up_down(self, _: MagicMock) -> None:
        expected_serial_mock_calls = []
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.micro_step_up(micro_step_count=0)
        erika.micro_step_down(micro_step_count=0)

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.micro_step_up(micro_step_count=2)

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['MICRO_STEP_UP']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ] * 2
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.micro_step_down(micro_step_count=569)

        expected_serial_mock_calls.extend(
            [
                call.write(self.__class__.CONTROL_FIELDS['MICRO_STEP_DOWN']),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ] * 569
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

    @patch('time.sleep')
    def test_micro_step_left_right(self, _: MagicMock) -> None:
        expected_serial_mock_calls = []
        erika, serial_mock = self._get_test_instance_and_serial_mock()

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.micro_step_left(micro_step_count=0)
        erika.micro_step_right(micro_step_count=0)

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        erika.micro_step_left(micro_step_count=Erika.MAX_MICRO_STEP_COUNT)
        erika.micro_step_right(micro_step_count=Erika.MAX_MICRO_STEP_COUNT)

        expected_serial_mock_calls.extend(
            [
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', -1 * Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ]
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        test_micro_step_count = 2 * Erika.MAX_MICRO_STEP_COUNT + 1

        erika.micro_step_right(micro_step_count=test_micro_step_count)
        erika.micro_step_left(micro_step_count=test_micro_step_count)

        expected_serial_mock_calls.extend(
            [
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', 1)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', -1 * Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', -1 * Erika.MAX_MICRO_STEP_COUNT)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
                call.write(
                    self.__class__.CONTROL_FIELDS['MICRO_STEP_LEFT_RIGHT']
                    + struct.pack('b', -1)
                ),
                call.write(self.__class__.CONTROL_FIELDS['PRINTER_READY'] * 2),
            ]
        )

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)
