import base64
import dataclasses
import json
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class ErikaMovement:
    STEP_UP: bytes
    STEP_DOWN: bytes
    STEP_LEFT: bytes
    STEP_RIGHT: bytes
    MICRO_STEP_UP: bytes
    MICRO_STEP_DOWN: bytes
    MICRO_STEP_LEFT_RIGHT: bytes


def get_movement_values(language: str) -> ErikaMovement:
    with open(Path(__file__).parent.joinpath('char_data.json')) as char_data_file:
        raw_movement_data = json.load(char_data_file)[language]['movement']

    movement_map = { k: base64.b64decode(v) for k, v in raw_movement_data.items() }

    return ErikaMovement(**movement_map)
