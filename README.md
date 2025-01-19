# erika-s3004

## Contents

* [About](#about)
* [License](#license)
* [Hardware setup](#hardware-setup)
  * [Erika connector](#erika-connector)
* [Software](#software)
* [Resources](#resources)

## About

__TODO__

## License

__TODO__

## Hardware setup

__TODO__

### Erika connector

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

| Connector | Function |
| --------- | -------- |
| `A11`     | `RX`     |
| `A12`     | `RTS`    |
| `A13`     | `GND`    |
| `B11`     | `DTD`    |
| `B12`     | `+5V`    |
| `B13`     | `TX`     |

### USB to TTL adapter

Is this necessary?

### Connecting the typewriter to USB to TTL adapter

| USB to TTL adapter pin | Erika connector pin (function) |
| ---------------------- | ------------------------------ |
| `TX`                   | `A11` (`RX`)                   |
| `CTS`                  | `A12` (`RTS`)                  |
| `GND`                  | `A13` (`GND`)                  |
| `RTS`                  | `B11` (`DTD`)                  |
| `+5V`                  | `B12` (`+5V`)                  |
| `RX`                   | `B13` (`TX`)                   |

## Software

__TODO__

## Character encoding and typewriter control

| Character | Erika encoded character [byte] | Description                                       |
| --------- | ------------------------------ | ------------------------------------------------- |
| `\u0008`  | `0x72`                         | Backspace (U+0008)                                |
| `\u0009`  | `0x79`                         | Character tabulation (U+0009)                     |
| `\u000A`  | `0x77`                         | Line feed (lf) (U+000A)                           |
| `\u000D`  | `0x78`                         | Carriage return (cr) (U+000D)                     |
| `\u0020`  | `0x71`                         | Space (U+0020)                                    |
| `!`       | `0x3D`                         |                                                   |
| `"`       | `0x3F`                         |                                                   |
| `%`       | `0x33`                         |                                                   |
| `&`       | `0x0C`                         |                                                   |
| `'`       | `0x0F`                         |                                                   |
| `(`       | `0x3B`                         |                                                   |
| `)`       | `0x39`                         |                                                   |
| `+`       | `0x1B`                         |                                                   |
| `,`       | `0x63`                         |                                                   |
| `-`       | `0x62`                         |                                                   |
| `.`       | `0x64`                         |                                                   |
| `/`       | `0x35`                         |                                                   |
| `0`       | `0x65`                         |                                                   |
| `1`       | `0x2F`                         |                                                   |
| `2`       | `0x2D`                         |                                                   |
| `3`       | `0x2B`                         |                                                   |
| `4`       | `0x29`                         |                                                   |
| `5`       | `0x27`                         |                                                   |
| `6`       | `0x25`                         |                                                   |
| `7`       | `0x23`                         |                                                   |
| `8`       | `0x21`                         |                                                   |
| `9`       | `0x1F`                         |                                                   |
| `:`       | `0x02`                         |                                                   |
| `;`       | `0x0D`                         |                                                   |
| `=`       | `0x1A`                         |                                                   |
| `?`       | `0x37`                         |                                                   |
| `A`       | `0x2C`                         |                                                   |
| `B`       | `0x22`                         |                                                   |
| `C`       | `0x24`                         |                                                   |
| `D`       | `0x26`                         |                                                   |
| `E`       | `0x46`                         |                                                   |
| `F`       | `0x44`                         |                                                   |
| `G`       | `0x2A`                         |                                                   |
| `H`       | `0x28`                         |                                                   |
| `I`       | `0x41`                         |                                                   |
| `J`       | `0x20`                         |                                                   |
| `K`       | `0x42`                         |                                                   |
| `L`       | `0x1E`                         |                                                   |
| `M`       | `0x38`                         |                                                   |
| `N`       | `0x36`                         |                                                   |
| `O`       | `0x2E`                         |                                                   |
| `P`       | `0x45`                         |                                                   |
| `Q`       | `0x34`                         |                                                   |
| `R`       | `0x1C`                         |                                                   |
| `S`       | `0x43`                         |                                                   |
| `T`       | `0x32`                         |                                                   |
| `U`       | `0x30`                         |                                                   |
| `V`       | `0x3E`                         |                                                   |
| `W`       | `0x40`                         |                                                   |
| `X`       | `0x3A`                         |                                                   |
| `Y`       | `0x3C`                         |                                                   |
| `Z`       | `0x47`                         |                                                   |
| `_`       | `0x01`                         |                                                   |
| `a`       | `0x51`                         |                                                   |
| `b`       | `0x48`                         |                                                   |
| `c`       | `0x54`                         |                                                   |
| `d`       | `0x55`                         |                                                   |
| `e`       | `0x52`                         |                                                   |
| `f`       | `0x5E`                         |                                                   |
| `g`       | `0x4F`                         |                                                   |
| `h`       | `0x5B`                         |                                                   |
| `i`       | `0x56`                         |                                                   |
| `j`       | `0x5C`                         |                                                   |
| `k`       | `0x53`                         |                                                   |
| `l`       | `0x58`                         |                                                   |
| `m`       | `0x5D`                         |                                                   |
| `n`       | `0x4D`                         |                                                   |
| `o`       | `0x4C`                         |                                                   |
| `p`       | `0x59`                         |                                                   |
| `q`       | `0x57`                         |                                                   |
| `r`       | `0x50`                         |                                                   |
| `s`       | `0x5A`                         |                                                   |
| `t`       | `0x4E`                         |                                                   |
| `u`       | `0x4B`                         |                                                   |
| `v`       | `0x4A`                         |                                                   |
| `w`       | `0x5F`                         |                                                   |
| `x`       | `0x49`                         |                                                   |
| `y`       | `0x61`                         |                                                   |
| `z`       | `0x60`                         |                                                   |
| `\u00C1`  | `0x0E`                         | Latin capital letter a with acute (U+00C1)        |
| `\u00C9`  | `0x03`                         | Latin capital letter e with acute (U+00C9)        |
| `\u00CD`  | `0x11`                         | Latin capital letter i with acute (U+00CD)        |
| `\u00D3`  | `0x13`                         | Latin capital letter o with acute (U+00D3)        |
| `\u00D6`  | `0x0B`                         | Latin capital letter o with diaeresis (U+00D6)    |
| `\u0150`  | `0x15`                         | Latin capital letter o with double acute (U+0150) |
| `\u00DA`  | `0x06`                         | Latin capital letter u with acute (U+00DA)        |
| `\u00DC`  | `0x04`                         | Latin capital letter u with diaeresis (U+00DC)    |
| `\u0170`  | `0x08`                         | Latin capital letter u with double acute (U+0170) |
| `\u00E1`  | `0x16`                         | Latin small letter a with acute (U+00E1)          |
| `\u00E4`  | `0x0A`                         | Latin small letter a with diaeresis (U+00E4)      |
| `\u00E9`  | `0x17`                         | Latin small letter e with acute (U+00E9)          |
| `\u00ED`  | `0x19`                         | Latin small letter i with acute (U+00ED)          |
| `\u00F3`  | `0x05`                         | Latin small letter o with acute (U+00F3)          |
| `\u00F6`  | `0x09`                         | Latin small letter o with diaeresis (U+00F6)      |
| `\u0151`  | `0x07`                         | Latin small letter o with double acute (U+0151)   |
| `\u00FA`  | `0x18`                         | Latin small letter u with acute (U+00FA)          |
| `\u00FC`  | `0x12`                         | Latin small letter u with diaeresis (U+00FC)      |
| `\u0171`  | `0x14`                         | Latin small letter u with double acute (U+0171)   |

> 96H Drucker Fertigmeldung
>
> A0H Dauerfunktion für alle Tasten\
> A1H Übertragungsrate 10-1200 bd\
> 08-2400 bd\
> 04-4800 bd\
> 02-9600 bd\
> 01-19200 bd
>
> A3H Anschlagstärke (nächstes Zeichen ist Stärke)\
> A4H\
> A5H Tabulator (nächstes Zeichen is Schritt)\
> A6H Zeilenschaltung (nächstes Zeichen ist Schritt)\
> A7H Typenrad drehen (nächstes Zeichen ist Schritt)\
> A8H Farbbandtransport (nächstes Zeichen ist Schritt)\
> A9H kein Zeilenvorschub (Doppeldruck)\
> AAH BEL Bell (Signal nächstes Zeichen ist Signallänge)(07H;\
> ABH Tastaturabfrage\
> ACH Tastaturabfrage 2 (mit 00 Byte von Tastatur)\
> ADH entspr. der grünen REL-Funktion\
> AEH letztes Zeichen löschen\
> AFH Relocated

## Image drawing

6 &ldquo;color&rdquo; grayscale image conversion:

```
magick                                                              \
    img0023.tiff                                                    \
    -rotate '90>'                                                   \
    -geometry 128x                                                  \
    -grayscale Rec709Luma                                           \
    -dither FloydSteinberg                                          \
    -remap <(printf '%s\n' 'P2' '6 1' '255' '0 51 102 153 204 255') \
    pgm:-
```

Monochrome image conversion:

```
magick                    \
    img0023.tiff          \
    -rotate '90>'         \
    -geometry 256x        \
    -remap pattern:gray50 \
    pgm:-
```

## Resources

__TODO__
