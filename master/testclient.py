import struct
import asyncore
import socket
import threading
import queue
import time
import configparser


q = queue.Queue()
cfg = configparser.ConfigParser()


class Client(asyncore.dispatcher):

    def __init__(self, host='localhost', port=0):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect((host, port))
        q.queue.clear()
        self.buf = ''
        self.packetNum = 0

    def writable(self):
        if q.empty():
            return False
        else:
            self.buf = q.get_nowait()
            return True

    def handle_close(self):
        self.close()

    def handle_read(self):
        data, server = self.recvfrom(1024)
        print('handle_read:', data)
        if data[0] is 0x01: #status
            q.put(struct.pack('!BBB', 0x01, self.packetNum, 0x01))
            self.packetNum += 1
        elif data[0] is 0x02: #response
            pass


    def handle_write(self):
        sent = self.send(self.buf)
        print('handle_write:', self.buf)
        self.buf = self.buf[sent:]

    def sendStatusUBoot(self):
        q.put(struct.pack('!BBB', 0x01, self.packetNum, 0x01))
        self.packetNum += 1
    def sendStatusLinux(self):
        q.put(struct.pack('!BBB', 0x01, self.packetNum, 0x02))
        self.packetNum += 1
    def sendResponse(self):
        q.put(struct.pack('!BB', 0x02, self.packetNum))


if __name__ == '__main__':

    cfg.read('settings.ini')

    client = Client(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))
    async = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    async.start()




    #client.sendStatusUBoot()




    while 1:
        print('1. wyslij status uboot')
        print('2. wyslij status linux')
        print('3. wyslij response')
        data = int(input('wybor:\n'))
        if data is 1:
            client.sendStatusUBoot()
        elif data is 2:
            client.sendStatusLinux()
        elif data is 3:
            client.sendResponse()
        else:
            print('1. wyslij status uboot')
            print('2. wyslij status linux')
            print('3. wyslij response')
            data = int(input('wybor:\n'))
        #client.sendStatus()
        #time.sleep(5)

