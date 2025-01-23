from erika.erika import Erika
import time


with Erika('/dev/ttyUSB0') as tw:
    tw.write_string('\n')
    time.sleep(1)

    tw.write_string('3 micro step(s) per dot:')

    tw.write_string('\n')
    time.sleep(1)
    tw.write_string('\n')
    time.sleep(1)

    for i in range(1000):
        if i != 0 and i % 10 == 0:
            tw.micro_step_down(4)

        tw.write_string('.\b')
        tw.micro_step_right(3)
