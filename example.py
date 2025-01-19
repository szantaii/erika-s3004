from erika.erika import Erika


typewriter = Erika('/dev/ttyUSB0')
typewriter.connect()
typewriter.write_string("=" * 62)
typewriter.write_string('\n')
typewriter.disconnect()

with Erika('/dev/ttyUSB0') as tw:
    tw.write_string("Hello\n\tWorld!\n")
    tw.write_string("-" * 62)
    tw.write_string('\n')
