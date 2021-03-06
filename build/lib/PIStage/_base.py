__author__ = 'sei'

import socket
import time
import sys
import multiprocessing

class Controller(object):
    def __init__(self, ip=None, port=None):
        self._lock = multiprocessing.Lock()
        self._x = multiprocessing.Value('d', 0.)
        self._y = multiprocessing.Value('d', 0.)
        self._z = multiprocessing.Value('d', 0.)
        self._ID = None
        self._sock = None
        self._buffer_size = 1024
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
            print(self._sock.recv(self._buffer_size))
        except:
            self._sock.close()
            RuntimeError('Could not connect to Controller')
        self._lock.release()

        print('Successfully connected')

    def __del__(self):
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

    def query_pos(self):
        pass

    def moveabs(self, x=None, y=None, z=None):
        pass

    def moverel(self, dx=None, dy=None, dz=None):
        pass

    def home(self):
        pass

    def last_pos(self):
        return self._x.value, self._y.value, self._z.value
