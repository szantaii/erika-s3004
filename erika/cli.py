import argparse
from typing import Optional


class ErikaCli:
    def __init__(
        self,
        program_name: Optional[str] = None,
        usage: Optional[str] = None,
        description: Optional[str] = None
    ):
        self._parser = argparse.ArgumentParser(
            prog=program_name,
            usage=usage,
            description=description,
            allow_abbrev=False
        )
        self._parser.add_argument(
            '-d', '--device',
            required=True,
            help='path to the serial device (e.g. /dev/ttyUSB[0-9]+ or /dev/ttyACM[0-9]+)',
            metavar='/dev/ttyUSB0'
        )
        self._parser.add_argument(
            '-l', '--language',
            required=False,
            default='hu-HU',
            help='key for the encoding-decoding map specified in the char_data.json file',
            metavar='hu-HU'
        )

    def parse_args(self) -> dict[str, str]:
        return vars(self._parser.parse_args())
