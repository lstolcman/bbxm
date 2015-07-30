
class ClientUdp(object):
	def __init__(self, IP, PORT):
		self.__IP = IP
		self.__PORT = PORT
		self.__sock = None
		self.open_socket()
		
	def open_socket(self):
		self.__server_address = (self.__IP,self.__PORT)
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM):
		if self.__sock:
			print("Open success")
		else:
			print ("Socket error")

	def send_message(self,MSG):
		sent = self.__sock.sendto(bytes(str(MSG),'UTF-8'), self.__server_address)
		print("Message sent")
	
	def read_message(self):
		data,server = self.__sock.recvfrom(1048)
		print("Received message: "+ data+", from :"+server)
	
	
class EventHandler(object):
	def __init__(self,PATH):
		self.__PATH = PATH
		self.__file = None
		self.__event = None
		
	def open_file(self):
		self.__file = open(self.__PATH, "rb")
		if self.__file:
			self.__event = self.__file.read(16)
			print("File opened")
		else:
			print("File error")
		
	def change_status(self):
		while self.__event:
			(time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
			if type == 1 and code == 276 and value == 1:
			#send_message
			#wait_for_response
		self.close_file()
	
	def close_file(self):
		self.__file.close()	
	
	def get_status(self):
		#send_message
		#wait_for_response
		

class EventManager(object):
	def __init__(self):
		self.__queue = []
		self.__package = None

	def append(self,aDATA):
		self.__queue.append(aDATA)
	
	def pop(self):
		return self.__queue.pop(0)
	
	def make_pack(self):
		struct.pack("")
	
	
class Master(object):
	def __init__(self):
	
	


  
if __name__=="__main__":
	StartClient("10.0.0.2",8080)
