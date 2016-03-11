import serial

class Flags():
	isSet_fwd = False
	isSet_back = False
	isSet_left = False
	isSet_right = False
	isSet_stop = False
	prev_button = False
	cur_button = False
	isSet_button = False
	isLatch_button = False
	prev_cmd = 's'

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
		CSS_RED = 'background-color :rgb(190, 56, 56) ;'
		CSS_GREEN = 'background-color :rgb(0,131, 0) ;'
		
		if self.isLatch_button and self.isSet_button:
			if self.isSet_fwd:
				self.ui.up_arrow.setEnabled(True)
				self.send2xb('f')
			else:
				self.ui.up_arrow.setEnabled(False)

			if self.isSet_back:
				self.ui.down_arrow.setEnabled(True)
				self.send2xb('b')			
			else:
				self.ui.down_arrow.setEnabled(False)
			
			if self.isSet_left:
				self.ui.left_arrow.setEnabled(True)
				self.send2xb('l')		
				
			else:
				self.ui.left_arrow.setEnabled(False)
			
			if self.isSet_right:
				self.ui.right_arrow.setEnabled(True)
				self.send2xb('r')
				
			else:
				self.ui.right_arrow.setEnabled(False)

			if self.isSet_stop:
				try:
					self.ser.write('s')				# Exception if Xbee is not connected
				except AttributeError, e:
					pass
				self.ui.stop.setStyleSheet(CSS_RED)
				self.ui.stop.setText("Off")
			else:
				self.ui.stop.setStyleSheet(CSS_GREEN)
				self.ui.stop.setText("On")
		else:
			if self.isSet_button:
				try:
					self.ser.write(self.prev_cmd)	# Exception if Xbee is not connected
				except AttributeError, e:
					pass

		if self.prev_button == False and self.cur_button == True:
			self.isSet_button = not self.isSet_button


		if self.isSet_button:
			self.ui.mode.setStyleSheet(CSS_GREEN)
			self.ui.mode.setText("Robot")
		else:
			try:
				self.ser.write('s')				# Exception if Xbee is not connected
			except AttributeError, e:
				pass
			
						
				
			self.set_stop()
			
			self.ui.up_arrow.setEnabled(False)
			self.ui.down_arrow.setEnabled(False)
			self.ui.left_arrow.setEnabled(False)
			self.ui.right_arrow.setEnabled(False)
			self.ui.stop.setStyleSheet(CSS_RED)
			self.ui.stop.setText("Off")
			self.ui.mode.setStyleSheet(CSS_RED)
			self.ui.mode.setText("Relay")
			
	def send2xb(self,cmd):
		try:
			self.ser.write(cmd)					# To avoid error while debugging without Xbee
		except AttributeError, e:
			pass
		self.prev_cmd = cmd

