import asyncore, socket, os

class AsyncoreServerUDP(asyncore.dispatcher):
   
   def __init__(self):
      asyncore.dispatcher.__init__(self)
      self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.bind(('', 8080))
      self.buffer = ""
      self.addr = ""
      self.temp = True
      print("Slave start..")

   def handle_read(self):
      self.buffer, self.addr = self.recvfrom(2048)
      self.temp = not self.temp
      
      if self.temp:
         os.system("echo 1 > /sys/class/leds/beagleboard::usr0/brightness")
         print "1"
      else:
         os.system("echo 0 > /sys/class/leds/beagleboard::usr0/brightness")
         print "0"
         
   def handle_write(self):
      if self.buffer != "":
          sent = self.sendto("Signal: "+self.buffer, (str(self.addr[0]), int(self.addr[1])))
          self.buffer = self.buffer[sent:]
          
   def handle_close(self):
      self.close()
      
if __name__ == "__main__":
   
   AsyncoreServerUDP()
   asyncore.loop()



