from pathlib import Path
import sys


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.cli import ErikaCli  # noqa: E402
from erika.erika import Erika  # noqa: E402


if __name__ == '__main__':
    cli_args = ErikaCli().parse_args()
    char_to_text_map = {
        '\n': 'ENTER',
        ' ': 'SPACE',
        '.': "'.' (FULL STOP)",
        '!': "'!' (EXCLAMATION MARK)",
        '?': "'?' (QUESTION MARK)",
        ',': "',' (COMMA)",
        ':': "':' (COLON)",
        '-': "'-' (HYPHEN-MINUS)",
    }
    chars_to_type = (
        'abcdefghijklmnopqrstuvwxyz'
        '\n'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '\n'
        '0123456789'
        '\n'
        ' .!?,:-'
        '\n'
    )

    with Erika(**cli_args) as typewriter:
        for char in chars_to_type:
            if char in char_to_text_map:
                char = char_to_text_map[char]

            print(
                'Type {}{}: '.format(
                    f"'{char}'" if len(char) == 1 else char,
                    '' if char == 'ENTER' or char == 'SPACE' else ' or SPACE if not applicable'
                ),
                end='',
                flush=True
            )
            print('0x{}'.format(typewriter.read_bytes().hex().upper()))
