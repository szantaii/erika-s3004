import erika

typewriter = erika.Erika('/dev/ttyUSB0')
typewriter.connect()
typewriter.write_string("Hello\n\tWorld!\n\n\n")
typewriter.disconnect()
