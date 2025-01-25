from .erika import Erika
import random
import subprocess


class ErikaDrawing(Erika):
    MAX_WIDTH = 128
    MICRO_STEP_PER_DOT = 3
    GRAY_PALETTE = (0, 85, 170, 255)
    GRAY_PALETTE_IMAGE_TEMPLATE = (
        'P2\n'
        '{image_width} 1\n'
        '{max_color_value}\n'
        '{colors}\n'
    )

    @classmethod
    def _get_image_data_from_file(cls, image_path: str) -> list[list[int]]:
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

        # Process PGM image
        #
        # This is how a 3x3 PGM image looks like:
        #
        #   b'P5\n3 3\n255\n\xff\xff\x00\xff\x00\xff\x00\xff\xff'
        #
        # In general:
        #
        #   1. A "magic number" for identifying the file type.
        #      A pgm image's magic number is the two characters "P5".
        #   2. Whitespace (blanks, TABs, CRs, LFs).
        #   3. A width, formatted as ASCII characters in decimal.
        #   4. Whitespace.
        #   5. A height, again in ASCII decimal.
        #   6. Whitespace.
        #   7. The maximum gray value, again in ASCII decimal.
        #   8. A single whitespace character (usually a newline).
        #   9. A raster of height rows, in order from top to bottom.
        #      Each row consists of width gray values, in order from
        #      left to right. Each gray value is a number from 0 through
        #      maximum gray value, with 0 being black and maximum gray
        #      value being white.

        # Get image header size
        newline_count = 0
        image_header_size = 0

        for _ in range(len(pgm_image)):
            if pgm_image[image_header_size: image_header_size + 1] == b'\n':
                newline_count += 1

            image_header_size += 1

            if newline_count == 3:
                break

        # Get image width and height
        image_width, image_height = map(
            int,
            pgm_image[0: image_header_size].decode().split('\n', maxsplit=2)[1].split(' ', maxsplit=1)
        )

        # Get image data
        image_data = []

        for i in range(image_height):
            image_data.append(
                list(
                    pgm_image[image_header_size + i * image_width: image_header_size + i * image_width + image_width]
                )
            )

        return image_data

    def _move_to_new_line(self) -> None:
        self.write_string('\r')
        self.micro_step_down(micro_step_count=2 * self.__class__.MICRO_STEP_PER_DOT)

    def print_image(self, image_path: str) -> None:
        dot = self._control.NO_CGE_ADVANCE + '.'.encode(self._encoding_name)
        image_data = self._get_image_data_from_file(image_path)

        for line in image_data:
            continuous_white_pixels = 0

            if set(line) == {max(self.__class__.GRAY_PALETTE)}:
                self._move_to_new_line()

                continue

            for pixel_value in line:
                if pixel_value not in self.__class__.GRAY_PALETTE:
                    raise RuntimeError()

                if pixel_value != max(self.__class__.GRAY_PALETTE):
                    self.micro_step_right(
                        micro_step_count=continuous_white_pixels * 2 * self.__class__.MICRO_STEP_PER_DOT
                    )

                    continuous_white_pixels = 0

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
                    continuous_white_pixels += 1

            self._move_to_new_line()
