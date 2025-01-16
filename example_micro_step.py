from erika.erika import Erika

with Erika('/dev/ttyUSB0') as tw:
    tw.write_string('Horizontal micro steps:\n')

    dot = '.\b'
    max_micro_step_count = 10
    padding = len(str(max_micro_step_count))

    for i in range(max_micro_step_count + 1):
        tw.write_string('\n{}: '.format(str(i).rjust(padding)))
        tw.write_string(dot)

        if i > 0:
            tw.micro_step_right(i)
            tw.write_string(dot)

    tw.write_string('\n\nVertical micro steps:\n')

    for i in range(max_micro_step_count + 1):
        tw.write_string('\n{}: '.format(str(i).rjust(padding)))
        tw.write_string(dot)

        if i > 0:
            tw.micro_step_down(i)
            tw.write_string(dot)
