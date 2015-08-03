import struct
import asyncore
import socket
import threading
import queue
import time
import configparser
import enum


class LedState(enum.Enum):
    LED_OFF = 0
    LED_ON = 1
    LED_FAST = 2
    LED_SLOW = 3


inputQueue = queue.Queue()
outputQueue = queue.Queue()

ledEvent = threading.Event()
ledState = LedState.LED_OFF

cfg = configparser.ConfigParser()


class Button():
    def __init__(self, buttonPath='/tmp/test'):
        self.button = open(buttonPath, 'r')

    def loop(self):
        while 1:
            pass



class Led():
    def __init__(self, slow=0.5, fast=0.1, ledPath='/tmp/test'):
        self.led = open(ledPath, 'w')
        self.slow = slow
        self.fast = fast
        self.delay = self.fast
        self.state = LedState.LED_FAST

    def toggle(self):
        if self.state is 1:
            self.turnOff()
        else:
            self.turnOn()

    def turnOn(self):
        self.led.write('1')
        self.state = 1

    def turnOff(self):
        self.led.write('0')
        self.state = 0

    def loop(self):
        while 1:
            if ledEvent.wait(self.delay): # event fired, change state
                self.state = ledState
            else: # no event, timeout passed, normal blink
                if self.state is LedState.LED_FAST:
                    self.delay = self.fast
                elif self.state is LedState.LED_SLOW:
                    self.delay = self.slow
                elif self.state is LedState.LED_OFF:
                    self.delay = None
                    self.turnOff()
                elif self.state is LedState.LED_ON:
                    self.delay = None
                    self.turnOn()




class Packet():
    '''Packet reader class

    Tasks:
    - get packet from queue
    - put packet in queue
    - manage LED change state (send new state to LED thread)'''
    def __init__(self):
        self.packetNum = 0
        self.queue = False

    def loop(self):
        while 1:
            queue = inputQueue.get(block=True)
            print(queue)



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
    packet = Packet()
    button = Button()
    led = Led()

    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    packetThread = threading.Thread(target=packet.loop)
    buttonThread = threading.Thread(target=button.loop)
    #ledThread = threading.Thread(target=led.loop, args=cfg.get('Common', 'LedPath'))
    ledThread = threading.Thread(target=led.loop)

    asyncThread.start()
    packetThread.start()
    buttonThread.start()
    ledThread.start()


    print('mainloop')
    while 1:
        pass
        '''
        Here:
        - check timeouts
        - send GetStatus beacon to slave
        '''


