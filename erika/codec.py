import codecs
import base64
import json
from pathlib import Path


class ErikaCodec(codecs.Codec):
    ERROR_HANDLER_ERROR_MESSAGE_TEMPLATE = (
        "{} does not support any error handlers other than 'strict'."
    )

    def __init__(self, language: str) -> None:
        with open(Path(__file__).parent.joinpath('char_data.json')) as char_data_file:
            char_data = json.load(char_data_file)

        self._encoding_map: dict[str, bytes] = {
            k: base64.b64decode(v)
            for k, v
            in char_data[language].items()
        }
        self._decoding_map: dict[bytes, str] = {
            v: k
            for k, v
            in self._encoding_map.items()
        }

    def encode(self, string: str, errors: str = 'strict') -> tuple[bytes, int]:
        if errors != 'strict':
            raise ValueError(
                self.__class__.ERROR_HANDLER_ERROR_MESSAGE_TEMPLATE.format(
                    self.__class__.encode.__qualname__
                )
            )

        encoded_bytes = b''

        for i, character in enumerate(string):
            if character not in self._encoding_map:
                raise UnicodeEncodeError(
                    self.__class__.__name__,
                    character,
                    i,
                    i + 1,
                    'Character not found in encoding map.'
                )

            encoded_bytes += self._encoding_map[character]

        return encoded_bytes, len(encoded_bytes)

    def decode(self, data: bytes, errors: str = 'strict') -> tuple[str, int]:
        if errors != 'strict':
            raise ValueError(
                self.__class__.ERROR_HANDLER_ERROR_MESSAGE_TEMPLATE.format(
                    self.__class__.decode.__qualname__
                )
            )

        if data in self._decoding_map:
            return self._decoding_map[data], len(self._decoding_map[data])

        decoded_string = ''

        for i in range(len(data)):
            encoded_character = data[i: i + 1]

            if encoded_character not in self._decoding_map:
                raise UnicodeDecodeError(
                    self.__class__.__name__,
                    data,
                    i,
                    i + 1,
                    'Byte pattern not found in decoding map.'
                )

            decoded_string += self._decoding_map[encoded_character]

        return decoded_string, len(decoded_string)
