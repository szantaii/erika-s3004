from pathlib import Path
import sys


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.cli import ErikaCli  # noqa: E402
from erika.erika import Erika  # noqa: E402


if __name__ == '__main__':
    cli_args = ErikaCli().parse_args()

    with Erika(**cli_args) as tw:
        tw.write_string(
            'You can move the paper up and down\n'
            'and the carriage left or right in smaller\n'
            'steps than a space or backspace character at a time.\n'
            'See the half step and micro step examples below.\n\n\n'
            'Moving the paper and carriage by half steps:\n\n    '
        )

        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for i, char in enumerate(alphabet):
            tw.write_char(char, carriage_advance=False)
            tw.half_step_right()

            if i < (len(alphabet) // 2):
                tw.half_step_down()

                continue

            tw.half_step_up()

        tw.half_step_right(half_step_count=4)

        for i, char in enumerate(alphabet.upper()):
            tw.write_char(char, carriage_advance=False)
            tw.half_step_left()

            if i < (len(alphabet) // 2):
                tw.half_step_down()

                continue

            tw.half_step_up()

        tw.write_string('\n' * 10)
        tw.write_string(
            'You can also move the paper and carriage by micro steps:\n\n'
            '              '
        )

        micro_step_count = 2
        char_count = 30

        for _ in range(char_count):
            tw.write_char('.', carriage_advance=False)
            tw.micro_step_down(micro_step_count=micro_step_count)
            tw.micro_step_right(micro_step_count=micro_step_count)

        for _ in range(char_count):
            tw.write_char('.', carriage_advance=False)
            tw.micro_step_up(micro_step_count=micro_step_count)
            tw.micro_step_right(micro_step_count=micro_step_count)

        for _ in range(char_count):
            tw.write_char('.', carriage_advance=False)
            tw.micro_step_up(micro_step_count=micro_step_count)
            tw.micro_step_left(micro_step_count=micro_step_count)

        for _ in range(char_count):
            tw.write_char('.', carriage_advance=False)
            tw.micro_step_down(micro_step_count=micro_step_count)
            tw.micro_step_left(micro_step_count=micro_step_count)

        tw.write_string('\n' * 10)
