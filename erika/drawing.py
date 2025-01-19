from __future__ import annotations
from .erika import Erika
import numpy
import cv2
import random
import subprocess


class ErikaDrawing(Erika):
    MAX_WIDTH = 128
    MICRO_STEP_PER_DOT = 3
    GRAY_PALETTE= (0, 85, 170, 255)
    GRAY_PALETTE_IMAGE_TEMPLATE = (
        'P2\n'
        '{image_width} 1\n'
        '{max_color_value}\n'
        '{colors}\n'
    )

    @classmethod
    def _get_image_data_from_file(cls, image_path: str) -> numpy.ndarray:
        imagemagick_command = [
            'magick',
            image_path,
            '-rotate', '90>',
            '-geometry', '{}x>'.format(cls.MAX_WIDTH),
            '-grayscale', 'Rec709Luma',
            '-normalize',
            '-dither', 'FloydSteinberg',
            '-remap', '-',
            'pgm:-',
        ]

        magick_process = subprocess.Popen(
            imagemagick_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        gray_palette_image = cls.GRAY_PALETTE_IMAGE_TEMPLATE.format(
            image_width=len(cls.GRAY_PALETTE),
            max_color_value=max(cls.GRAY_PALETTE),
            colors=' '.join(map(str, cls.GRAY_PALETTE))
        ).encode()

        pgm_image, stderr = magick_process.communicate(input=gray_palette_image)

        if magick_process.returncode != 0:
            raise RuntimeError('{!r}'.format(stderr))

        return cv2.imdecode(
            numpy.asarray(bytearray(pgm_image), dtype=numpy.uint8),
            cv2.IMREAD_GRAYSCALE
        )

    def _move_to_new_line(self) -> None:
        self.write_string('\r')
        self.micro_step_down(micro_step_count=2 * self.__class__.MICRO_STEP_PER_DOT)

    def print_image(self, image_path: str) -> None:
        dot = self._control.NO_CGE_ADVANCE + '.'.encode(self._encoding_name)
        image_data = self._get_image_data_from_file(image_path)

        for line in image_data:
            continous_white_pixels = 0

            if set(line) == set({max(self.__class__.GRAY_PALETTE)}):
                self._move_to_new_line()

                continue

            for pixel_value in line:
                if pixel_value not in self.__class__.GRAY_PALETTE:
                    raise RuntimeError()

                if pixel_value != max(self.__class__.GRAY_PALETTE):
                    self.micro_step_right(
                        micro_step_count=continous_white_pixels * 2 * self.__class__.MICRO_STEP_PER_DOT
                    )

                    continous_white_pixels = 0

                if pixel_value == 0:
                    self.write_bytes(dot)
                    self.write_bytes(dot)
                    self.micro_step_down(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.write_bytes(dot)
                    self.write_bytes(dot)
                    self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.write_bytes(dot)
                    self.write_bytes(dot)
                    self.micro_step_up(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.write_bytes(dot)
                    self.write_bytes(dot)
                    self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                elif pixel_value == 85:
                    if random.choice([True, False]):
                        self.write_bytes(dot)
                        self.micro_step_down(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                        self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                        self.write_bytes(dot)
                        self.micro_step_up(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                        self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)

                        continue

                    self.micro_step_down(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.write_bytes(dot)
                    self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.micro_step_up(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                    self.write_bytes(dot)
                    self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
                elif pixel_value == 170:
                    half_micro_steps = self.__class__.MICRO_STEP_PER_DOT // 2
                    vertical_padding = random.choice(
                        [half_micro_steps, self.__class__.MICRO_STEP_PER_DOT - half_micro_steps]
                    )
                    horizontal_padding = random.choice(
                        [half_micro_steps, self.__class__.MICRO_STEP_PER_DOT - half_micro_steps]
                    )
                    self.micro_step_down(micro_step_count=vertical_padding)
                    self.micro_step_right(micro_step_count=horizontal_padding)
                    self.write_bytes(dot)
                    self.micro_step_up(
                        micro_step_count=self.__class__.MICRO_STEP_PER_DOT - vertical_padding
                    )
                    self.micro_step_right(
                        micro_step_count=2 * self.__class__.MICRO_STEP_PER_DOT - horizontal_padding
                    )
                else:
                    continous_white_pixels += 1

            self._move_to_new_line()
