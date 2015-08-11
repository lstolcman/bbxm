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
ledQueue = queue.Queue()

cfg = configparser.ConfigParser()

class Led():
    def __init__(self):
        self.__led = open("/sys/class/leds/beagleboard::usr0/brightness",'w')
        self.state = 0
        
    def loop(self):
        while 1:
            if not ledQueue.empty():
                self.state = ledQueue.get()
            if self.state is 0:
                self.__led.write('0')
                self.__led.flush()
            if self.state is 1:
                self.__led.write('1')
                self.__led.flush()
            if self.state is 2:
                self.blink(0.8)
            if self.state is 3:
                self.blink(0.1)
                
    def blink(self,delay):
        time.sleep(delay)
        self.__led.write('0')
        self.__led.flush()
        time.sleep(delay)
        self.__led.write('1')
        self.__led.flush()


class Button():
    def __init__(self):
        self.__PATH = "/dev/input/event1"
        self.__file = None
        self.__event = None
        self.packet = Packet()
   
    def loop(self):
        self.__file = open(self.__PATH, "rb")
        self.__event = self.__file.read(16)
        while self.__event:
            (time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
            if type == 1 and code == 276 and value == 1:
                print("Button pressed")
                ledQueue.put(2)
                self.packet.parse(0x03)
            self.__event = self.__file.read(16)
        self.__file.close()

class Packet():
    def __init__(self):
        self.packetNum = 0
        self.packet = None
        self.last_status = 0x01

    def parse(self,packetType):
        if packetType is 0x01:
            print("Client status")
            if self.packet[0][2] is 0x01: #U-Boot                               
                print('U-Boot')
                ledQueue.put(0)
                if self.last_status != 0x01:
                    self.packer(0x02)
                    self.last_status = 0x01
                     
            elif self.packet[0][2] is 0x02: #Linux                              
                print('Linux')
                ledQueue.put(1)
                if self.last_status != 0x02:
                    self.packer(0x02)
                    self.last_status = 0x02
            
        if packetType is 0x02:
            print("Client response")
            
            
        if packetType is 0x03:
            print("Change status")
            if self.packet:
                self.packer(0x03)
                ## get response
                ## get new status 
                
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
    #led = Led()
    
    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    packetThread = threading.Thread(target=packet.loop)
   # buttonThread = threading.Thread(target=button.loop)
    #ledThread = threading.Thread(target=led.loop)
    
    asyncThread.start()
    packetThread.start()
   # buttonThread.start()
   # ledThread.start()

    print('mainloop')
    while 1:
        packet.parse(0x04)
        time.sleep(10)
