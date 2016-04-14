from PyQt4.QtGui import QMessageBox
import socket
import vlc
import sys  # for exit

host = '192.168.1.12'
port = 8888

CSS_RED = 'background-color :rgb(190, 56, 56) ;'
CSS_GREEN = 'background-color :rgb(0, 131, 0) ;'


class Flags():

    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()

    cmd = 's'
    isSet_prev = False
    isSet_cur = False
    isSet_button = False
    isLatch_button = False
    cmd_latch = 's'
    prev_cmd = 's'
    fingers = 1
    prev_fing = 0
    fing_latch = 0

    def __init__(self, ui):
        self.ui = ui
        
        # create dgram udp socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.settimeout(1.0)
        except socket.error:
            QMessageBox.warning(self.ui.widget, "Socket Error", 'Failed to create socket')
            sys.exit()

    def closeSocket(self):
        self.s.close()
        print "\nQuitting App!!\n"

    def checkFlags(self):
        if self.isSet_button:
            self.fing_latch = 0         # Resetting fing_latch
            self.fingers = 1
            self.ui.mode.setText("Robot")
            if str(self.ui.cmd.text()).isdigit():
                self.ui.cmd.clear()

            if self.isLatch_button:
                self.disable_arrows()
                self.ui.mode.setStyleSheet(CSS_GREEN)

                if self.cmd == 'f':
                    self.ui.up_arrow.setEnabled(True)
                elif self.cmd == 'b':
                    self.ui.down_arrow.setEnabled(True)
                elif self.cmd == 'l':
                    self.ui.left_arrow.setEnabled(True)
                elif self.cmd == 'r':
                    self.ui.right_arrow.setEnabled(True)
                elif self.cmd == 's':
                    self.ui.cmd.setText('s')
                    self.ui.mode.setStyleSheet(CSS_RED)

                self.cmd_latch = self.cmd
            else:
                self.cmd = self.cmd_latch

        else:
            self.cmd = 's'
            self.cmd_latch = self.cmd
            self.disable_arrows()
            self.ui.mode.setText("Relay")
            if str(self.ui.cmd.text()).isalpha():
                self.ui.cmd.clear()
            if self.fingers == self.prev_fing:
                if self.fing_latch == 10:             # Reduce bouncing
                    self.playAudio(str(self.fingers))
                    # print self.fing_latch,"\tFingers = ",self.fingers

                self.fing_latch += 1
            else:
                self.fing_latch = 0

            self.prev_fing = self.fingers

        if self.prev_cmd != self.cmd:
            self.playAudio(self.cmd)
            self.prev_cmd = self.cmd

        if self.isSet_prev is False and self.isSet_cur is True:
            self.isSet_button = not self.isSet_button

    def disable_arrows(self):
        self.ui.up_arrow.setEnabled(False)
        self.ui.down_arrow.setEnabled(False)
        self.ui.left_arrow.setEnabled(False)
        self.ui.right_arrow.setEnabled(False)

    def sock_send(self, cmd):
        try:
            self.s.sendto(cmd, (host, port))
            d = self.s.recvfrom(1024)

            reply = d[0]
            addr = d[1]
            self.ui.echo.setText(reply)
        except socket.timeout, e:
            self.ui.echo.setText("TIME!!")
            print "Socket timeout"

        except socket.error, msg:
            print "Socket Error"
            print 'Error Code : ', msg
            self.s.close()

    def playAudio(self, cmd):
        
        if cmd.isalpha():
            self.ui.cmd.setText(str(cmd))
            media = self.vlc_instance.media_new('./Sounds/'+cmd+'.mp3')
            self.player.set_media(media)
            self.player.play()
            self.sock_send(cmd)
        elif int(cmd) < 6 and int(cmd) > 0:
            self.ui.cmd.setText(str(cmd))
            media = self.vlc_instance.media_new('./Sounds/'+cmd+'.mp3')
            self.player.set_media(media)
            self.player.play()
            self.sock_send(cmd)
        else:
            self.ui.cmd.clear()
