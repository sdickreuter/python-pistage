__author__ = 'sei'

from PIStage._base import Controller

class E545(Controller):
    def __init__(self, ip=None, port=None, coordinate_mapping = None):
        #super(E545, self).__init__()
        super().__init__(ip=ip,port=port,coordinate_mapping=coordinate_mapping)

        self._sock.send(bytes('ONL 1 1 2 1 3 1\n','UTF-8'))
        self._sock.send(bytes('SVO A 1 B 1 C 1\n','UTF-8'))
        self._sock.send(bytes('DCO A 1 B 1 C 1\n','UTF-8'))

        print('E545 initialized')
        print('All Channels in Online Mode, Servo Control on, Drift Compensation on')

        #self.moveabs(10, 10, 10)

        self.query_pos()
        #self._x.value, self._y.value, self._z.value = self.query_pos()

        print('Position: ' + str(self._x.value) + " " + str(self._y.value) + " " + str(self._z.value))

    def query_pos(self):
        self._lock.acquire()
        try:
            self._sock.send(bytes("POS?\n",'UTF-8'))
            pos = self._sock.recv(self._buffer_size)
            # self._sock.send("ERR?\n")
            # print self._sock.recv(self._buffer_size)
        except:
            self._sock.close()
            pos = None
            RuntimeError('Lost Connection to Controller')
            return False
        pos = str(pos,'UTF-8')
        pos = pos.split("\n")
        self._lock.release()
        self._x.value,self._y.value,self._z.value = self.map_coordinates(float(pos[0][2:12]),float(pos[1][2:12]),float(pos[2][2:12]))
                #self._x.value = float(pos[0][2:12])
        #self._y.value = float(pos[1][2:12])
        #self._z.value = float(pos[2][2:12])
        #return self._x.value, self._y.value, self._z.value

    def moveabs(self, x=None, y=None, z=None):
        x,y,z = self.map_coordinates(x,y,z)
        com = 'MOV '
        if x is not None:
            if (x > 0) & (x < 200):
                com += 'A ' + str(round(x, 4))
                self._x.value = x
        if y is not None:
            if (y > 0) & (y < 200):
                if len(com) > 4:
                    com += ' '
                com += 'B ' + str(round(y, 4))
                self._y.value = y
        if z is not None:
            if (z > 0) & (z < 200):
                if len(com) > 4:
                    com += ' '
                com += 'C ' + str(round(z, 4))
                self._z.value = z
        if len(com) > 4:
            self._lock.acquire()
            try:
                self._sock.send(bytes(com + "\n",'UTF-8'))
            except:
                self._sock.close()
                RuntimeError('Lost Connection to Controller')
            self._lock.release()

    def moverel(self, dx=None, dy=None, dz=None):
        dx,dy,dz = self.map_coordinates(dx,dy,dz)
        #com = 'MVR '
        com = 'MOV '
        if dx is not None:
            if ((self._x.value + dx) > 0) & ((self._x.value + dx) < 200):
                #com += 'A ' + str(round(dx, 4))
                self._x.value += dx
                com += 'A ' + str(round(self._x.value, 4))
        if dy is not None:
            if ((self._y.value + dy) > 0) & ((self._y.value + dy) < 200):
                if len(com) > 4:
                    com += ' '
                #com += 'B ' + str(round(dy, 4))
                self._y.value += dy
                com += 'B ' + str(round(self._y.value, 4))
        if dz is not None:
            if ((self._z.value + dz) > 0) & ((self._z.value + dz) < 200):
                if len(com) > 4:
                    com += ' '
                #com += 'C ' + str(round(dz, 4))
                self._z.value += dz
                com += 'C ' + str(round(self._z.value, 4))

        if len(com) > 4:
            self._lock.acquire()
            try:
                self._sock.send(bytes(com + "\n",'UTF-8'))
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
            self._sock.send(bytes("GOH\n",'UTF-8'))
            self.query_pos()
        except:
            self._sock.close()
            RuntimeError('Lost Connection to Controller')
        self._lock.release()


# Unit test code
if __name__ == '__main__':
    stage = None

    stage = E545()
    while True:
        stage.query_pos()
        print(stage.last_pos())