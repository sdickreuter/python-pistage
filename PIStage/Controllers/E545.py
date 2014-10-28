__author__ = 'sei'

import time

from PIStage._base import Controller


class E545(Controller):
    def __init__(self):
        super(E545, self).__init__()

        self._sock.send('ONL 1 1 2 1 3 1\n')
        self._sock.send('SVO A 1 B 1 C 1\n')
        self._sock.send('DCO A 1 B 1 C 1\n')

        print('E545 initialized')
        print('All Channels in Online Mode, Servo Control on, Drift Compensation on')

        self.moveabs(10, 10, 10)

        self._x, self._y, self._z = self.query_pos()

        print('Position: ' + str(self._x) + " " + str(self._y) + " " + str(self._z))

    def query_pos(self):
        self._lock.acquire()
        try:
            self._sock.send('POS?\n')
            pos = self._sock.recv(self._buffer_size)
            # self._sock.send("ERR?\n")
            # print self._sock.recv(self._buffer_size)
        except:
            self._sock.close()
            pos = None
            RuntimeError('Lost Connection to Controller')
        self._lock.release()
        pos = pos.split("\n")
        self._x = float(pos[0][2:12])
        self._y = float(pos[1][2:12])
        self._z = float(pos[2][2:12])
        return self._x, self._y, self._z

    def moveabs(self, x=None, y=None, z=None):
        com = 'MOV '
        if x is not None:
            if (x > 0) & (x < 200):
                com += 'A ' + str(round(x, 4))
                self._x = x
        if y is not None:
            if (y > 0) & (y < 200):
                if len(com) > 4:
                    com += ' '
                com += 'B ' + str(round(y, 4))
                self._y = y
        if z is not None:
            if (z > 0) & (z < 200):
                if len(com) > 4:
                    com += ' '
                com += 'C ' + str(round(z, 4))
                self._z = z
        if len(com) > 4:
            self._lock.acquire()
            try:
                self._sock.send(com + "\n")
            except:
                self._sock.close()
                RuntimeError('Lost Connection to Controller')
            self._lock.release()

    def moverel(self, dx=None, dy=None, dz=None):
        com = 'MVR '
        if dx is not None:
            if ((self._x + dx) > 0) & ((self._x + dx) < 200):
                com += 'A ' + str(round(dx, 4))
                self._x += dx
        if dy is not None:
            if ((self._y + dy) > 0) & ((self._y + dy) < 200):
                if len(com) > 4:
                    com += ' '
                com += 'B ' + str(round(dy, 4))
                self._y += dy
        if dz is not None:
            if ((self._z + dz) > 0) & ((self._z + dz) < 200):
                if len(com) > 4:
                    com += ' '
                com += 'C ' + str(round(dz, 4))
                self._z += dz

        if len(com) > 4:
            self._lock.acquire()
            try:
                self._sock.send(com + "\n")
            except:
                self._sock.close()
                RuntimeError('Lost Connection to Controller')
            self._lock.release()


    def home(self):
        """
        homes all axes of the stage

        :return: returns counter values after homing
        """
        self._lock.acquire()
        try:
            self._sock.send('GOH\n')
            self._x, self._y, self._z = self.query_pos()
        except:
            self._sock.close()
            RuntimeError('Lost Connection to Controller')
        self._lock.release()
