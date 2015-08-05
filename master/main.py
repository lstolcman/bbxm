import struct
import asyncore
import socket
import threading
import queue
import time
import configparser
import enum
import struct




inputQueue = queue.Queue()
outputQueue = queue.Queue()

cfg = configparser.ConfigParser()

class Button():
    def __init__(self):
        self.__PATH = "/dev/input/event0"
        self.__file = None
        self.__event = None
        self.packet = Packet()
   
    def loop(self):
        self.__file = open(self.__PATH, "rb")
        if self.__file:
            self.__event = self.__file.read(16)
            while self.__event:
                (time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
                if type == 1 and code == 276 and value == 1:
                    print("Button pressed")
                    self.packet.put_packet(0x03)
                self.__event = self.__file.read(16)
            self.__file.close()

class Packet():
    def __init__(self):
        self.packetNum = 0
        self.packet = None

    def parse(self,packetType):

        if packetType is 0x01:
            print("Client status")
            if self.packet[0][2] is 0x01: #U-Boot                               
                print('U-Boot')
            elif self.packet[0][2] is 0x02: #Linux                              
                print('Linux')

        if packetType is 0x02:
            print("Client response")

        if packetType is 0x03:
            print("Change status")
            if self.packet:
                self.packer(0x03)
                
        if packetType is 0x04:
            print("Get status")
            if self.packet:
                self.packer(0x04)

    def packer(self, bit):
        outputQueue.put((struct.pack('!BB', bit, self.packetNum), self.packet[1]))
        self.packetNum += 1
        
    def loop(self):                       
        while 1:
            self.packet = inputQueue.get()
            self.parse(self.packet[0][0])
            
class Async(asyncore.dispatcher):
    '''Asynchronous socket handling'''
    def __init__(self, host='localhost', port=9000):                            
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet = Packet()    
        self.bind((host, port))

    def writable(self):
        return not outputQueue.empty()

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recvfrom(1024)
        inputQueue.put(data)
        print('handle_read: ', data[0])

    def handle_write(self):
        data = outputQueue.get()
        sent = self.sendto(data[0], data[1])
        print('handle_write:', data[0])



if __name__ == '__main__':

    cfg.read('settings.ini')

    async = Async(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    packet = Packet()
    #button = Button()
    
    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    packetThread = threading.Thread(target=packet.loop)
    #buttonThread = threading.Thread(target=button.loop)
    
    asyncThread.start()
    packetThread.start()
    #buttonThread.start()


    print('mainloop')
    while 1:
        packet.parse(0x04)
        time.sleep(3)
