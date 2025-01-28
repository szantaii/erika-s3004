from .erika import Erika
import subprocess


class ErikaDrawing(Erika):
    MAX_WIDTH = 256
    MICRO_STEP_PER_PIXEL = 3

    @classmethod
    def _get_dithered_image_data_from_file(
        cls,
        image_path: str,
        rotate_90_degrees: bool
    ) -> tuple[int, int, int, list[list[int]]]:
        imagemagick_command = [
            'magick',
            image_path,
            '-rotate', '90',
            '-geometry', '{}x>'.format(cls.MAX_WIDTH),
            '-colorspace', 'Gray',
            '-ordered-dither', 'o2x2',
            'pgm:-'
        ]

        if not rotate_90_degrees:
            del imagemagick_command[2]
            del imagemagick_command[2]

        magick_process = subprocess.Popen(
            imagemagick_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        pgm_image, stderr = magick_process.communicate()

        if magick_process.returncode != 0:
            raise RuntimeError(
                "Image converter process (magick) "
                "returned a non-zero exit status ({}): '{}'.".format(
                    magick_process.returncode,
                    stderr.decode()
                )
            )

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

        # Get image width, height and max gray value (aka white value)
        image_header_fields = (
            pgm_image[0: image_header_size].decode()
                                           .split('\n', maxsplit=3)[:3]
        )

        image_width, image_height = map(int, image_header_fields[1].split(' ', maxsplit=1))
        white_value = int(image_header_fields[2])

        # Get pixel data
        pixel_data = []

        for i in range(image_height):
            pixel_data.append(
                list(
                    pgm_image[image_header_size + i * image_width: image_header_size + i * image_width + image_width]
                )
            )

        return image_width, image_height, white_value, pixel_data

    def draw_image(self, image_path: str, rotate_90_degrees: bool = False) -> None:
        _, _, white_value, pixel_data = self._get_dithered_image_data_from_file(
            image_path,
            rotate_90_degrees
        )

        for line in pixel_data:
            continuous_white_pixels = 0

            for i, pixel_value in enumerate(line):
                if set(line[i:]) == {white_value}:
                    break

                if pixel_value == white_value:
                    continuous_white_pixels += 1

                    continue

                self.micro_step_right(
                    micro_step_count=continuous_white_pixels * self.__class__.MICRO_STEP_PER_PIXEL
                )

                continuous_white_pixels = 0

                self.write_char('.', carriage_advance=False)
                self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_PIXEL)

            self.write_string('\r')
            self.micro_step_down(micro_step_count=self.__class__.MICRO_STEP_PER_PIXEL)
