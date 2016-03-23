import serial

CSS_RED = 'background-color :rgb(190, 56, 56) ;'
CSS_GREEN = 'background-color :rgb(0,131, 0) ;'

class Flags():
	isSet_fwd = False
	isSet_back = False
	isSet_left = False
	isSet_right = False
	isSet_stop = False
	isSet_prev = False
	isSet_cur = False
	isSet_button = False
	isLatch_button = False
	cmd_latch = 's'
	prev_comnd = 's'

	def __init__(self,ui):
		self.ui = ui
		try:
			self.ser = serial.Serial('/dev/ttyUSB0')
		except Exception, e:
			print e

	def set_fwd(self):
		self.isSet_fwd = True
		self.isSet_back = False
		self.isSet_stop = False
		self.isSet_left = False
		self.isSet_right = False

	def set_back(self):
		self.isSet_back = True
		self.isSet_fwd = False
		self.isSet_stop = False
		self.isSet_left = False
		self.isSet_right = False

	def set_left(self):
		self.isSet_left = True
		self.isSet_right = False
		self.isSet_fwd = False
		self.isSet_back = False
		self.isSet_stop = False

	def set_right(self):
		self.isSet_right = True
		self.isSet_left = False
		self.isSet_fwd = False
		self.isSet_back = False
		self.isSet_stop = False

	def set_stop(self):
		self.isSet_stop = True
		self.isSet_fwd = False
		self.isSet_back = False
		self.isSet_left = False
		self.isSet_right = False

	def checkFlags(self):
		if self.isSet_button:
			self.ui.mode.setStyleSheet(CSS_GREEN)
			self.ui.mode.setText("Robot")

			if self.isLatch_button:
				if self.isSet_fwd:
					self.ui.up_arrow.setEnabled(True)
					cmd = 'f'
				else:
					self.ui.up_arrow.setEnabled(False)

				if self.isSet_back:
					self.ui.down_arrow.setEnabled(True)
					cmd = 'b'
				else:
					self.ui.down_arrow.setEnabled(False)
				if self.isSet_left:
					self.ui.left_arrow.setEnabled(True)
					cmd = 'l'
				else:
					self.ui.left_arrow.setEnabled(False)
				if self.isSet_right:
					self.ui.right_arrow.setEnabled(True)
					cmd = 'r'
				else:
					self.ui.right_arrow.setEnabled(False)

				if self.isSet_stop:
					cmd = 's'
					self.ui.stop.setStyleSheet(CSS_RED)
					self.ui.stop.setText("Off")
				else:
					self.ui.stop.setStyleSheet(CSS_GREEN)
					self.ui.stop.setText("On")

				self.cmd_latch = cmd
			else:
				cmd = self.cmd_latch

		else:
			cmd = 's'
                        self.cmd_latch = cmd
			self.set_stop()
			self.disable_arrows()
			self.ui.mode.setText("Relay")
		self.cur_comnd = cmd

		if self.prev_comnd != self.cur_comnd:
			print cmd
                        self.ser.write(cmd)
			self.prev_comnd = self.cur_comnd

		if self.isSet_prev == False and self.isSet_cur == True:
			self.isSet_button = not self.isSet_button


	def disable_arrows(self):
		self.ui.up_arrow.setEnabled(False)
		self.ui.down_arrow.setEnabled(False)
		self.ui.left_arrow.setEnabled(False)
		self.ui.right_arrow.setEnabled(False)
		self.ui.stop.setStyleSheet(CSS_RED)
		self.ui.stop.setText("Off")
		self.ui.mode.setStyleSheet(CSS_RED)


