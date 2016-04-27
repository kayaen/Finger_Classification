import re
from bt import BT
from serial.tools.list_ports import comports

from common import *

class MyoRaw(object):
    '''Implements the Myo-specific communication protocol.'''

    def __init__(self, tty=None):
        if tty is None:
            tty = self.detect_tty()
        if tty is None:
            raise ValueError('Myo dongle not found!')

        self.bt = BT(tty)
        self.conn = None
        self.emg_handlers = []
        self.imu_handlers = []
        self.arm_handlers = []
        self.pose_handlers = []

    def detect_tty(self):
        for p in comports():
            if re.search(r'PID=2458:0*1', p[2]):
                print('using device:', p[0])
                return p[0]

        return None

    def run(self, timeout=None):        
        self.bt.recv_packet(timeout)
               
        
    def handle_data(self, p):           
        if (p.cls, p.cmd) != (4, 5): return

        c, attr, typ = unpack('BHB', p.payload[:4])
        pay = p.payload[5:]

#        print('attr is ok?',attr)
        if attr == 0x27:             
            
            vals = unpack('8HB', pay)
            emg = vals[:8]
            moving = vals[8]
#            print('emg:', emg)
            self.on_emg(emg, moving)
                
    def connect(self):
        ## stop everything from before
        self.bt.end_scan()
        self.bt.disconnect(0)
        self.bt.disconnect(1)
        self.bt.disconnect(2)

        ## start scanning
        print('scanning...')
        self.bt.discover()
        while True:
            p = self.bt.recv_packet()
            print('scan response:', p)

            if p.payload.endswith(b'\x06\x42\x48\x12\x4A\x7F\x2C\x48\x47\xB9\xDE\x04\xA9\x01\x00\x06\xD5'):
                addr = list(multiord(p.payload[2:8]))
                break
        self.bt.end_scan()

        ## connect and wait for status event
        conn_pkt = self.bt.connect(addr)
        self.conn = multiord(conn_pkt.payload)[-1]
        self.bt.wait_event(3, 0)

        ## get firmware version
        fw = self.read_attr(0x17)
        _, _, _, _, v0, v1, v2, v3 = unpack('BHBBHHHH', fw.payload)
        print('firmware version: %d.%d.%d.%d' % (v0, v1, v2, v3))

        self.old = (v0 == 0)
        print('old and v0',self.old, v0)

        self.mc_start_collection()
        self.bt.add_handler(self.handle_data)
        print('connect end')

    def write_attr(self, attr, val):
        if self.conn is not None:
            self.bt.write_attr(self.conn, attr, val)

    def read_attr(self, attr):
        if self.conn is not None:
            return self.bt.read_attr(self.conn, attr)
        return None

    def disconnect(self):
        if self.conn is not None:
            self.bt.disconnect(self.conn)

    def mc_start_collection(self):
        '''Myo Connect sends this sequence (or a reordering) when starting data
        collection for v1.0 firmware; this enables raw data but disables arm and
        pose notifications.
        '''
        self.write_attr(0x28, b'\x01\x00')
        self.write_attr(0x19, b'\x01\x03\x01\x01\x01')

    def on_emg(self, emg, moving):
        for h in self.emg_handlers:
            h(emg, moving)
    
    def add_emg_handler(self, h):
        self.emg_handlers.append(h)

    def vibrate(self, duration):
        cmd = b'\x03\x01'
        if duration == 3:
            cmd = cmd + b'\x03'
        elif duration == 2:
            cmd = cmd + b'\x02'
        elif duration == 1:
            cmd = cmd + b'\x01'
        else:
            cmd = cmd + b'\x00'
            
        self.write_attr(0x19, cmd)