__author__ = 'sei'

import socket
import sys
import time


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
#multicast_group = ('225.255.255.255', 50000)


# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))
# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
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

print 'Message send successfully'

#get reply and print
addr, data = recv_timeout(sock)
print data
print addr
#Close the socket
sock.close()



TCP_IP = addr[0]
TCP_PORT = addr[1]
BUFFER_SIZE = 1024
MESSAGE = "POS?\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data

