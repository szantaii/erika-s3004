from erika.automaton import ErikaAutomaton
import random


# states = [0] * 33
# states[16] = 1
#
# with ErikaAutomaton('/dev/ttyUSB0', 99, initial_states=states) as tw:
#     tw.print_automaton(33)

states = [0] * ErikaAutomaton.MAX_PIXEL_WIDTH
states[(ErikaAutomaton.MAX_PIXEL_WIDTH // 2) - 1] = 1

with ErikaAutomaton(
    device='/dev/ttyUSB0',
    rule=18,
    initial_states=states,
    draw_as_image=True
) as tw:
    tw.print_automaton(ErikaAutomaton.MAX_PIXEL_WIDTH)
