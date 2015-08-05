import platform
import struct
import asyncore
import socket
import threading
import queue
import time
import configparser
import enum
import struct


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
    def __init__(self, buttonPath):
        self.button = None
        self.buttonPath = buttonPath

    def loop(self):
        with open(self.buttonPath, 'rb') as self.button:
            print('bytn')
            evt = self.button.read(struct.calcsize('llHHI'))
            while evt:
                tv_sec, tv_usec, key_type, key_code, key_value = struct.unpack('llHHI', evt)
                if key_type == 1 and key_code == 276 and key_value == 0:
                    print(evt)
                    print(tv_sec, tv_usec, key_type, key_code, key_value)
                    print('user key released')
                evt = self.button.read(struct.calcsize('llHHI'))






class Led():
    def __init__(self, ledPath, slow=0.15, fast=0.05):
        self.led = open(ledPath, 'w')
        self.slow = slow
        self.fast = fast
        self.delay = self.fast
        self.value = 0

    def __del__(self):
        self.led.close()

    def toggle(self):
        if self.value == 1:
            self.turnOff()
        else:
            self.turnOn()

    def turnOn(self):
        self.led.write('1')
        self.led.flush()
        self.value = 1

    def turnOff(self):
        self.led.write('0')
        self.led.flush()
        self.value = 0

    def loop(self):
        while 1:
            if ledEvent.wait(self.delay): # event fired, change state
                if ledState == LedState.LED_FAST:
                    self.delay = self.fast
                elif ledState == LedState.LED_SLOW:
                    self.delay = self.slow
                elif ledState == LedState.LED_ON:
                    self.delay = None
                    self.turnOn()
                elif ledState == LedState.LED_OFF:
                    self.delay = None
                    self.turnOff()
                else:
                    raise Exception('Unknown LED state')

            else: # no event, timeout passed, normal blink
                self.toggle()



class Packet():
    '''Packet reader class

    Tasks:
    - get packet from queue
    - put packet in queue
    - manage LED change state (send new state to LED thread)'''
    def __init__(self):
        self.packetNum = 0
        self.queue = False
        self.packet = None

    def parse(self):
        packetType = self.packet[0][0]
        packetNum = self.packet[0][1]
        if packetType == 0x01: #STATUS
            packetState = self.packet[0][2]
            outputQueue.put((struct.pack('!BB', 0x02, self.packetNum), self.packet[1]))
            print('received status: ', end='')
            if packetState == 0x01: #U-Boot
                print('U-Boot')
            elif packetState == 0x02: #Linux
                print('Linux')
            else:
                print('Unknown')
        elif packetType == 0x02: #RESPONSE
            print('received response')
        else: #unknown
            raise TypeError('Unsupported header')

    def getStatus(self):
        if self.packet:
            outputQueue.put((struct.pack('!BB', 0x04, self.packetNum), self.packet[1]))

    def changeState(self):
        if self.packet:
            outputQueue.put((struct.pack('!BB', 0x03, self.packetNum), self.packet[1]))

    def loop(self):
        while 1:
            self.packet = inputQueue.get(block=True)
            self.parse()



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

    if platform.machine() == 'armv7l': #beagle
        button = Button(cfg.get('Common', 'ButtonPath'))
        led = Led(cfg.get('Common', 'LedPath'))
    else: #host computer
        button = Button('/tmp/test')
        led = Led('/tmp/testled')

    asyncThread = threading.Thread(target=asyncore.loop, kwargs={'timeout':0.1, 'use_poll':True})
    packetThread = threading.Thread(target=packet.loop)
    buttonThread = threading.Thread(target=button.loop)
    ledThread = threading.Thread(target=led.loop)

    asyncThread.start()
    packetThread.start()
    buttonThread.start()
    ledThread.start()


    print('mainloop')
    while 1:
        #packet.getStatus()
        time.sleep(1)
        '''
        Here:
        - check timeouts
        - send GetStatus beacon to slave
        '''


