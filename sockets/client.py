import socket   # for sockets
import sys  # for exit

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = '192.168.1.7'
port = 8888

while True:
    msg = raw_input('Enter message to send : ')
    try:
        # Set the whole string
        s.sendto(msg, (host, port))
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print 'Server reply : ' + reply
    except socket.error, msg:
        print "Socket Error"
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        s.close()
        sys.exit()
    except KeyboardInterrupt, e:
        print "Ctr + C ==> Quiting"
        s.close()
        sys.exit()
