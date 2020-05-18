# pyGCodeLoader
Python GCode Loader

Inspired by https://github.com/bborncr/gcodesender.py and https://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/

Requirements

apt install python3 python3-serial

Allows the user to load gcode as a path to a file or to add it as an argument with a separator.
If no gcode argument or file is provided the user will be asked to type it in the script.

An argument can be added to enable an infinite loop until exit is typed.
This should allow a user to create a screen and send commands from a different script"PHP".

Commands

python3 pyGCodeLoader.py --help

usage: pyGCodeLoader.py [-h] [-p PORT] [-pb PORTBAUD] [-f FILE] [-c CODE]
                        [-w WAIT] [-s SLEEP] [-l LOG] [-inf INFLOOP]
                        [-debug DEBUG]

pyGCodeLoader

optional arguments:
  -h, --help            show this help message and exit

  -p PORT, --port PORT  TTY/COM port path in '' if folders have spaces

  -pb PORTBAUD, --portbaud PORT Baud rate

  -f FILE, --file FILE  Gcode file path in '' if folders have spaces

  -c CODE, --code CODE  Gcode string separated by <> enclosed in ''

  -w WAIT, --wait WAIT  Wait for a value="ok" to get returned before sending next line

  -s SLEEP, --sleep SLEEP Sleep time = float = 0.001 between each command sent

  -l LOG, --log LOG     Append Log file path in '' if folders have spaces

  -inf INFLOOP, --infloop INFLOOP Infinite loop with manual code add until exit is typed = enable

  -debug DEBUG, --debug DEBUG Disable Writing to port and disable -w --wait function as no return will be available = enable

Example

python3 pyGCodeLoader.py -p /dev/serial0 -pb 115200

python3 pyGCodeLoader.py -p /dev/serial0 -pb 115200 -c 'G28<>G1 X0 Y0<>M18'

python3 pyGCodeLoader.py -p /dev/serial0 -pb 115200 -f /media/file/gcode.gcode

Screen Example

# Run pyGCodeLoader as Daemon

# OPEN A SCREEN

screen -dmS 3DPRINTER1

# START pyGCodeLoader IN THE SCREEN

screen -S 3DPRINTER1 -X stuff "python3 pyGCodeLoader.py -p /dev/serial0 -pb 115200 -inf enable^M"

# SEND COMMANDS TO SCREEN

screen -S 3DPRINTER1 -X stuff "G28<>G1 X100 Y100^M" # Send a command


