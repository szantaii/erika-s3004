from pathlib import Path
import sys
from unittest import TestCase


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.codec import ErikaCodec  # noqa: E402


class ErikaCodecTest(TestCase):
    CHAR_ENCODED_CHAR_PAIRS = (
        ('\u0000', b'\x00'),  # Null (nul) (U+0000)
        ('\u0004', b'\x04'),  # End of transmission (eot) (U+0004)
        ('a', b'a'),
        ('b', b'b'),
        ('c', b'c'),
        ('\U0010FFFF', b'\xf1\x03'),  # Largest Unicode code point
    )
    UNSUPPORTED_ERROR_HANDLERS = (
        'ignore',
        'replace',
        'backslashreplace',
        'surrogateescape',
        'xmlcharrefreplace',
        'namereplace',
        'surrogatepass',
        'whatever',
    )

    def test_encode(self) -> None:
        for char, encoded_char in self.__class__.CHAR_ENCODED_CHAR_PAIRS:
            with self.subTest("Encode '{!r}' to '{!r}'".format(char, encoded_char)):

                self.assertEqual(
                    ErikaCodec('test').encode(char),
                    (encoded_char, len(encoded_char))
                )

    def test_decode(self) -> None:
        for char, encoded_char in self.__class__.CHAR_ENCODED_CHAR_PAIRS:
            with self.subTest("Decode '{!r}' to '{!r}'".format(encoded_char, char)):

                self.assertEqual(
                    ErikaCodec('test').decode(encoded_char),
                    (char, len(char))
                )

    def test_encode_with_missing_encoding_mapping(self) -> None:
        chars = [
            '\u0001',
            'd',
            '\U0010FFFE',
        ]

        for char in chars:
            with self.subTest("Decode '{!r}' which is missing from encoding map".format(char)):
                self.assertRaisesRegex(
                    UnicodeEncodeError,
                    (
                        r"^'ErikaCodec' codec can't encode character .*? in position 0: "
                        r"Character not found in encoding map\.$"
                    ),
                    ErikaCodec('test').encode,
                    char
                )

    def test_decode_with_missing_decoding_mapping(self) -> None:
        chars = [
            b'\x01',
            b'UUUU',
            b'deadbeef',
            b'ada',
        ]

        for char in chars:
            with self.subTest("Decode '{!r}' which is missing from encoding map".format(char)):
                self.assertRaisesRegex(
                    UnicodeDecodeError,
                    (
                        r"^'ErikaCodec' codec can't decode byte .*? in position [01]: "
                        r"Byte pattern not found in decoding map\.$"
                    ),
                    ErikaCodec('test').decode,
                    char
                )

    def test_encode_with_unsupported_error_handler(self) -> None:
        for error_handler in self.__class__.UNSUPPORTED_ERROR_HANDLERS:
            with self.subTest("Call ErikaCodec.encode with '{}' error handler".format(error_handler)):
                self.assertRaisesRegex(
                    ValueError,
                    r"ErikaCodec\.encode does not support any error handlers other than 'strict'\.",
                    ErikaCodec('test').encode,
                    self.__class__.CHAR_ENCODED_CHAR_PAIRS[0][0],
                    error_handler
                )

    def test_decode_with_unsupported_error_handler(self) -> None:
        for error_handler in self.__class__.UNSUPPORTED_ERROR_HANDLERS:
            with self.subTest("Call ErikaCodec.decode with '{}' error handler".format(error_handler)):
                self.assertRaisesRegex(
                    ValueError,
                    r"ErikaCodec\.decode does not support any error handlers other than 'strict'\.",
                    ErikaCodec('test').decode,
                    self.__class__.CHAR_ENCODED_CHAR_PAIRS[3][1],
                    error_handler
                )
