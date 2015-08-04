import struct


with open('/tmp/test', 'wb') as f:
    while 1:
        input('Press Enter to send button')
        # push button
        f.write(struct.pack('llHHI', 0,0,1,276,1))
        f.flush()

        # release button
        f.write(struct.pack('llHHI', 0,0,1,276,0))
        f.flush()



