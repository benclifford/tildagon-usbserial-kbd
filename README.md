read stuff off the usb serial line (the thing `mpremote` or `minicom`
connects to on your laptop) and turn it into tildagon keyboard input.

that way you can use your laptop as a cheap/expensive substitute for
the 2026 tildagon keyboard hexpansion.

keys that work:
  lowercase letters
  numbers
  symbols
  arrows
  enter

keys that are weird:
  tab on the keyboard is escape on the tildagon (button F) - this is because it's hard for me to detect ESC.

other keys:
  perhaps in future releases!

if you can figure out how to reconfigure the serial port onto hexpansion
pins and have the right level shifter, you can probably use this to
use a real TTY as input.
