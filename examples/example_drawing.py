import os
from pathlib import Path
import subprocess
import sys
import tempfile


sys.path.insert(-1, Path(__file__).parent.parent.as_posix())


from erika.cli import ErikaCli  # noqa: E402
from erika.drawing import ErikaDrawing  # noqa: E402


if __name__ == '__main__':
    cli_args = ErikaCli().parse_args()

    fd, example_image_path = tempfile.mkstemp(suffix='.png', prefix='imagemagick_logo_')
    os.close(fd)

    magick_process = subprocess.Popen(
        ['magick', 'logo:', example_image_path],
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    _, stderr = magick_process.communicate()

    if magick_process.returncode != 0:
        raise RuntimeError(stderr)

    try:
        with ErikaDrawing(**cli_args) as tw:
            tw.draw_image(example_image_path)
    except KeyboardInterrupt:
        pass
    finally:
        os.remove(example_image_path)
