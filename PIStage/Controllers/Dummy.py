__author__ = 'sei'

import time
from billiard import Lock
import billiard

from PIStage._base import Controller


class Dummy(Controller):
    def __init__(self):
        self._lock = Lock()
        self._x = 10.0
        self._y = 10.0
        self._z = 10.0
        print('Dummy initialized')

    def pos(self):
        self._lock.acquire()
        time.sleep(0.05)
        self._lock.release()
        return self._x, self._y, self._z

    def moveabs(self, x=None, y=None, z=None):
        self._lock.acquire()
        if x is not None:
            self._x = round(x, 4)
        if y is not None:
            self._y = round(y, 4)
        if z is not None:
            self._z = round(z, 4)
        time.sleep(0.05)
        self._lock.release()

    def moverel(self, dx=None, dy=None, dz=None):
        self._lock.acquire()
        if dx is not None:
            self._x += round(dx, 4)
        if dy is not None:
            self._y += round(dy, 4)
        if dz is not None:
            self._z += round(dz, 4)
        time.sleep(0.05)
        self._lock.release()

    def home(self):
        self._lock.acquire()
        self._x = 10.0
        self._y = 10.0
        self._z = 10.0
        time.sleep(0.05)
        self._lock.release()

    def __del__(self):
        pass