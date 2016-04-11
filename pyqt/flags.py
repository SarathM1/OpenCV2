from PyQt4.QtGui import QMessageBox
import serial
import vlc

CSS_RED = 'background-color :rgb(190, 56, 56) ;'
CSS_GREEN = 'background-color :rgb(0, 131, 0) ;'


class Flags():

    vlc_instance = vlc.Instance()                                                                                                  
    player = vlc_instance.media_player_new()

    robot_cmd = 's'
    isSet_prev = False
    isSet_cur = False
    isSet_button = False
    isLatch_button = False
    cmd_latch = 's'
    prev_comnd = 's'
    fingers = 1
    prev_fing = 0
    fing_latch = 0

    def __init__(self, ui):
        self.ui = ui
        try:
            self.ser = serial.Serial('/dev/ttyUSB0')
        except Exception, e:
            QMessageBox.warning(self.ui.widget, "Xbee Error", str(e))
            print e

    def checkFlags(self):
        if self.isSet_button:
            self.fing_latch = 0         # Resetting fing_latch
            self.fingers = 1
            self.ui.mode.setStyleSheet(CSS_GREEN)
            self.ui.mode.setText("Robot")

            if self.isLatch_button:
                self.disable_arrows()
                cmd = self.robot_cmd
                if self.robot_cmd == 'f':
                    self.ui.up_arrow.setEnabled(True)
                
                elif self.robot_cmd == 'b':
                    self.ui.down_arrow.setEnabled(True)
                    
                elif self.robot_cmd == 'l':
                    self.ui.left_arrow.setEnabled(True)
                    
                elif self.robot_cmd == 'r':
                    self.ui.right_arrow.setEnabled(True)
                
                self.cmd_latch = cmd
            else:
                cmd = self.cmd_latch

        else:
            cmd = 's'
            self.cmd_latch = cmd
            self.robot_cmd = 's' 
            self.disable_arrows()
            self.ui.mode.setText("Relay")
            if self.fingers == self.prev_fing:
                if self.fing_latch == 10 and self.fingers!=1:             # Reduce bouncing
                    self.playAudio(str(self.fingers))
                    #print self.fing_latch,"\tFingers = ",self.fingers

                self.fing_latch += 1
            else:
                self.fing_latch = 0

            self.prev_fing = self.fingers

        self.cur_comnd = cmd

        if self.prev_comnd != self.cur_comnd:
            self.playAudio(cmd)
            try:
                self.ser.write(cmd)
            except:
                pass

            self.prev_comnd = self.cur_comnd

        if self.isSet_prev is False and self.isSet_cur is True:
            self.isSet_button = not self.isSet_button

    def disable_arrows(self):
        self.ui.up_arrow.setEnabled(False)
        self.ui.down_arrow.setEnabled(False)
        self.ui.left_arrow.setEnabled(False)
        self.ui.right_arrow.setEnabled(False)
        self.ui.mode.setStyleSheet(CSS_RED)

    def playAudio(self, cmd):
        if cmd.isalpha():
            self.ui.cmd.setText(str(cmd))
            media = self.vlc_instance.media_new('./Sounds/'+cmd+'.mp3')
            self.player.set_media(media)                                                                
            self.player.play()
        elif int(cmd) < 6:
            self.ui.cmd.setText(str(cmd))
            media = self.vlc_instance.media_new('./Sounds/'+cmd+'.mp3')
            self.player.set_media(media)                                                                                               
            self.player.play() 
        else:
            self.ui.cmd.clear()
 
