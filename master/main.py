import time, socket, os, threading

IP = "localhost"
PORT = 8080
FILE = "plik.txt"

class LedStatus(object):
	def __init__(self, bin):
		self.bin = bin
		self.status = {0x02 : self.led_on(),
					   0x01 : self.led_off(),
					   0x03 : self.led_fast(),
				       #default : self.led_slow(bin),}
		self.status(bin)
		
	def led_off(self):
		os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")

	def led_on(self):
		os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
		
	def led_slow(self):
		while 1:
			os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")
			time.sleep(2)
			os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
			time.sleep(2)
	
	def led_fast(self):
		while 1:
			os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")
			time.sleep(0.5)
			os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
			time.sleep(0.5)

			
			
class ClientUdp(object):
	def __init__(self):
		self.__IP = IP
		self.__PORT = PORT
		self.__sock = None
		self.open_socket()
		
	def open_socket(self):
		self.__server_address = (self.__IP,self.__PORT)
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def send_message(self,MSG):
		sent = self.__sock.sendto(bytes(str(MSG),'UTF-8'), self.__server_address)
		print("Message sent")
	
	def read_message(self):
		data,server = self.__sock.recvfrom(1048)
		(ID, HEADER) = struct.unpack('ic',data)
		#print("ID: "+ ID + " ,HEADER: "+HEADER)
		return (ID, HEADER)
			
	
	
class FileHandler(ClientUdp):
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
	
class MakeStructure():
	def __init__(self,HEADER):
		self.__id = 0
		
	def pack(self):
		self.__id += self.__id
		return (self.__id,struct.pack('ic',self.__id,HEADER))
		
		
class ChangeStatus(threading.Thread,FileHandler,ClientUdp):
	def __init__(self):
		__struct = make_struct(0x03)
		send_message(__struct[1])
		rcv_id = read_message()
		if rcv_id[0] == struct[0] 
		read_message()
		
		
class GetStatus(threading.Thread,LedStatus, ClientUdp):
	def __init__(self):	   
		__struct = make_struct(0x04)
		send_message(__struct[1])
		rcv_id = read_message()
		if rcv_id[0] == struct[0]
			print("Status checked")
			self.led = LedStatus(struct[1])	##??
		else:
			print("Incompatible ID")
		time.sleep(5)
			

  
if __name__=="__main__":

	thread1 = GetStatus()
	thread1.start()
	
	
	

