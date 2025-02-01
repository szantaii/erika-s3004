from pathlib import Path
import serial
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.automaton import ErikaAutomaton  # noqa: E402


class ErikaAutomatonTest(TestCase):
    @patch('time.sleep')
    @patch('serial.serial_for_url', spec=serial.serial_for_url)
    def test_draw_generations(self, *_: MagicMock) -> None:
        initial_states = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        automaton = ErikaAutomaton('does not matter', 54, language='test', initial_states=initial_states)

        self.assertListEqual(automaton._current_states, initial_states)

        automaton.draw_generations(1)

        self.assertListEqual(automaton._current_states, [0, 0, 0, 1, 1, 1, 0, 0, 0])

        automaton.draw_generations(1)

        self.assertListEqual(automaton._current_states, [0, 0, 1, 0, 0, 0, 1, 0, 0])

        automaton.draw_generations(1)

        self.assertListEqual(automaton._current_states, [0, 1, 1, 1, 0, 1, 1, 1, 0])

        automaton.draw_generations(1)

        self.assertListEqual(automaton._current_states, [1, 0, 0, 0, 1, 0, 0, 0, 1])
