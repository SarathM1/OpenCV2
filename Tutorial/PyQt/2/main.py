import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from test_ui import Ui_Form

class Gui(QMainWindow):
	def __init__(self,parent=None):
		QWidget.__init__(self,parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.ui.button.clicked.connect(self.button_clicked)

	def button_clicked(self):
		self.ui.lineEdit.setText("Hello World")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Gui()
	form.show()
	sys.exit(app.exec_())
		