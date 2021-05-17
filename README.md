# encoder

Install pigpio
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install

(alternate -> sudo apt-get install pigpio python-pigpio python3-pigpio)
can check version with
pigpiod -v

sudo ./x_pigpio # check C I/F  (will not work if daemon already started. stop with sudo killall pigpiod)
sudo pigpiod    # start daemon
./x_pigpio.py   # check Python I/F to daemon

callback(user_gpio, edge, func)
Calls a user supplied function (a callback) whenever the specified GPIO edge is detected.

Parameters
user_gpio:= 0-31.
     edge:= EITHER_EDGE, RISING_EDGE (default), or FALLING_EDGE.
     func:= user supplied callback function.

The user supplied callback receives three parameters, the GPIO, the level, and the tick.
Parameter   Value    Meaning
GPIO        0-31     The GPIO which has changed state
level       0-2      0 = change to low (a falling edge)
                     1 = change to high (a rising edge)
                     2 = no level change (a watchdog timeout) Can determine when it has stopped
tick        32 bit   The number of microseconds since boot