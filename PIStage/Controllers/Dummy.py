__author__ = 'sei'

from PIStage._base import Controller
import time

class Dummy(Controller):

    def __init__(self, port=None):
        self._x = 10.0
        self._y = 10.0
        self._z = 10.0
        print('Dummy initialized')

    def pos(self):
        time.sleep(0.05)
        return self._x,self._y,self._z

    def moveabs(self, x=None, y=None, z=None):
        if x is not None: self._x = round(x,4)
        if y is not None: self._y = round(y,4)
        if z is not None: self._z = round(z,4)
        time.sleep(0.05)

    def moverel(self, dx=None, dy=None, dz=None):
        if dx is not None: self._x += round(dx,4)
        if dy is not None: self._y += round(dy,4)
        if dz is not None: self._z += round(dz,4)
        time.sleep(0.05)

    def home(self):
        self._x = 10.0
        self._y = 10.0
        self._z = 10.0
        time.sleep(0.05)
