cd('Matlab_Files')
fileID = fopen('input_hidden.txt', 'w');
fprintf(fileID,'%18.15f %18.15f %18.15f %18.15f %18.15f %18.15f %18.15f %18.15f %18.15f %18.15f\n', IW1_1);
fclose(fileID);

fileID = fopen('hidden_output.txt', 'w');
fprintf(fileID,'%18.15f %18.15f %18.15f %18.15f %18.15f %18.15f\n', LW2_1);
fclose(fileID);

fileID = fopen('bias1.txt', 'w');
fprintf(fileID,'%18.15f\n', b1);
fclose(fileID);

fileID = fopen('bias2.txt', 'w');
fprintf(fileID,'%18.15f\n', b2);
fclose(fileID);

fileID = fopen('x1_step1_gain.txt', 'w');
fprintf(fileID,'%18.15f\n', x1_step1_gain);
fclose(fileID);

fileID = fopen('x1_step1_xoffset.txt', 'w');
fprintf(fileID,'%18.15f\n', x1_step1_xoffset);
fclose(fileID);

fileID = fopen('x1_step1_ymin.txt', 'w');
fprintf(fileID,'%18.15f\n', x1_step1_ymin);
fclose(fileID);