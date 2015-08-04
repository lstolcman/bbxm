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
    def __init__(self):
        self.__path = buttonPath
        self.__file = None
        self.__event = None
        self.packet = Packet()
        self.open_file()



    def read_file(self):
        self.__file = open(self.__PATH, "rb")
        if self.__file:
            self.__event = self.__file.read(16)
            while self.__event:
                (time1, time2, type, code, value) = struct.unpack('iihhi', self.__event)
                if type == 1 and code == 276 and value == 1:
                    print("Button pressed")
                    self.packet.put_packet(0x03)###
                self.__file.close()
    '''
    def fun_test(self):
        while 1:
            x = input("[x]")
            if x == 'x':
                self.packet.put_packet(0x03)
   ''' 
class Packet():
    def __init__(self):
        self.packetNum = 0
        self.address = None
        self.data = None
   
    def get_packet(self):
        packet = inputQueue.get()
        self.address = packet[1]
        self.data = packet[0]
        return self.data

    def put_packet(self, task):
        outputQueue.put(struct.pack('!BB', task, self.packetNum))
        self.packetNum += 1

    def parse(self, state):
        if state is 0x01:
            print("Client status", self.data[2])
            
        if state is 0x02:
            print("Client response")

        if state is 0x03:
            print("Change status")
            self.put_packet(0x03)
            
        if state is 0x04:
            print("Get status")
            self.put_packet(0x04)
        
class Async(asyncore.dispatcher):
    def __init__(self, host='localhost', port=9000):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet = Packet()
        self.bind((host, port))
        self.buf=''
        self.client = None

    def writable(self):
        if outputQueue.empty():
            return False
        else:
            return True

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recvfrom(1024)
        inputQueue.put(data)
        self.client = data[1]##
        self.packet.parse(self.packet.get_packet()[0])        

    def handle_write(self):
        if self.client:
            data = outputQueue.get()
            sent = self.sendto(data,self.client)##
            print('ID:', data[1],' task:',data[0])
            self.buf = self.buf[sent:]



if __name__ == '__main__':

    cfg.read('settings.ini')
    
    async = Async(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    asyncThread.start()

    async_b = Button()
    async_bThread = threading.Thread(target=async_b.fun_test)
    async_bThread.start()
    
    g_stat = Packet()
    while 1:
        g_stat.parse(0x04)
        time.sleep(10)



