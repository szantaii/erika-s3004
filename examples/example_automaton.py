from pathlib import Path
import sys


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.cli import ErikaCli  # noqa: E402
from erika.automaton import ErikaAutomaton  # noqa: E402


if __name__ == '__main__':
    cli_args = ErikaCli().parse_args()
    rule = 18
    initial_states = [0] * ErikaAutomaton.MAX_WIDTH
    initial_states[(ErikaAutomaton.MAX_WIDTH // 2) - 1] = 1

    with ErikaAutomaton(
        cli_args['device'],
        rule,
        language=cli_args['language'],
        initial_states=initial_states
    ) as tw:
        tw.write_string('Elementary cellular automaton with rule {}:\n\n'.format(rule))

        tw.draw_generations(ErikaAutomaton.MAX_WIDTH // 2)

        tw.write_string('\n' * 10)
