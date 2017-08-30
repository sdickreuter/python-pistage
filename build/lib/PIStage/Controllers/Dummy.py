__author__ = 'sei'

import time
import multiprocessing

from PIStage._base import Controller


class Dummy(Controller):
    def __init__(self):
        self._lock = multiprocessing.Lock()
        self._x = multiprocessing.Value('d', 10.)
        self._y = multiprocessing.Value('d', 10.)
        self._z = multiprocessing.Value('d', 10.)
        #pos_manager = multiprocessing.Manager()
        #pos = pos_manager.dict()
        #pos['x'] = 10.0
        #pos['y'] = 10.0
        #pos['z'] = 10.0
        print('PIStage Dummy initialized')

    def query_pos(self):
        self._lock.acquire()
        time.sleep(0.05)
        self._lock.release()
        return self._x.value, self._y.value, self._z.value

    def moveabs(self, x=None, y=None, z=None):
        self._lock.acquire()
        if x is not None:
            self._x.value = round(x, 4)
        if y is not None:
            self._y.value = round(y, 4)
        if z is not None:
            self._z.value = round(z, 4)
        time.sleep(0.05)
        self._lock.release()

    def moverel(self, dx=None, dy=None, dz=None):
        self._lock.acquire()
        if dx is not None:
            self._x.value += round(dx, 4)
        if dy is not None:
            self._y.value += round(dy, 4)
        if dz is not None:
            self._z.value += round(dz, 4)
        time.sleep(0.05)
        self._lock.release()

    def home(self):
        self._lock.acquire()
        self._x.value = 10.0
        self._y.value = 10.0
        self._z.value = 10.0
        time.sleep(0.05)
        self._lock.release()

    def __del__(self):
        pass