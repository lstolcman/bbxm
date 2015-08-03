import struct
import asyncore
import socket
import threading
import queue
import time
import configparser



q_out = queue.Queue()
cfg = configparser.ConfigParser()

class Client(asyncore.dispatcher):
    def __init__(self, host='localhost', port=0):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect((host, port))
        q_out.queue.clear()
        self.buf = ''
        self.packetNum = 0
        self.send_status()

    def writable(self):
        if q_out.empty():
            return False
        else:
            self.buf = q_out.get_nowait()
            return True

    def handle_read(self):
        data, server = self.recvfrom(1024)
        print('Handle read:', data)
        self.packetNum = data[1]
        
        if data[0] is 0x04: #
            print("Get status")
            q_out.put(struct.pack('!BBB', 0x01, data[1], 0x02)) # LINUX
            #q.put(struct.pack('!BBB', 0x01, data[1], 0x01)) # UBOOT      

        elif data[0] is 0x03:
            print("Change status")
            q_out.put(struct.pack('!BB', 0x02, data[1]))
            q_out.put(struct.pack('!BBB', 0x01, data[1]), 0x01)
            
        elif data[0] is 0x02: 
            print("Server has response")
            pass

    def handle_write(self):
        sent = self.send(self.buf)
        print('handle_write:', self.buf)
        self.buf = self.buf[sent:]

    def send_status(self):
        i=0
        while i<5:
            sent = self.sendto(struct.pack('!BBB', 0x01, self.packetNum, 0x01),('localhost',9000))
            print('Try to connect server:', self.buf)
            self.buf = self.buf[sent:]
            i += 1
            self.close()
        
        

if __name__ == '__main__':

    cfg.read('settings.ini')

    client = Client(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    async = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    async.start()
  

