__author__ = 'sei'

from PIStage._base import Controller

class E545(Controller):

    def __init__(self, port=None):
        super(E545, self).__init__(self)

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
        self._x, self._y, self._z = x, y, z
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
