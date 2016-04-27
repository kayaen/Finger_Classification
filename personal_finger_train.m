%FUNCTION%
%kisi sayisi ve hareket sayisini input olarak al
%window size input olarak al
%tum datalari run eder
%kisi ve hareket adlarina gore gerekli datalari secer
%wavelete bunlari sokar ve ayni hareketleri uc uca ekler
%class lari olusturur
%input matrisinin boyutuna gore target matrisini yapar.
%function [net, X, T, S] = personal_finger_train()

wininc=10;
winsize=40;
SF=4;
X=[];
T=[];
S=[];
M=[];

addpath('Matlab_Files');
run('finger_moves.m');

har_num = 6;
kisiler = {'fin'};
hareketler = { '1'; '2'; '3'; '4'; '5'; '6' };
inp_kisi=kisiler{input('Devam etmek icin 1 ve enter basin.')};

fprintf(inp_kisi)
fprintf('\n')

for j=1:1:har_num
        
    sv=[inp_kisi '*' hareketler{j}];
    gerekli_var=who(sv);
    size_var=size(gerekli_var);
        
    for t=1:1:size_var(1)
        wl_data=getmswpfeat(eval(gerekli_var{t}),winsize,wininc,SF,'matlab');         
        X=[X; wl_data];
    end
    
    [ row_x col_x ]=size(X);
    [ row_t col_t ]=size(T);
    T(row_t+1:row_x,j)=ones(row_x-row_t,1);
end

X=X';
T=T';

hiddenLayerSize=10;
inputs=X;
targets=T;
net = patternnet(hiddenLayerSize);
net.divideFcn = 'dividerand';  % Divide data randomly
net.divideMode = 'sample';  % Divide up every sample
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

[net,tr] = train(net,inputs,targets);

for i=1:length(X(:,1))
    max_x = max(X(i,:));
    min_x = min(X(i,:));
    x1_step1_gain(i) = 2/(max_x-min_x);
end

IW1_1 = net.IW{1,1};
LW2_1 = net.LW{2,1};
b1 = net.b{1,1};
b2 = net.b{2,1};
x1_step1_xoffset = net.inputs{1,1}.range(:,1);
x1_step1_gain = x1_step1_gain';     
x1_step1_ymin = -1;

s = 's';
if s == input('Kayit etmek icin s ve enter basin.')
    coefficients_to_txt_files
    disp('Kayit tamamlandi')
else
    disp('Kayit edilmeden cikildi')
end

