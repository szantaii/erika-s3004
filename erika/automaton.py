from .erika import Erika
import random
from typing import Optional


class ErikaAutomaton(Erika):
    MAX_CHAR_WIDTH = 62
    MAX_PIXEL_WIDTH = 256
    MICRO_STEP_PER_DOT = 3
    ALIVE_CELL_CHAR = 'o'

    def __init__(
        self,
        device: str,
        rule: int,
        language: str = 'hu-HU',
        initial_states: Optional[list[int]] = None,
        draw_as_image: bool = False
    ) -> None:
        super().__init__(device, language=language)

        tmp_rule = rule % (2 ** 8)

        self._rule: list[int] = []
        self._rule.append((0b10000000 & tmp_rule) >> 7)
        self._rule.append((0b01000000 & tmp_rule) >> 6)
        self._rule.append((0b00100000 & tmp_rule) >> 5)
        self._rule.append((0b00010000 & tmp_rule) >> 4)
        self._rule.append((0b00001000 & tmp_rule) >> 3)
        self._rule.append((0b00000100 & tmp_rule) >> 2)
        self._rule.append((0b00000010 & tmp_rule) >> 1)
        self._rule.append((0b00000001 & tmp_rule))

        self._draw_as_image: bool = draw_as_image

        if self._draw_as_image:
            self._alive_cell: bytes = self._control.NO_CGE_ADVANCE \
                + '.'.encode(encoding=self._encoding_name)
        else:
            self._alive_cell: bytes = self._control.NO_CGE_ADVANCE \
                + self.__class__.ALIVE_CELL_CHAR.encode(encoding=self._encoding_name)

        self._max_width: int = self.__class__.MAX_CHAR_WIDTH

        if self._draw_as_image:
            self._max_width = self.__class__.MAX_PIXEL_WIDTH

        if initial_states is None:
            self._previous_states: list[int] = [random.randint(0, 1) for _ in range(self._max_width)]
        else:
            self._previous_states: list[int] = [cell % 2 for cell in initial_states[:self._max_width]]

        self._current_states: list[int] = self._previous_states[:]

    def _next_generation(self) -> None:
        for i in range(len(self._current_states)):
            if i == 0:
                previous_left = self._previous_states[-1]
                previous_right = self._previous_states[i + 1]
            elif i == len(self._current_states) - 1:
                previous_left = self._previous_states[i - 1]
                previous_right = self._previous_states[0]
            else:
                previous_left = self._previous_states[i - 1]
                previous_right = self._previous_states[i + 1]

            previous_center = self._previous_states[i]

            self._current_states[i] = self._rule[
                len(self._rule) - 1 - (previous_left << 2 | previous_center << 1 | previous_right)
            ]

        self._previous_states = self._current_states[:]

    def _move_to_new_line(self) -> None:
        self.write_string('\r')

        if self._draw_as_image:
            self.micro_step_down(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)

            return

        self.write_string('\n')

    def _print_current_generation(self) -> None:
        continuous_dead_cells = 0

        for i, cell in enumerate(self._current_states):
            if set(self._current_states[i:]) == {0}:
                break

            if cell == 0:
                continuous_dead_cells += 1

                continue

            if self._draw_as_image:
                self.micro_step_right(
                    micro_step_count=continuous_dead_cells * self.__class__.MICRO_STEP_PER_DOT
                )
            else:
                self.write_string(' ' * continuous_dead_cells)

            continuous_dead_cells = 0

            self.write_bytes(self._alive_cell)

            if self._draw_as_image:
                self.micro_step_right(micro_step_count=self.__class__.MICRO_STEP_PER_DOT)
            else:
                self.write_string(' ')

        self._move_to_new_line()

    def print_automaton(self, step_count: int) -> None:
        for _ in range(step_count):
            self._print_current_generation()
            self._next_generation()
