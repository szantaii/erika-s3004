from erika.erika import Erika


# with Erika('/dev/ttyUSB0') as tw:
#     tw.write_string('+\b')
#     tw.step_right(10)
#     tw.write_string('+\b')
#     tw.step_down(10)
#     tw.write_string('+\b')
#     tw.step_left(10)
#     tw.write_string('+\b')
#     tw.step_up(10)


# with Erika('/dev/ttyUSB0') as tw:
#     micro_space_step_step = 10
#     max_micro_space_step = micro_space_step_step * 21
#     padding_size = len(str(max_micro_space_step))
#
#     for i in range(0, max_micro_space_step, micro_space_step_step):
#         tw.write_string('\n{}: .\b'.format(str(i).rjust(padding_size)))
#         tw.micro_step_right(i)
#         tw.write_string('.\b')

with Erika('/dev/ttyACM0') as tw:
    tw.write_string('\n')

    for i in range(0, 21, 1):
        tw.write_string('.\b')
        tw.micro_step_down(i)
        tw.write_string('.\b')
        tw.micro_step_up(i)
        tw.step_right(2)
