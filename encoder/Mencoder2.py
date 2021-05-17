#!/usr/bin/env python

# read_RPM.py
# 2016-01-20
# Public Domain

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html

class Encoder2:
    """
    A class to read speedometer pulses and calculate the RPM.
    """
    def __init__(self, pi, gpio, pulses_per_rev=20.0):
        """
        Instantiate with the Pi and gpio of the RPM signal
        to monitor.

        Optionally the number of pulses for a complete revolution
        may be specified.  It defaults to 1.

        Optionally a weighting may be specified.  This is a number
        between 0 and 1 and indicates how much the old reading
        affects the new reading.  It defaults to 0 which means
        the old reading has no effect.  This may be used to
        smooth the data.

        Optionally the minimum RPM may be specified.  This is a
        number between 1 and 1000.  It defaults to 5.  An RPM
        less than the minimum RPM returns 0.0.
        """
        self.pi = pi
        self.gpio = gpio
        self.pulses_per_rev = pulses_per_rev

        self._high_tick = None
        self._period = None

        pi.set_mode(gpio, pigpio.INPUT)

        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

    def _cbf(self, gpio, level, tick):

        if gpio == 5: # Rising edge.
            print(self._high_tick)
            if self._high_tick is not None:
                t = pigpio.tickDiff(self._high_tick, tick)

                if self._period is not None:
                    self._period = self._period + t
                else:
                    self._period = t

            self._high_tick = tick

    def RPM(self):
        """
        Returns the RPM.
        """
        RPM = 0.0
        print(self._period)
        if self._period is not None:
            RPM = 60000000.0 / (self._period * self.pulses_per_rev)
            #if RPM < self.min_RPM:
            #    RPM = 0.0

        return RPM

if __name__ == "__main__":

    import time
    import pigpio

    gpioPin = 5
    RUN_TIME = 60.0
    SAMPLE_TIME = 1.0

    pi = pigpio.pi()

    p = Encoder2(pi, gpioPin)

    start = time.time()

    while (time.time() - start) < RUN_TIME:

        time.sleep(SAMPLE_TIME)

        RPM = p.RPM()

        print("RPM={}".format(RPM))

    pi.stop()
