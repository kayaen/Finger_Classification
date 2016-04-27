# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:05:39 2016

@author: Engin
"""
import numpy as np
import os

def create_m_file():
    finger1_file = 'finger1.txt'
    finger2_file = 'finger2.txt'
    finger3_file = 'finger3.txt'
    finger4_file = 'finger4.txt'
    finger5_file = 'finger5.txt'
    finger6_file = 'finger6.txt'
    
    finger1_data = np.loadtxt(finger1_file)
    finger2_data = np.loadtxt(finger2_file)
    finger3_data = np.loadtxt(finger3_file)
    finger4_data = np.loadtxt(finger4_file)
    finger5_data = np.loadtxt(finger5_file)
    finger6_data = np.loadtxt(finger6_file)    
    
    print 'file is creating'
    os.chdir( "../Matlab_Files" )
    fo = open("finger_moves.m", "a")
    fo.write('finger1 = [')
    for b in finger1_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    fo.write('finger2 = [')
    for b in finger2_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    fo.write('finger3 = [')
    for b in finger3_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    fo.write('finger4 = [')
    for b in finger4_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    fo.write('finger5 = [')
    for b in finger5_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    fo.write('finger6 = [')
    for b in finger6_data:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
    fo.write('];')
    
    fo.close()    
    print 'CREATED'
    
if __name__ == '__main__':
    create_m_file()
