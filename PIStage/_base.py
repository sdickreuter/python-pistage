__author__ = 'sei'

import serial
import time
import sys
import _defines as d

class PIStage(object):
    _x = 0
    _y = 0
    _z = 0
    _serial = None

    def __init__(self, port=None):
        try:
            if port is None:
                self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, timeout=0.1)
            else:
                self._serial = serial.Serial(port, d.DEFAULT_BAUDRATE, timeout=1)
        except:
            self._serial.close()
            raise RuntimeError('Could not open serial connection')

        if self._serial is None:
            raise RuntimeError('Could not open serial connection')

        self._serial.write('ONL 1 1 2 1 3 1\r')
        self._serial.write('SVO A 1 B 1 C 1\r')
        self._serial.write('DCO A 1 B 1 C 1\r')

        print('NanoControl initialized on port %s' %self._serial.name)
        print('All Channels in Online Mode, Servo Control on, Drift Compensation on')

        _x, _y, _z = self.pos()

        print('Position: ' + str(_x) +" " + str(_y) + " " + str(_z))

    def pos(self):
        self._serial.write('POS?\r')
        pos = self._serial.readlines()
        x = float(pos[0][2:12])
        y = float(pos[1][2:12])
        z = float(pos[2][2:12])
        return x, y, z

    def moveabs(self, x=None, y=None, z=None):
        com = 'MOV '
        if x is not None:
            com += 'A '+x
        if y is not None:
            com += 'B '+y
        if z is not None:
            com += 'C '+z

        if len(com) > 4:
            self._serial.write(com+"\r")

    def moverel(self, dx=None, dy=None, dz=None):
        com = 'MVR '
        if dx is not None:
            com += 'A '+dx
        if dy is not None:
            com += 'B '+dy
        if dz is not None:
            com += 'C '+dz

        if len(com) > 4:
            self._serial.write(com+"\r")

    def home(self):
        """
        homes all axes of the stage

        :return: returns counter values after homing
        """
        self._serial.write('GOH\r')



class PIStage_Dummy(object):
    _x = 0
    _y = 0

    def __init__(self, port=None):
        pass

    def _read_return_status(self):
        time.sleep(0.05)
        return 'o\r'

    def _coarse(self, channel, steps):
        time.sleep(0.05)
        return 0

    def _get_coarse_counter(self, channel):
        time.sleep(0.05)
        return 0

    def _coarse_reset(self):
        time.sleep(0.05)
        return 0

    def _fine(self, channel, steps):
        time.sleep(0.05)
        return 0

    def _get_fine_counter(self):
        time.sleep(0.05)
        return 0

    def _relax(self):
        time.sleep(0.05)
        return 0

    def _moveabs(self, x=None, y=None, channel=None, pos=None):
        time.sleep(0.05)
        return 0

    def _moverel(self, dx=None, dy=None):
        time.sleep(0.05)
        return 0

    def _counterread(self):
        time.sleep(0.05)
        return (0,0)

    def _counterreset(self):
        time.sleep(0.05)
        return 0

    def home(self):
        time.sleep(0.05)
        return 0
