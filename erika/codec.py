import codecs
import base64
import json
from pathlib import Path

class ErikaCodec(codecs.Codec):
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

    def encode(self, input: str, errors: str = 'strict') -> tuple[bytes, int]:
        # TODO: encoding error handling (https://docs.python.org/3/library/codecs.html#error-handlers)
        encoded_bytes = b''

        for character in input:
            if character not in self._encoding_map:
                raise UnicodeEncodeError()

            encoded_bytes += self._encoding_map[character]

        return encoded_bytes, len(encoded_bytes)

    def decode(self, input: bytes, errors: str = 'strict') -> tuple[str, int]:
        # TODO: encoding error handling (https://docs.python.org/3/library/codecs.html#error-handlers)
        decoded_string = ''

        for i in range(len(input)):
            encoded_character = input[i: i + 1]

            if encoded_character not in self._decoding_map:
                raise UnicodeDecodeError()

            decoded_string += self._decoding_map[encoded_character]

        return decoded_string, len(decoded_string)
