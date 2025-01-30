from pathlib import Path
import sys
from types import MappingProxyType
from unittest import TestCase


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.control import ErikaControl, get_control_values  # noqa: E402


class ErikaControlTest(TestCase):
    CONTROL_FIELDS = MappingProxyType(
        {
            'HALF_STEP_UP': b'v',
            'HALF_STEP_DOWN': b'u',
            'HALF_STEP_LEFT': b't',
            'HALF_STEP_RIGHT': b's',
            'MICRO_STEP_UP': b'\x82',
            'MICRO_STEP_DOWN': b'\x81',
            'MICRO_STEP_LEFT_RIGHT': b'\xa5',
            'PRINTER_READY': b'\x96',
            'NO_CGE_ADVANCE': b'\xa9',
        }
    )

    def test_control_fields(self) -> None:
        self.assertListEqual(
            list(ErikaControl.__dict__['__annotations__'].keys()),
            list(self.__class__.CONTROL_FIELDS.keys())
        )
        self.assertListEqual(
            list(ErikaControl.__dict__['__dataclass_fields__'].keys()),
            list(self.__class__.CONTROL_FIELDS.keys())
        )
        self.assertListEqual(
            list(ErikaControl.__dict__['__match_args__']),
            list(self.__class__.CONTROL_FIELDS.keys())
        )

    def test_get_control_values(self) -> None:
        control_values = get_control_values()

        self.assertIsInstance(control_values, ErikaControl)
        self.assertDictEqual(
            control_values.__dict__,
            dict(self.__class__.CONTROL_FIELDS)
        )
