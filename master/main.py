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
        pass

    def waitForButton(self):
        pass



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
    '''Packet reader class

    Tasks:
    - get packet from queue
    - put packet in queue
    - manage LED change state (send new state to LED thread)'''
    def __init__(self):
        self.packetNum = 0



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
        print('handle_read: ', data)

    def handle_write(self):
        data = outputQueue.get()
        sent = self.sendto(data[0], data[1])
        print('handle_write:', data)



if __name__ == '__main__':

    cfg.read('settings.ini')

    async = Async(cfg.get('Common', 'Host'), cfg.getint('Common', 'Port'))

    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})

    asyncThread.start()


    while 1:
        pass
        '''
        Here:
        - check timeouts
        - send GetStatus beacon to slave
        '''


