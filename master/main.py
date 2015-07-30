IP = "localhost"
PORT = 8080
FILE = "plik.txt"

class LedStatus(object):
	def led_off(self):
		os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")

	def led_on(self):
		os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
		
	def led_slow(self):
		while 1:
			os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")
			delay(1000ms)
			os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
			delay(1000ms)
	
	def led_fast(self):
		while 1:
			os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")
			delay(100ms)
			os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
			delay(100ms)

			
			
class ClientUdp(object):
	def __init__(self):
		self.__IP = IP
		self.__PORT = PORT
		self.__sock = None
		self.open_socket()
		
	def open_socket(self):
		self.__server_address = (self.__IP,self.__PORT)
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if self.__sock:
			p
			print("Open success")
		else:
			print ("Socket error")

	def send_message(self,MSG):
		sent = self.__sock.sendto(bytes(str(MSG),'UTF-8'), self.__server_address)
		print("Message sent")
	
	def read_message(self):
		data,server = self.__sock.recvfrom(1048)
		(ID, HEADER) = struct.unpack('ic',data)
		#print("ID: "+ ID + " ,HEADER: "+HEADER)
		return (ID)
			
	
	
class FileHandler(ClientUdp,Events):
	def __init__(self,PATH):
		self.client = ClientUdp()
		self.event = Events()
		self.__PATH = FILE # TEMP FILE
		self.__file = None
		self.__event = None
		self.open_file()
		
	def open_file(self):
		self.__file = open(self.__PATH, "rb")
		if self.__file:
			self.__event = self.__file.read(16)
			print("File opened")
		else:
			print("File error")
		
	def read_file_event(self):
		while self.__event:
			(time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
			if type == 1 and code == 276 and value == 1:
			 print("Button pushed")
			 self.client.change_status()
		self.close_file(self):
	
	def close_file(self):
		self.__file.close()	

		
		
class Events(object):
	def __init__(self):
		self.__queue = []
		self.__package = None
		self.__id = 0
		
		self.led = LedStatus()
		self.status = {0 : self.led.led_on,
					   1 : self.led.led_off
					   2 : self.led.led_fast,
					   3 : self.led.led_slow,
					   }

	def append(self,aDATA):
		self.__queue.append(aDATA)
	
	def pop(self):
		return self.__queue.pop(0)
	
	def make_struct(self,HEADER):
		self.__id += self.__id
		return (self.__id,struct.pack('ic',self.__id,HEADER))
	
	def get_status(self):
		struct = make_struct(0x04)
		send_message(struct[1])
		rcv_id = read_message()
		if rcv_id == struct[0]
			print("Status checked")
			#CHANGE_LED_STATUS
			
		else:
			print("Incompatible ID")
		
	def change_status(self):
		send_message(self.manager.make_pack(0x03))
		read_message()
		
	
	def response(self):
		return read_message()
		
	def 
		
class Main(LedStatus):
	def __init__(self):
		
	
	
	def thread1():
		read_message()
		
		


  
if __name__=="__main__":

