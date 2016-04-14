import socket   # for sockets
import sys  # for exit

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2.0)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
host = '192.168.1.12'
port = 8888

try:
    while True:
        msg = raw_input('Enter message to send : ')
        try:
            s.sendto(msg, (host, port))
            if msg == 'q':
                print "Raising KeyboardInterrupt"
                raise KeyboardInterrupt
            # Set the whole string
            # receive data from client (data, addr)
            d = s.recvfrom(1024)

            reply = d[0]
            addr = d[1]

            print 'Server reply : ' + reply
        except socket.timeout, e:
            print "Socket timeout"

        except socket.error, msg:
            print "Socket Error"
            print 'Error Code : ', msg
            s.close()
            sys.exit()
        except KeyboardInterrupt, e:
            print "Ctr + C ==> Quiting"
            s.close()
            sys.exit()
except KeyboardInterrupt, e:
    print "Ctr + C ==> Quiting"
    s.close()
    sys.exit()
