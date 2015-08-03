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


class Button():
    def __init__(self, buttonPath=None):
        self.__path = buttonPath
        self.__file = None
        self.__event = None
        self.packet = Packet()
        self.open_file()

        
    def open_file(self):
        self.__file = open(self.__PATH, "rb")
        if self.__file:
            self.__event = self.__file.read(16)
            self.read_file()

    def read_file(self):
        while self.__event:
            (time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
            if type == 1 and code == 276 and value == 1:
                print("Button pressed")
                self.packet.change_status()
            self.__file.close()
 
class Led():
    def __init__(self, slow=0.5, fast=0.1, ledPath='/sys/class/leds/beagleboard::usr0/brightness'):
        self.slow = slow
        self.fast = fast

    def toggle(self):
        pass

    def turnOn(self):
        pass

    def turnOff(self):
        pass

    def blinkSlow(self):
        self.toggle()
        time.sleep(self.slow)


    def blinkFast(self):
        self.toggle()
        time.sleep(self.fast)



class Packet():
    def __init__(self):
        self.packetNum = 0
        self.address = None
        self.data = None
        
    def get_packet(self):
        packet = inputQueue.get()
        self.address = packet[1]
        self.data = packet[0]

    def put_packet(self, task):
        outputQueue.put((struct.pack('!BB', task, self.packetNum)),('localhost',9000))

    def change_status(self):
        self.put_packet(0x03)
  
    def get_status(self):
        self.put_packet(0x04)

    def parse(self):
        if self.data[0] is 0x01:
            print("Client status")
            
        if self.data[0] is 0x02:
            print("Client response")
    
        
class Async(asyncore.dispatcher):
    '''Asynchronous socket handling'''
    def __init__(self, host='localhost', port=9000):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet = Packet()
        self.bind((host, port))
        self.buf=""
        self.data_to_send = None

    def writable(self):
        return not outputQueue.empty()

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recvfrom(1024)
        inputQueue.put(data)
        print('handle_read: ', data)

    def handle_write(self):
        self.data_to_send = outputQueue.get()
        sent = self.sendto(self.data_to_send[0],self.data_to_send[1])
        print('handle_write:')
        self.buf = self.buf[sent:]



if __name__ == '__main__':

    cfg.read('settings.ini')
    
    async = Async(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    asyncThread.start()

    g_stat = Packet()
    while 1:
        g_stat.get_status()
        '''
        Here:
        - check timeouts
        - send GetStatus beacon to slave
        '''


