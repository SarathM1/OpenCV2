import socket
import sys
import RPi.GPIO as g

R1 = 3
R2 = 5
R3 = 7
R4 = 11

class Server():
    g.setmode(g.BOARD)
    HOST = '192.168.1.12'
    PORT = 8888  # Arbitrary non-privileged port
    # Datagram (udp) socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed !! Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    def __init__(self):
        # Bind socket to local host and port
        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
    
        print 'Socket bind complete'
        self.gpio_init()
    
    def gpio_init(self):
        g.setup(R1, g.OUT)
        g.setup(R2, g.OUT)
        g.setup(R3, g.OUT)
        g.setup(R4, g.OUT)
    
    def relaysOff(self):
        g.output(R1, 0)
        g.output(R2, 0)
        g.output(R3, 0)
        g.output(R4, 0)

    def run(self):
        # now keep talking with the client
        while 1:
         # receive data from client (data, addr)
            d = self.s.recvfrom(1024)
            data = d[0]
            addr = d[1]
        
            if data == 'q':
                print "Breaking"
                break
            else:
                print len(data),
            
            if data.isalpha():
                print data
            else:
                self.relaysOff()
                if data == '1':
                    print "Relay 1"
                    g.output(R1,1)
                elif data == '2':
                    print "Relay 2"
                    g.output(R2,1)
                elif data == '3':
                    print "Relay 3"
                    g.output(R3,1)
                elif data == '4':
                    print "Relay 4"
                    g.output(R4,1)

            reply = 'OK...' + data
            self.s.sendto(reply, addr)
            print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
        
        self.s.close()

if __name__ == '__main__':
    obj = Server()
    try:
        obj.run()
    finally:
        print "\n\tQuitting"
        obj.s.close()
        g.cleanup()
