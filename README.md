# erika-s3004

## Contents

* [About](#about)
* [License](#license)
* [Hardware setup](#hardware-setup)
  * [Erika connector](#erika-connector)
  * [USB to TTL adapter](#usb-to-ttl-adapter)
  * [Connecting the typewriter to USB to TTL adapter](#connecting-the-typewriter-to-usb-to-ttl-adapter)
* [Software](#software)
  * [Prerequisites](#prerequisites)
  * [Character encoding](#character-encoding)
  * [Typewriter control](#typewriter-control)
  * [Tests](#tests)
* [Examples](#examples)
  * [Simple example](#simple-example)
  * [Reading from the typewriter](#reading-from-the-typewriter)
  * [Paper and typewriter carriage movement](#paper-and-typewriter-carriage-movement)
  * [Elementary cellular automaton](#elementary-cellular-automaton)
  * [Drawing images](#drawing-images)
* [Resources](#resources)

## About

This project provides a Python library and some documentation how to connect an [Erika S3004 electronic typewriter][erika_3004_electronic_typewriters_by_year_then_serial_number_on_the_typewriter_database] to a PC and use it as a printer or as an input device.

The project is structured in the following directories:

| Directory                    | Description                                                                          |
|------------------------------|--------------------------------------------------------------------------------------|
| __[`doc`](./doc)__           | Directory containing images for this README.                                         |
| __[`erika`](./erika)__       | `erika` Python library for communicating with the Erika S3004 electronic typewriter. |
| __[`examples`](./examples)__ | Example scripts how-to use the `erika` library.                                      |
| __[`test`](./test)__         | Tests for the `erika` library.                                                       |

## License

This project is licensed under the MIT license. For the full license, please see [`LICENSE`](./LICENSE).

## Hardware setup

This section describes how to connect the Erika S3004 electronic typewriter to a PC.

### Erika connector

The Erika S3004 electronic typewriter has a connector on its right side towards the front which can be used to connect it to a computer. This serial interface made it possible to use the Erika S3004 electronic typewriter as an input (keyboard) or output (printer) device.

The Erika S3004 electronic typewriter is connected via a serial connection. See the following (rudimentary) connector schematic and the explaining table below.

```
                                                                           +-------- RX
                                                                           |
                                                                           |  +----- RTS
                                                                           |  |
                                                                           |  |  +-- GND
                                                                           |  |  |
                                                                           v  v  v
   +--------------------------------------------------------------------------------+
   |                                                                                |
A1 |  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  | A13
   |                                                                                |
B1 |  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  O  | B13
   |                                                                                |
   +--------------------------------------------------------------------------------+
                                                                           ^  ^  ^
                                                                           |  |  |
                                                                           |  |  +-- TX
                                                                           |  |
                                                                           |  +----- +5V
                                                                           |
                                                                           +-------- DTD
```

| Connector pin | Function |
|---------------|----------|
| `A11`         | `RX`     |
| `A12`         | `RTS`    |
| `A13`         | `GND`    |
| `B11`         | `DTD`    |
| `B12`         | `+5V`    |
| `B13`         | `TX`     |

The Erika S3004 electronic typewriter is equipped with a 26-pin connector. Two serial data lines (RxD and TxD) and two signal lines (RTS and DTD) are used for connection. Ground and +5V are also provided. The figure and table above shows the connector pin assignments.

(Only the six listed pins are used on the 26-pin connector the other twenty pins are not used.)

For further details on the 26-pin connector, see [Erika S 3004 [Homecomputer DDR]][erika_s_3004_homecomputer_ddr] and other links at [Resources](#resources).

### USB to TTL adapter

To be able to connect a PC to the Erika S3004 electronic typewriter you will need an USB to TTL adapter with CTS (clear to send) and RTS (ready to receive) signal lines. Such USB adapters with FT232 or CH343 chips are usually have the required signal lines.

### Connecting the typewriter to USB to TTL adapter

Connect your USB to TTL adapter pins to the Erika S3004 electronic typewriter's connector pins according to the table below. For further details of the Erika S3004 electronic typewriter connector see [Erika connector](#erika-connector).

| USB to TTL adapter pin | Erika connector pin (function) |
|------------------------|--------------------------------|
| `TX`                   | `A11` (`RX`)                   |
| `CTS`                  | `A12` (`RTS`)                  |
| `GND`                  | `A13` (`GND`)                  |
| `RTS`                  | `B11` (`DTD`)                  |
| `+5V`                  | `B12` (`+5V`)                  |
| `RX`                   | `B13` (`TX`)                   |

## Software

This section describes the prerequisites for using this software along with some technical details about the character encoding and control codes of the Erika S3004 electronic typewriter.

### Prerequisites

The following software is required for the Python library:

* __[pySerial][pyserial]:__ pySerial is a Python serial port access library.
* __[ImageMagick][imagemagick]:__ ImageMagick is a free, open-source software suite, used for editing and manipulating digital images.

Please note that ImageMagick is only necessary if you would like to [print images](#drawing-images) with your Erika S3004 electronic typewriter.

### Character encoding

To send data to or read data (text) from the Erika S3004 electronic typewriter data is needed to be encoded or decoded. The [`char_data.json`](erika/char_data.json) file in the [`erika`](./erika) directory contains all language specific and control data necessary for encoding and decoding. Language specific data is stored in Unicode escaped character and Base64 encoded byte pairs.

Since I only have Erika S3004 electronic typewriters with Hungarian keyboard layouts, the only language specified in the mentioned [`char_data.json`](erika/char_data.json) file is Hungarian (`hu-HU`). The following table contains all Hungarian characters and their encoded bytes for the Erika S3004 electronic typewriter.

One could ask, why are there different character encodings for different languages? Since different languages use different letters, the [daisy wheel][daisy_wheel_printing_wikipedia] in the typewriter is different for each language with different layouts resulting in different encoded character codes. You can make your own encoding map by using [one of the example programs](#reading-from-the-typewriter) and extending the [`char_data.json`](erika/char_data.json) file.

| Character | Erika encoded character \[byte\] | Description                                       |
|-----------|----------------------------------|---------------------------------------------------|
| `\u0008`  | `0x72`                           | Backspace (U+0008)                                |
| `\u0009`  | `0x79`                           | Character tabulation (U+0009)                     |
| `\u000A`  | `0x77`                           | Line feed (lf) (U+000A)                           |
| `\u000D`  | `0x78`                           | Carriage return (cr) (U+000D)                     |
| `\u0020`  | `0x71`                           | Space (U+0020)                                    |
| `!`       | `0x3D`                           |                                                   |
| `"`       | `0x3F`                           |                                                   |
| `%`       | `0x33`                           |                                                   |
| `&`       | `0x0C`                           |                                                   |
| `'`       | `0x0F`                           |                                                   |
| `(`       | `0x3B`                           |                                                   |
| `)`       | `0x39`                           |                                                   |
| `+`       | `0x1B`                           |                                                   |
| `,`       | `0x63`                           |                                                   |
| `-`       | `0x62`                           |                                                   |
| `.`       | `0x64`                           |                                                   |
| `/`       | `0x35`                           |                                                   |
| `0`       | `0x65`                           |                                                   |
| `1`       | `0x2F`                           |                                                   |
| `2`       | `0x2D`                           |                                                   |
| `3`       | `0x2B`                           |                                                   |
| `4`       | `0x29`                           |                                                   |
| `5`       | `0x27`                           |                                                   |
| `6`       | `0x25`                           |                                                   |
| `7`       | `0x23`                           |                                                   |
| `8`       | `0x21`                           |                                                   |
| `9`       | `0x1F`                           |                                                   |
| `:`       | `0x02`                           |                                                   |
| `;`       | `0x0D`                           |                                                   |
| `=`       | `0x1A`                           |                                                   |
| `?`       | `0x37`                           |                                                   |
| `A`       | `0x2C`                           |                                                   |
| `B`       | `0x22`                           |                                                   |
| `C`       | `0x24`                           |                                                   |
| `D`       | `0x26`                           |                                                   |
| `E`       | `0x46`                           |                                                   |
| `F`       | `0x44`                           |                                                   |
| `G`       | `0x2A`                           |                                                   |
| `H`       | `0x28`                           |                                                   |
| `I`       | `0x41`                           |                                                   |
| `J`       | `0x20`                           |                                                   |
| `K`       | `0x42`                           |                                                   |
| `L`       | `0x1E`                           |                                                   |
| `M`       | `0x38`                           |                                                   |
| `N`       | `0x36`                           |                                                   |
| `O`       | `0x2E`                           |                                                   |
| `P`       | `0x45`                           |                                                   |
| `Q`       | `0x34`                           |                                                   |
| `R`       | `0x1C`                           |                                                   |
| `S`       | `0x43`                           |                                                   |
| `T`       | `0x32`                           |                                                   |
| `U`       | `0x30`                           |                                                   |
| `V`       | `0x3E`                           |                                                   |
| `W`       | `0x40`                           |                                                   |
| `X`       | `0x3A`                           |                                                   |
| `Y`       | `0x3C`                           |                                                   |
| `Z`       | `0x47`                           |                                                   |
| `_`       | `0x01`                           |                                                   |
| `a`       | `0x51`                           |                                                   |
| `b`       | `0x48`                           |                                                   |
| `c`       | `0x54`                           |                                                   |
| `d`       | `0x55`                           |                                                   |
| `e`       | `0x52`                           |                                                   |
| `f`       | `0x5E`                           |                                                   |
| `g`       | `0x4F`                           |                                                   |
| `h`       | `0x5B`                           |                                                   |
| `i`       | `0x56`                           |                                                   |
| `j`       | `0x5C`                           |                                                   |
| `k`       | `0x53`                           |                                                   |
| `l`       | `0x58`                           |                                                   |
| `m`       | `0x5D`                           |                                                   |
| `n`       | `0x4D`                           |                                                   |
| `o`       | `0x4C`                           |                                                   |
| `p`       | `0x59`                           |                                                   |
| `q`       | `0x57`                           |                                                   |
| `r`       | `0x50`                           |                                                   |
| `s`       | `0x5A`                           |                                                   |
| `t`       | `0x4E`                           |                                                   |
| `u`       | `0x4B`                           |                                                   |
| `v`       | `0x4A`                           |                                                   |
| `w`       | `0x5F`                           |                                                   |
| `x`       | `0x49`                           |                                                   |
| `y`       | `0x61`                           |                                                   |
| `z`       | `0x60`                           |                                                   |
| `\u00C1`  | `0x0E`                           | Latin capital letter a with acute (U+00C1)        |
| `\u00C9`  | `0x03`                           | Latin capital letter e with acute (U+00C9)        |
| `\u00CD`  | `0x11`                           | Latin capital letter i with acute (U+00CD)        |
| `\u00D3`  | `0x13`                           | Latin capital letter o with acute (U+00D3)        |
| `\u00D6`  | `0x0B`                           | Latin capital letter o with diaeresis (U+00D6)    |
| `\u0150`  | `0x15`                           | Latin capital letter o with double acute (U+0150) |
| `\u00DA`  | `0x06`                           | Latin capital letter u with acute (U+00DA)        |
| `\u00DC`  | `0x04`                           | Latin capital letter u with diaeresis (U+00DC)    |
| `\u0170`  | `0x08`                           | Latin capital letter u with double acute (U+0170) |
| `\u00E1`  | `0x16`                           | Latin small letter a with acute (U+00E1)          |
| `\u00E4`  | `0x0A`                           | Latin small letter a with diaeresis (U+00E4)      |
| `\u00E9`  | `0x17`                           | Latin small letter e with acute (U+00E9)          |
| `\u00ED`  | `0x19`                           | Latin small letter i with acute (U+00ED)          |
| `\u00F3`  | `0x05`                           | Latin small letter o with acute (U+00F3)          |
| `\u00F6`  | `0x09`                           | Latin small letter o with diaeresis (U+00F6)      |
| `\u0151`  | `0x07`                           | Latin small letter o with double acute (U+0151)   |
| `\u00FA`  | `0x18`                           | Latin small letter u with acute (U+00FA)          |
| `\u00FC`  | `0x12`                           | Latin small letter u with diaeresis (U+00FC)      |
| `\u0171`  | `0x14`                           | Latin small letter u with double acute (U+0171)   |

### Typewriter control

Similarly to [character encoding and decoding](#character-encoding), some typewriter control codes are also stored in the [`char_data.json`](erika/char_data.json) file in the [`erika`](./erika) directory.

Control codes are stored in the mentioned [`char_data.json`](erika/char_data.json) file under `control` in function and erika encoded byte pairs.

The following table below contains all used typewriter control codes used in this project.

| Erika encoded character \[byte\] | Function                                                               | Note                                                                                                                                                       |
|----------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `0x76`                           | Move the paper upwards by half a line                                  | Half step up                                                                                                                                               |
| `0x75`                           | Move the paper downwards by half a line                                | Half step down                                                                                                                                             |
| `0x74`                           | Move the carriage half a character to the left                         | Half-backspace                                                                                                                                             |
| `0x73`                           | Move the carriage half a character to the right                        | Half-space                                                                                                                                                 |
| `0x82`                           | Move the paper upwards by &sup1;&frasl;&#8322;&#8320; of a line feed   | Micro step up                                                                                                                                              |
| `0x81`                           | Move the paper downwards by &sup1;&frasl;&#8322;&#8320; of a line feed | Micro step down                                                                                                                                            |
| `0xA5`                           | Direct carriage control                                                | The subsequent byte specifies the number of micro steps: 0&ndash;127 steps forwards; 256&#8239;-&#8239;\[1&ndash;127\] steps backwards                     |
| `0x96`                           | Printer ready                                                          | RTS line will only be activated again when the character is printed                                                                                        |
| `0xA9`                           | No line feed                                                           | The character following this code is printed without the carriage advancing, making it possible to print on the same spot without moving back the carriage |

For the complete list of control codes for the Erika S3004 electronic typewriter please see [Erika S 3004 [Homecomputer DDR]][erika_s_3004_homecomputer_ddr], [practic 3/89, S. 135-137 [Homecomputer DDR]][practic_3_89_s_135_137_homecomputer_ddr], [Z1013.de practic 3/89 - Vom Bausatz zum PC - Mikrorechnerbausatz robotron Z1013][z1013_de_practic_3_89_vom_bausatz_zum_pc_mikrorechnerbausatz_robotron_z1013] and other links under [Resources](#resources).

### Tests

To run tests run the [`test_runner.py`](test/test_runner.py) in the [`test`](./test) directory:

```sh
python3 test/test_runner.py
```

## Examples

This section describes some example programs included in this project.

Do not forget to load paper into your Erika S3004 electronic typewriter before running any of the examples below!

### Simple example

This simple example program shows how to use the main [`Erika` class](./erika/erika.py#L10-L175) to interact with the typewriter.

To run this example program, invoke it the following way, just make sure you use the proper device (it is usually `/dev/ttyUSB[0-9]` or `/dev/ttyACM[0-9]`). (This applies to all subsequent example programs.)

```sh
python3 examples/example_simple.py --device /dev/ttyUSB0
```

You can specify to use a different character encoding than the default Hungarian by specifying the `-l` or `--language` command-line parameter and the language code used in the [`char_data.json`](erika/char_data.json) file. (This applies to all subsequent example programs.)

Please note that this project only includes the default Hungarian character encoding/decoding data, for further details please see [Character encoding](#character-encoding).

```sh
python3 examples/example_simple.py --device /dev/ttyUSB0 --language en-US
```

See the printed result of this example program below.

![](doc/example_simple.png)

### Reading from the typewriter

This example program showcases how to read from the typewriter. You will be prompted to type a single character at a time and this example will print the encoded character code to the screen in hexadecimal format:

```console
$ sudo python3 examples/example_read.py --device /dev/ttyUSB0
Type 'a' or SPACE if not applicable: 0x51
Type 'b' or SPACE if not applicable: 0x48
Type 'c' or SPACE if not applicable: 0x54
Type 'd' or SPACE if not applicable: 0x55
⋮
Type '5' or SPACE if not applicable: 0x27
Type '6' or SPACE if not applicable: 0x25
Type '7' or SPACE if not applicable: 0x23
Type '8' or SPACE if not applicable: 0x21
Type '9' or SPACE if not applicable: 0x1F
Type ENTER: 0x77
Type SPACE: 0x71
Type '.' (FULL STOP) or SPACE if not applicable: 0x64
Type '!' (EXCLAMATION MARK) or SPACE if not applicable: 0x3D
Type '?' (QUESTION MARK) or SPACE if not applicable: 0x37
Type ',' (COMMA) or SPACE if not applicable: 0x63
Type ':' (COLON) or SPACE if not applicable: 0x02
Type '-' (HYPHEN-MINUS) or SPACE if not applicable: 0x62
Type ENTER: 0x77
```

To run this example program, invoke it the following way.

```sh
python3 examples/example_read.py --device /dev/ttyUSB0
```

### Paper and typewriter carriage movement

This example program shows how to programatically move the carriage and the paper left, right, up and down in smaller and larger steps to get some funky looking text and even shapes.

To run this example program, invoke it the following way.

```sh
python3 examples/example_movement.py --device /dev/ttyUSB0
```

See the printed result of this example program below.

![](doc/example_movement.png)

### Elementary cellular automaton

This example shows how to print an [elementary cellular automaton][elementary_cellular_automaton_wolfram_mathworld] using the [`ErikaAutomaton` class](./erika/automaton.py#L6-L85).

To run this example program, invoke it the following way.

```sh
python3 examples/example_automaton.py --device /dev/ttyUSB0
```

See the printed result of this example program below.

![](doc/example_automaton.png)

### Drawing images

This example example will print (or rather draw) [ImageMagick's built-in logo image][imagemagick_builtin_logo] using the [`ErikaDrawing` class](./erika/drawing.py#L5-L131).

Please note that printing or drawing images may take a toll on your typewriter's ribbon. If you would like to kind of see what an image would look like printed using the [`ErikaDrawing` class](./erika/drawing.py#L5-L131), you can use the following chained-command to check it without wasting precious ribbon and time.

```sh
preview_img_path='/tmp/preview.pgm' \
    && magick                       \
        /path/to/your/img.file      \
        -geometry '256x>'           \
        -colorspace Gray            \
        -ordered-dither o2x2        \
        "pgm:${preview_img_path}"   \
    && xdg-open                     \
        "${preview_img_path}"
```

To run this example program, invoke it the following way.

```sh
python3 examples/example_drawing.py --device /dev/ttyUSB0
```

See the printed result of this example program below.

![](doc/example_drawing.png)

## Resources

* [Erika 3004 electronic Typewriters by Year then Serial Number on the Typewriter Database][erika_3004_electronic_typewriters_by_year_then_serial_number_on_the_typewriter_database]
* [Chaostreff-Potsdam/erika3004][chaostreff_potsdam_erika3004]
* [Chaostreff-Potsdam/erika-docs][chaostreff_potsdam_erika_docs]
* [jbb/erika_S3004][jbb_erika_S3004]
* [Erika S 3004 [Homecomputer DDR]][erika_s_3004_homecomputer_ddr] ([archive.org copy][erika_s_3004_homecomputer_ddr_archive_org])
* [practic 3/89, S. 135-137 [Homecomputer DDR]][practic_3_89_s_135_137_homecomputer_ddr] ([archive.org copy][practic_3_89_s_135_137_homecomputer_ddr_archive_org])
* [Informationen zur Modellreihe Erika electronic 30xx][informationen_zur_modellreihe_erika_electronic_30xx] ([archive.org copy][informationen_zur_modellreihe_erika_electronic_30xx_archive_org])
* [KC85 Drucker - Der KC85/4 System Aufbau Bedienung][kc85_drucker_der_kc85_4_system_aufbau_bedienung]
* [Z1013.de practic 3/89 - Vom Bausatz zum PC - Mikrorechnerbausatz robotron Z1013][z1013_de_practic_3_89_vom_bausatz_zum_pc_mikrorechnerbausatz_robotron_z1013] ([archive.org copy][z1013_de_practic_3_89_vom_bausatz_zum_pc_mikrorechnerbausatz_robotron_z1013_archive_org])

[erika_3004_electronic_typewriters_by_year_then_serial_number_on_the_typewriter_database]: https://typewriterdatabase.com/Erika.3004+electronic.242.bmys
[chaostreff_potsdam_erika3004]: https://github.com/Chaostreff-Potsdam/erika3004
[chaostreff_potsdam_erika_docs]: https://github.com/Chaostreff-Potsdam/erika-docs
[jbb_erika_S3004]: https://codeberg.org/jbb/erika_S3004
[erika_s_3004_homecomputer_ddr]: https://hc-ddr.hucki.net/wiki/doku.php/z9001/erweiterungen/s3004
[erika_s_3004_homecomputer_ddr_archive_org]: https://web.archive.org/web/20250215162723/https://hc-ddr.hucki.net/wiki/doku.php/z9001/erweiterungen/s3004
[practic_3_89_s_135_137_homecomputer_ddr]: https://hc-ddr.hucki.net/wiki/doku.php/z1013/literatur/practic-89-3-1
[practic_3_89_s_135_137_homecomputer_ddr_archive_org]: https://web.archive.org/web/20250215162540/https://hc-ddr.hucki.net/wiki/doku.php/z1013/literatur/practic-89-3-1
[informationen_zur_modellreihe_erika_electronic_30xx]: https://erika-electronic.de/
[informationen_zur_modellreihe_erika_electronic_30xx_archive_org]: https://web.archive.org/web/20250211180518/https://erika-electronic.de/
[kc85_drucker_der_kc85_4_system_aufbau_bedienung]: http://www.mpm-kc85.de/html/Drucker.htm
[z1013_de_practic_3_89_vom_bausatz_zum_pc_mikrorechnerbausatz_robotron_z1013]: http://www.z1013.de/artikel/prac8903/practic8903_135.html
[z1013_de_practic_3_89_vom_bausatz_zum_pc_mikrorechnerbausatz_robotron_z1013_archive_org]: https://web.archive.org/web/20240225040036/http://z1013.de/artikel/prac8903/practic8903_135.html
[imagemagick]: https://imagemagick.org/
[imagemagick_builtin_logo]: https://www.imagemagick.org/script/formats.php#builtin-images
[pyserial]: https://github.com/pyserial/pyserial
[daisy_wheel_printing_wikipedia]: https://en.wikipedia.org/wiki/Daisy_wheel_printing
[elementary_cellular_automaton_wolfram_mathworld]: https://mathworld.wolfram.com/ElementaryCellularAutomaton.html
