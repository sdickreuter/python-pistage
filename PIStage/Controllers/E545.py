__author__ = 'sei'

from PIStage._base import Controller

class E545(Controller):

    def __init__(self, port=None):
        super(E545, self).__init__()

        self._sock.send('ONL 1 1 2 1 3 1\n')
        self._sock.send('SVO A 1 B 1 C 1\n')
        self._sock.send('DCO A 1 B 1 C 1\n')

        print('E545 initialized')
        print('All Channels in Online Mode, Servo Control on, Drift Compensation on')

        self.moveabs(10,10,10)

        _x, _y, _z = self.pos()

        print('Position: ' + str(_x) +" " + str(_y) + " " + str(_z))

    def pos(self):
        try:
            self._sock.send('POS?\n')
            pos = self._sock.recv(self._buffer_size)
        except:
            self._sock.close()
            RuntimeError('Lost Connection to Controller')
        pos = pos.split("\n")
        x = float(pos[0][2:12])
        y = float(pos[1][2:12])
        z = float(pos[2][2:12])
        self._x, self._y, self._z = x, y, z
        return x, y, z

    def moveabs(self, x=None, y=None, z=None):
        com = 'MOV '
        if x is not None:
            if (x > 0) & (x < 200) :
                com += 'A '+str(round(x,4))
                self._x = x
        if y is not None:
            if (y > 0) & (y < 200) :
                if len(com) > 4: com+= ' '
                com += 'B '+str(round(y,4))
                self._y = y
        if z is not None:
            if (z > 0) & (z < 200) :
                if len(com) > 4: com+= ' '
                com += 'C '+str(round(z,4))
                self._z = z
        print(com)
        if len(com) > 4:
            try:
                self._sock.send(com+"\n")
            except:
                self._sock.close()
                RuntimeError('Lost Connection to Controller')


    def moverel(self, dx=None, dy=None, dz=None):
        com = 'MVR '
        if dx is not None:
            if ((self._x+dx) > 0) & ((self._x+dx) < 200) :
                com += 'A '+str(round(dx,4))
                self._x += dx
        if dy is not None:
            if ((self._y+dy) > 0) & ((self._y+dy) < 200) :
                if len(com) > 4: com+= ' '
                com += 'B '+str(round(dy,4))
                self._y += dy
        if dz is not None:
            if ((self._z+dz) > 0) & ((self._z+dz) < 200) :
                if len(com) > 4: com+= ' '
                com += 'C '+str(round(dz,4))
                self._z += dz

        if len(com) > 4:
            try:
                self._sock.send(com+"\n")
            except:
                self._sock.close()
                RuntimeError('Lost Connection to Controller')

    def home(self):
        """
        homes all axes of the stage

        :return: returns counter values after homing
        """
        try:
            self._sock.send('GOH\n')
        except:
            self._sock.close()
            RuntimeError('Lost Connection to Controller')
