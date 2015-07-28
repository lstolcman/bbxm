import socket, asyncore, struct

file = open("/dev/input/event0", "rb")
event = file.read(16)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1",8080)


while event:
   (time1, time2, type, code, value) = struct.unpack('iihhi', event)
   if type == 1 and code == 276 and value == 1:
      sent = sock.sendto(value, server_address)
      print "Sent"  
   data,server = sock.recvfrom(2048)
   print "Recived " + data
file.close()

   




