from pathlib import Path
import serial
import subprocess
import sys
from unittest import TestCase
from unittest.mock import call, patch, MagicMock


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.drawing import ErikaDrawing  # noqa: E402


class ErikaDrawingTest(TestCase):
    TEST_LANGUAGE = 'test'

    @patch('time.sleep')
    @patch('subprocess.PIPE', spec=subprocess.PIPE)
    @patch('subprocess.Popen', spec=subprocess.Popen)
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_draw_image(
        self,
        serial_for_url_mock: MagicMock,
        popen_mock: MagicMock,
        pipe_mock: MagicMock,
        _: MagicMock
    ) -> None:
        step_right = b'\xA5\x03'
        step_down = b'\x81'
        carriage_return = b'\x78'
        dot_wo_carriage_return = b'\xA9\x70'
        printer_ready = b'\x96\x96'

        pgm_image = b'P5\n2 2\n255\n\xff\x00\x00\xff'
        image_path = '/dummy/path/to/image.file'

        imagemagick_command = [
            'magick',
            image_path,
            '-geometry', '{}x>'.format(ErikaDrawing.MAX_WIDTH),
            '-colorspace', 'Gray',
            '-ordered-dither', 'o2x2',
            'pgm:-'
        ]
        magick_process_mock = popen_mock(imagemagick_command, stdout=pipe_mock, stderr=pipe_mock)
        magick_process_mock.returncode = 0
        magick_process_mock.communicate.return_value = pgm_image, None

        serial_device = 'whatever'
        expected_serial_mock_calls = []
        serial_mock = serial_for_url_mock(serial_device, do_not_open=True)
        erika = ErikaDrawing(serial_device, language=self.__class__.TEST_LANGUAGE)

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

        expected_serial_mock_calls.extend(
            [
                call.write(step_right),  # Step right 3 micro steps (not drawing anything in case of white pixel)
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(dot_wo_carriage_return),  # Draw a dot without advancing the carriage
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_right),  # Step right 3 micro steps after drawing a dot
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(carriage_return),  # Return carriage to the beginning of the line
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(dot_wo_carriage_return),  # Draw a dot without advancing the carriage
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_right),  # Step right 3 micro steps after drawing a dot
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(carriage_return),  # Return carriage to the beginning of the line
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
                call.write(step_down),  # Step down 1 micro step
                call.write(printer_ready),  # Send printer ready command (workaround)
            ]
        )

        erika.draw_image(image_path)

        self.assertListEqual(serial_mock.mock_calls, expected_serial_mock_calls)

    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    @patch('subprocess.PIPE', spec=subprocess.PIPE)
    @patch('subprocess.Popen', spec=subprocess.Popen)
    def test_draw_image_when_magick_process_fails(
        self,
        popen_mock: MagicMock,
        pipe_mock: MagicMock,
        *_: MagicMock
    ) -> None:
        image_path = ''
        imagemagick_command = [
            'magick',
            image_path,
            '-rotate', '90',
            '-geometry', '{}x>'.format(ErikaDrawing.MAX_WIDTH),
            '-colorspace', 'Gray',
            '-ordered-dither', 'o2x2',
            'pgm:-'
        ]
        magick_process_mock = popen_mock(imagemagick_command, stdout=pipe_mock, stderr=pipe_mock)
        magick_process_mock.returncode = 1
        magick_process_mock.communicate.return_value = None, b'shit hit the fan'
        erika = ErikaDrawing('', language=self.__class__.TEST_LANGUAGE)

        self.assertRaisesRegex(
            RuntimeError,
            (
                r"^Image converter process \(magick\) "
                r"returned a non-zero exit status \(1\): 'shit hit the fan'\.$"
            ),
            erika.draw_image,
            '',
            True
        )
