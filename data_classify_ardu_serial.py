# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:52:22 2016

@author: Engin
"""

from Myo_python.Myo import MyoRaw
from Myo_python.mwpd import mwpd

import numpy as np
import enum
import serial
ser = serial.Serial('COM20',9600)   #change the COM xxx

x1_step1_ymin_data = []; x1_step1_xoffset_data = []; x1_step1_gain_data = [];
input_hidden_data = []; hidden_out_data = []; bias2_data = []; bias1_data = [];

finger = 0
say = 0
secim = 0
old_secim = 0

inp = []
j = 0
result = []
yi = []
            
h = []
x = []
y = []
a = []
started = 0
end = 0
i = 0
k = 0
tahmin = 0
j=0

J = 4 
winsize = 40
wininc = 40

class Finger(enum.Enum):
    UNKNOWN = 0
    THUMB = 1
    POINT = 2
    MIDDLE = 3
    RING = 4
    LITTLE = 5
    
def load_data():
    global x1_step1_ymin_data, x1_step1_xoffset_data, x1_step1_gain_data 
    global input_hidden_data, hidden_out_data, bias2_data, bias1_data
    bias1_file = 'Matlab_Files/bias1.txt'
    bias2_file = 'Matlab_Files/bias2.txt'
    hidden_out_file = 'Matlab_Files/hidden_output.txt'
    input_hidden_file = 'Matlab_Files/input_hidden.txt'
    x1_step1_gain_file = 'Matlab_Files/x1_step1_gain.txt'
    x1_step1_xoffset_file = 'Matlab_Files/x1_step1_xoffset.txt'
    x1_step1_ymin_file = 'Matlab_Files/x1_step1_ymin.txt'
    
    bias1_data = np.loadtxt(bias1_file)
    bias2_data = np.loadtxt(bias2_file)
    hidden_out_data = np.loadtxt(hidden_out_file)
    input_hidden_data = np.loadtxt(input_hidden_file)
    x1_step1_gain_data = np.loadtxt(x1_step1_gain_file)
    x1_step1_xoffset_data = np.loadtxt(x1_step1_xoffset_file)
    x1_step1_ymin_data = np.loadtxt(x1_step1_ymin_file)

if __name__ == '__main__':
    #ser.write('0')    
    load_data()

    m = MyoRaw() 
    #ser.write('0')
    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x) / np.sum(np.exp(x), axis=0)
    
    def proc_emg(emg, moving, times=[]):
#        print(emg)
        global say, secim, finger, ser, old_secim
        global inp, k, a, h, x, a_temp
        global x1_step1_ymin_data, x1_step1_xoffset_data, x1_step1_gain_data 
        global input_hidden_data, hidden_out_data, bias2_data, bias1_data
        if k<40:
            a.append(emg)
            k = k+1
        else:
            for b in a:
                for c in b:
                    h.append(c)
                x.append(h)
                h = []
            inp = mwpd(x, winsize, wininc, J)
#            print(len(yi))
            inp = inp[0]
            y = np.subtract(inp,x1_step1_xoffset_data) 
            
            y1 = np.multiply(y,x1_step1_gain_data) 
            
            y2 = np.add(y1,x1_step1_ymin_data)  
            
            hh = [(sum(y2[i]*input_hidden_data[i][ji] for i in range(191))+bias1_data[ji]) for ji in range(10)]
            
            h2 = (2./(1+np.exp(np.dot(-2,hh)))-1.)
            
            o = [(sum(h2[i]*hidden_out_data[i][jc] for i in range(10))+bias2_data[jc]) for jc in range(6)]
            
            ff = softmax(o)
            
            cls = [round(ff[i]) for i in range(len(ff))]
            print cls
             
            if 1.0 == cls[0]:
                finger = 1 
                    
            elif 1.0 == cls[1]:
                finger = 2 

            elif 1.0 == cls[2]:
                finger = 3
                    
            elif 1.0 == cls[3]:
                finger = 4
                    
            elif 1.0 == cls[4]:
                finger = 5

            elif 1.0 == cls[5]:
                finger = 6
                
            if finger == 1 and old_secim != 1:
                    print 'finger1'
                    ser.write('1')
                    old_secim = 1
                    
            if finger == 2 and old_secim != 2:
                    print 'finger2'
                    ser.write('2')
                    old_secim = 2
                
            if finger == 3 and old_secim != 3:
                    print 'finger3'
                    ser.write('3')
                    old_secim = 3
                    
            if finger == 4 and old_secim != 4:
                    print 'finger4'
                    ser.write('4')
                    old_secim = 4
                    
            if finger == 5 and old_secim != 5:
                    print 'finger5'
                    ser.write('5')
                    old_secim = 5

            if finger == 6 and old_secim != 6:
                    print 'finger6'
                    ser.write('6')
                    old_secim = 6

            secim = 0
            finger = 0
            say = 0
                                    
            k = 0
            a = []
            x = []
            h = []
            
    m.add_emg_handler(proc_emg)
    m.connect()

     
    try:
        while True: # or limited working i < 1480:
            m.run()

                
    except KeyboardInterrupt:
        pass
    finally:
        m.disconnect()
        print('Disconnected')
        print('len a''s: ',len(a))
