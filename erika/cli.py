import argparse
from typing import Optional, Union


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


class InitialStatesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        if values is None:
            setattr(namespace, self.dest, values)

            return

        setattr(
            namespace,
            self.dest,
            [int(char) for char in values if char in '01']
        )


class ErikaAutomatonCli(ErikaCli):
    def __init__(self):
        super().__init__()

        self._parser.add_argument(
            '-r', '--rule',
            required=True,
            type=int,
            # help='TODO',
            metavar='110'
        )
        self._parser.add_argument(
            '-s', '--initial-states',
            required=False,
            default=None,
            action=InitialStatesAction,
            # help='TODO',
            metavar='01010110100111110101011000011101'
        )

    def parse_args(self) -> dict[str, Union[str, Optional[list[int]]]]:
        return {
            k: vars(self._parser.parse_args())[k]
            for k
            in ['device', 'rule', 'language', 'initial_states']
        }
