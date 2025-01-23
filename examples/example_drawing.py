from erika.drawing import ErikaDrawing

with ErikaDrawing('/dev/ttyUSB0') as tw:
    tw.print_image()
