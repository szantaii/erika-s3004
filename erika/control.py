import base64
import dataclasses
import json
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class ErikaControl:
    HALF_STEP_UP: bytes
    HALF_STEP_DOWN: bytes
    HALF_STEP_LEFT: bytes
    HALF_STEP_RIGHT: bytes
    MICRO_STEP_UP: bytes
    MICRO_STEP_DOWN: bytes
    MICRO_STEP_LEFT_RIGHT: bytes
    PRINTER_READY: bytes
    NO_CGE_ADVANCE: bytes


def get_control_values() -> ErikaControl:
    with open(Path(__file__).parent.joinpath('char_data.json')) as char_data_file:
        raw_control_data = json.load(char_data_file)['control']

    control_map = { k: base64.b64decode(v) for k, v in raw_control_data.items() }

    return ErikaControl(**control_map)
