from pathlib import Path
import sys


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.cli import ErikaCli  # noqa: E402
from erika.erika import Erika  # noqa: E402


if __name__ == '__main__':
    cli_args = ErikaCli().parse_args()

    # Example with context manager
    #
    # Note that there is no need to manually call connect
    # and disconnect as the enter and exit functions of
    # the context manager will take care of those
    with Erika(**cli_args) as typewriter:
        typewriter.write_string('Hello\n\tWorld!\n\n')

    # Example with calling connect() and disconnect() directly
    typewriter = Erika(cli_args['device'])

    typewriter.connect()

    typewriter.write_string(
        """You can also use the typewriter instance
\twithout a context manager but then you
\t    have to manually call connect and
disconnect when you want to start and stop
using the typewriter.

"""
    )

    for i in range(5):
        if i > 0:
            typewriter.half_step_down()
            typewriter.half_step_right(half_step_count=i)

        typewriter.write_string('Happy Hacking!\r')

    typewriter.write_string('\n' * 5)

    typewriter.disconnect()
