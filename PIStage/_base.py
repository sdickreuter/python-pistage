__author__ = 'sei'

import serial
import time
import sys
import _defines as d

class Controller(object):
    _x = 0
    _y = 0
    _z = 0
    _serial = None

    def __init__(self):
        try:
            self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, timeout=0.1)
        except:
            if self._serial is not None: self._serial.close()
            raise RuntimeError('Could not open serial connection')

    def pos(self):
        pass

    def moveabs(self, x=None, y=None, z=None):
        pass

    def moverel(self, dx=None, dy=None, dz=None):
        pass

    def home(self):
        pass
