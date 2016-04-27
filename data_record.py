
from Myo_python.Myo import MyoRaw

a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []

a = []
i = 0
    
if __name__ == '__main__':

    m = MyoRaw() 
#    data_sayi = 500; bekleme = 110;         #alinacak data sayisi gir!!
    data_sayi = eval(raw_input("Enter number of example (ideal=500): "))
    bekleme = eval(raw_input("Enter waiting between two movement (ideal=120): "))
    
    def proc_emg(emg, moving, times=[]):
#        print(emg)
        if i<bekleme:
            print ("Rest position")            
        elif i<data_sayi+bekleme:
            a6.append(emg)            #6 
        elif i<data_sayi+2*bekleme:
            print ("1st Finger")            
        elif i<2*data_sayi+2*bekleme:
            a1.append(emg)          #1
        elif i < 2*data_sayi+3*bekleme:
            print ("2nd Finger")
        elif i < 3*data_sayi+3*bekleme:
            a2.append(emg)           #2 topla (320 530)
        elif i < 3*data_sayi+4*bekleme:
            print ("3rd Finger")
        elif i < 4*data_sayi+4*bekleme:
            a3.append(emg)          # 3 topla (630 840)
        elif i < 4*data_sayi+5*bekleme:
            print ("4th Finger")
        elif i < 5*data_sayi+5*bekleme:              
            a4.append(emg)          # 4 topla (940 1150)
        elif i < 5*data_sayi+6*bekleme:
            print ("5th Finger")
        elif i < 6*data_sayi+6*bekleme:
            a5.append(emg)          # 5 topla (1250 1460)
        elif i < 6*data_sayi+7*bekleme:
            print ("Finished")

    m.add_emg_handler(proc_emg)
    m.connect()

    try:
        while i<(6*data_sayi+7*bekleme)+1: #True #clock() < interval_time:
            m.run()
            i = i+1
        
    except KeyboardInterrupt:
        pass
    finally:
        m.disconnect()
        print('Disconnected')
        print('len a''s: ',len(a1),len(a2),len(a3),len(a4),len(a5),len(a6))
        fo = open("Finger_Data/finger1.txt", "a")
        for b in a1:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        fo = open("Finger_Data/finger2.txt", "a")
        for b in a2:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        fo = open("Finger_Data/finger3.txt", "a")
        for b in a3:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        fo = open("Finger_Data/finger4.txt", "a")
        for b in a4:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        fo = open("Finger_Data/finger5.txt", "a")
        for b in a5:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        fo = open("Finger_Data/finger6.txt", "a")
        for b in a6:
            for comp in b:
                fo.write(str(comp).ljust(5) + '\t' )
            fo.write('\n' )
        fo.close()

        s = 's'
        if 's' == eval(raw_input("Automaticly transform to matlab file, Enter s: \t")):
            from Finger_Data.create_mFile import create_m_file            
            import os
            os.chdir( "Finger_Data" )
            create_m_file()
        