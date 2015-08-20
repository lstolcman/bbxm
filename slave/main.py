import struct
import asyncore
import socket
import threading
import queue
import time
import configparser
import enum
import struct
import os


inputQueue = queue.Queue()
outputQueue = queue.Queue()
sendQueue = queue.Queue()

cfg = configparser.ConfigParser()

class Packet():
    def __init__(self):
        self.packet = None

    def parse(self,packetType):
        if packetType is 0x02:
            print("Server response")

        if packetType is 0x03:
            print("Change status")
            outputQueue.put((struct.pack('!BB', 0x02, self.packet[0][1])))
            os.system("shutdown now -r")
            
        if packetType is 0x04:
            print("Get status")
            outputQueue.put((struct.pack('!BBB', 0x01, self.packet[0][1], 0x02)))         

    def loop(self):
        while 1:
            self.packet = inputQueue.get(block=True)
            self.parse(self.packet[0][0])


class Client(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect((host, port))
        outputQueue.queue.clear()
        self.packet = Packet()
        self.send_status()
        
    def writable(self):
        return not outputQueue.empty()

    def handle_read(self):
        sendQueue.put(1)
        data = self.recvfrom(1024)
        print("Handle read ", data[0])
        inputQueue.put(data)
        
    def handle_write(self):
        data = outputQueue.get()
        print("Handle write ", data)
        sent = self.send(data)      
        data = data[sent:]

    def send_status(self):
        f = None
        while not f:
            try:
                time.sleep(3)
                print("Try init")
                rc = self.send(struct.pack('!BBB', 0x01, 0x00, 0x02))
                f = self.recvfrom(1024)
            except:
                print("Server is not responding")

        
if __name__ == '__main__':

    cfg.read('settings.ini')
    
    client = Client('10.0.0.1',9090)
    async = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    async.start()
    
    packet = Packet()
    packetThread = threading.Thread(target=packet.loop)
    packetThread.start()


        
    



