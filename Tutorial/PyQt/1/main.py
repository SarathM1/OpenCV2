from ui import Ui_Form
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Gui(QMainWindow):
	def __init__(self,parent = None):
		QWidget.__init__(self,parent)

		self.ui = Ui_Form()
		self.ui.setupUi(self)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Gui()
	form.show()
	sys.exit(app.exec_())
