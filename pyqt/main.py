from PyQt4 import QtGui, QtCore
from PyQt4.Qt import Qt
from dip import openCV
from flags import Flags
from py_file import Ui_MainWindow
import cv2
import sys


class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flags = Flags(self.ui)
        self.video = openCV(cv2.VideoCapture(0), self.flags)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(20)
        self.update()

    def play(self):
        # try:
        self.video.captureNextFrame()
        self.ui.videoFrame.setPixmap(self.video.convertFrame())
        self.ui.videoFrame.setScaledContents(True)
        self.flags.checkFlags()
        # except Exception, e:
        #   print "play(): ", e

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        self.key = QtCore.QString()
        if Qt.Key_A <= event.key() <= Qt.Key_Z:
            self.key = event.text()
        self.flags.isLatch_button = True
        self.key = event.text()
        self.ui.latch.setStyleSheet('background-color :rgbrgb(0, 131,  0);')

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        self.flags.isLatch_button = False
        self.ui.latch.setStyleSheet('background-color :rgb(190, 56, 56) ;')


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
