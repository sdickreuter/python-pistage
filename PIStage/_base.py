__author__ = 'sei'

import socket
import time
import sys
import _defines as d

class Controller(object):
    _x = 0
    _y = 0
    _z = 0
    _ip = None
    _port = None
    _ID = None
    _sock = None
    _buffer_size = 1024

    def _findController(self):

        def recv_timeout(the_socket,timeout=2):
            #make socket non blocking
            the_socket.setblocking(0)

            #total data partwise in an array
            total_data=[];
            data='';

            addr = None
            #beginning time
            begin=time.time()
            while 1:
                #if you got some data, then break after timeout
                if total_data and time.time()-begin > timeout:
                    break

                #if you got no data at all, wait a little longer, twice the timeout
                elif time.time()-begin > timeout*2:
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

            if addr is not None : print addr
            #join all parts to make final string
            return (addr,''.join(total_data))

        message = 'PI'
        multicast_group = ('<broadcast>', 50000)

        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))
        sock.settimeout(2)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            # Send data to the multicast group
            print 'Searching for Controller'
            sent = sock.sendto(message, multicast_group)
        except socket.error:
            #Send failed
            print 'Send failed'
            sys.exit()

        #get reply and print
        addr, data = recv_timeout(sock)
        print 'found Controller' + data + ' at ' + addr[0]
        #Close the socket
        sock.close()
        return addr[0], addr[1], data

    def __init__(self):
        self._ip, self._port, self._ID = self._findController()

        print 'Trying to connect to Controller...'

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._ip, self._port))
            self._sock.send('POS?\n')
            data = self._sock.recv(self._buffer_size)
        except:
            RuntimeError('Could not connect to Controller')

        print 'Successfully connected'

    def __del__(self):
        self._sock.close()

    def pos(self):
        pass

    def moveabs(self, x=None, y=None, z=None):
        pass

    def moverel(self, dx=None, dy=None, dz=None):
        pass

    def home(self):
        pass
