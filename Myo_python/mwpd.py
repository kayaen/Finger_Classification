
import pywt;
import numpy as np;

def mwpd(X1, winsize, wininc, J):
    X = np.reshape(X1,(len(X1),8))
    datasize  = len(X)
    numwin    = np.floor((datasize - winsize)/wininc)+1
    Signals   = np.zeros((winsize,numwin))
    nfCh      = (np.power(2,(J+1))-1)
    Features  = np.zeros((numwin,nfCh*X.shape[1]))

    feat_array = np.zeros((len(Signals[1]),J+1,np.power(2,J)));
    feat = feat_array.tolist()

    row_num = 0
    for j in range(3,J+1):
        row_num = row_num + np.power(2,j)
    FEAT = [[0 for l in range(0,row_num)] for l in range(0,len(Signals[1]))]
    All_Feat = [[] for l in range(0,int(numwin))]
    def waveod(x):
        ## Start the process and loop along all dimensions (channels)
        for i_Sig in range(0,1): #1 = int(x.shape[1])
            st  = 0
            en  = winsize
            for i in range(0,int(numwin)):
                Signals[0:winsize,i] = x[st:en]
                st = st + wininc
                en = en + wininc
            
            for p in range(0,len(Signals[1])):
                feat[p][0][0] = Signals[:,p]
                for k in range(0,J):
                    index = 0
                    for j in range(0,np.power(2,k)):
                        (feat[p][k+1][index], feat[p][k+1][index+1]) = pywt.dwt(feat[p][k][j],'db4')
                        index = index +2

                num = 0
                for k in range(3,J+1):
                    for j in range(0,np.power(2,k)):         
                        FEAT[p][num] = np.log(np.sqrt(np.mean(np.square(feat[p][k][j]))))
                        num = num +1 
        return FEAT
    for k in range(0,X.shape[1]):
        for j in range(0,len(All_Feat)):
            All_Feat[j] = All_Feat[j] + waveod(X[:,k])[j]
    return All_Feat

