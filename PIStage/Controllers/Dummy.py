__author__ = 'sei'

from PIStage._base import Controller
import time

class Dummy(Controller):

    def __init__(self, port=None):
        self._x = 10
        self._y = 10
        self._z = 10
        print('Dummy initialized')

    def pos(self):
        time.sleep(0.05)
        return self._x,self._y,self._z

    def moveabs(self, x=None, y=None, z=None):
        if x is not None: self._x = x
        if y is not None: self._y = y
        if z is not None: self._z = z
        time.sleep(0.05)

    def moverel(self, dx=None, dy=None, dz=None):
        if dx is not None: self._x += dx
        if dy is not None: self._y += dy
        if dz is not None: self._z += dz
        time.sleep(0.05)

    def home(self):
        self._x = 10
        self._y = 10
        self._z = 10
        time.sleep(0.05)
