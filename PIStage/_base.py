__author__ = 'sei'

import socket
import time
import sys
import multiprocessing

class Controller(object):
    def __init__(self, ip=None, port=None, coordinate_mapping = None, z_correction_angle = None):
        self.is_initialized = False
        received = None
        self._lock = multiprocessing.Lock()
        self._x = multiprocessing.Value('d', 0.)
        self._y = multiprocessing.Value('d', 0.)
        self._z = multiprocessing.Value('d', 0.)
        self._ID = None
        self._sock = None
        self._buffer_size = 1024

        # examples for coordinate_mapping:
        #  coordinate_mapping = {"x":"x","y":"y","z":"z"} will map coordinates to themselves
        #  coordinate_mapping = {"x":"z","y":"y","z":"x"} will map x to z and z to x, y stays the same
        self._coord_map = coordinate_mapping

        # z_correction_angle will move the stage also in x direction if moved in z direction
        # this compensates movement in x direction when stage is placed at an angle relativ to the objective
        if z_correction_angle is None:
            self.z_correction_angle = 0
        else:
            self.z_correction_angle = z_correction_angle


        if ip is None:
            self._ip, self._port, self._ID = self._findcontroller()
        else:
            self._ip = ip
            self._port = port

        print('Trying to connect to Controller...')

        self._lock.acquire()
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._ip, self._port))
            self._sock.send('POS?\n'.encode('UTF-8'))
            received = self._sock.recv(self._buffer_size)
            print(received)
        except:
            self._sock.close()
            RuntimeError('Could not connect to Controller')
        self._lock.release()

        if not received is None:
            print('Successfully connected to Controller')
            self.is_initialized = True
        else:
            print('Could not connect to Controller')

    def __del__(self):
        if not self._sock is None:
            if not self._sock._closed:
                self._lock.acquire()
                self._sock.close()
                self._lock.release()

    def _findcontroller(self):

        def recv_timeout(the_socket, timeout=2):
            # make socket non blocking
            the_socket.setblocking(0)

            # total data partwise in an array
            total_data = []

            addr = None
            # beginning time
            begin = time.time()
            while 1:
                # if you got some data, then break after timeout
                if total_data and time.time() - begin > timeout:
                    break

                #if you got no data at all, wait a little longer, twice the timeout
                elif time.time() - begin > timeout * 2:
                    break

                #recv something
                try:
                    data, addr = the_socket.recvfrom(8192)
                    if data:
                        total_data.append(data)
                        #change the beginning time for measurement
                        begin = time.time()
                    else:
                        #sleep for sometime to indicate a gap
                        time.sleep(0.01)
                except:
                    pass

            if addr is not None:
                print(addr)
            # join all parts to make final string
            return addr, str(total_data[0],"UTF-8")

        message = bytes('PI', 'UTF-8')
        multicast_group = (bytes('<broadcast>', 'UTF-8'), 50000)

        self._lock.acquire()
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))
        sock.settimeout(2)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            # Send data to the multicast group
            print('Searching for Controller')
            sock.sendto(message, multicast_group)
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

        # get reply and print
        addr, data = recv_timeout(sock)
        print('found Controller' + data + ' at ' + addr[0])
        # Close the socket
        sock.close()
        self._lock.release()
        return addr[0], addr[1], data

    def map_coordinates(self,x,y,z):
        if self._coord_map is not None:

            if self._coord_map["x"] == "x":
                nx = x
            elif self._coord_map["x"] == "y":
                nx = y
            elif self._coord_map["x"] == "z":
                nx = z

            if self._coord_map["y"] == "x":
                ny = x
            elif self._coord_map["y"] == "y":
                ny = y
            elif self._coord_map["y"] == "z":
                ny = z

            if self._coord_map["z"] == "x":
                nz = x
            elif self._coord_map["z"] == "y":
                nz = y
            elif self._coord_map["z"] == "z":
                nz = z

            return nx, ny, nz
        else:
            return x,y,z

    def query_pos(self):
        pass

    def moveabs(self, x=None, y=None, z=None):
        pass

    def moverel(self, dx=None, dy=None, dz=None):
        pass

    def home(self):
        pass

    def last_pos(self):
        if self._coord_map is not None:

            if self._coord_map["x"] == "x":
                nx = self._x.value
            elif self._coord_map["x"] == "y":
                nx = self._y.value
            elif self._coord_map["x"] == "z":
                nx = self._z.value

            if self._coord_map["y"] == "x":
                ny = self._x.value
            elif self._coord_map["y"] == "y":
                ny = self._y.value
            elif self._coord_map["y"] == "z":
                ny = self._z.value

            if self._coord_map["z"] == "x":
                nz = self._x.value
            elif self._coord_map["z"] == "y":
                nz = self._y.value
            elif self._coord_map["z"] == "z":
                nz = self._z.value

            return nx, ny, nz
        else:
            return self._x.value, self._y.value, self._z.value
        #return self._x.value, self._y.value, self._z.value

    def set_z_correction_angle(self,angle):
        self.z_correction_angle = angle