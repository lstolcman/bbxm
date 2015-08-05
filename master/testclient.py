import struct
import asyncore
import socket
import threading
import queue
import time
import configparser



inputQueue = queue.Queue()
outputQueue = queue.Queue()

cfg = configparser.ConfigParser()

class Packet():
    def __init__(self):
        self.packet = None

    def parse(self,packetType):
        if packetType is 0x02:
            print("Server response")

        if packetType is 0x03:
            print("Change status")
            outputQueue.put((struct.pack('!BBB', 0x01, self.packet[0][1], 0x02)))
            #outputQueue.put((struct.pack('!BBB', 0x01, self.packetNum, 0x01), self.packet[1]))
            
        if packetType is 0x04:
            print("Get status")
            outputQueue.put((struct.pack('!BBB', 0x01, self.packet[0][1], 0x01)))         

    def loop(self):
        while 1:
            self.packet = inputQueue.get(block=True)
            self.parse(self.packet[0][0])


class Client(asyncore.dispatcher):
    def __init__(self, host='localhost', port=0):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect((host, port))
        outputQueue.queue.clear()
        self.packet = Packet()
        self.send_status()

    def writable(self):
        return not outputQueue.empty()

    def handle_read(self):
        data = self.recvfrom(1024)
        print("Handle read ", data[0])
        inputQueue.put(data)
        
    def handle_write(self):
        data = outputQueue.get()
        print("Handle write ", data)
        sent = self.send(data)      
        data = data[sent:]

    def send_status(self):
        outputQueue.put((struct.pack('!BBB', 0x01, 0, 0x01)))

       
        

if __name__ == '__main__':

    cfg.read('settings.ini')
    
    client = Client(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    async = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    async.start()
    
    packet = Packet()
    packetThread = threading.Thread(target=packet.loop)
    packetThread.start()
    



