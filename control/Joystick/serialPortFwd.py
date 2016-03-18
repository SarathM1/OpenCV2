import serial

serXbee = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.SEVENBITS
)

serArduino = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.SEVENBITS
)


def main():
	while True:
		ch = serArduino.read(1)

		if ch in ['f'  ,'b'  ,'l'  , 'r'  ,'s']:
			print ch
			serXbee.write(ch)

if __name__ == '__main__':
	main()