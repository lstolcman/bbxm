import socket, asyncore, struct

BUTTON_USER_EVENT = "/dev/input/event1"

class ReadButton(object):
   def __init__(self, server_address, sock):
      print("Start Read Button")
      self.__sock = sock
      self.__server_address = server_address
      self.__file = open(BUTTON_USER_EVENT, "rb")
      print("File opened")
      if self.__file:
         self.__event = self.__file.read(16)
         self.read_event()
      else:
         return 0

   def read_event(self):
      print("Event reading")
      while self.__event:
          (time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
          if type == 1 and code == 276 and value == 1:
             sent = self.__sock.sendto(bytes(str(value),'UTF-8'), self.__server_address)
             print ("Sent byte")  
          data,server = self.__sock.recvfrom(2048)
          print ("Recived " + data)
      file.close()
      return 1


class ClientUdp(ReadButton):
   def __init__(self, IP, PORT):
      print("StartUDP")                                
      self.__IP = IP
      self.__PORT = PORT
      self.__sock = None
      self.__server_address = (self.__IP,self.__PORT)
      if self.open_socket():
         self.ReadButton = ReadButton(self.__server_address, self.__sock)
      else:
         print("Cannot open socket")
               
   def open_socket(self):
      self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      if self.__sock:
         return True
      else:
         return False
   

class StartClient(ClientUdp):
   def __init__(self,IP,PORT):
      print("ClientInit")
      self.__IP = IP
      self.__PORT = PORT
      self.ClientUdp = ClientUdp(self.__IP,self.__PORT)
      

      
if __name__=="__main__":
   
   StartClient("10.0.0.2",8080)

 
