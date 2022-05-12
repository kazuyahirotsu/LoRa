clear
clc

SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;

message = "Hello World!" ;

%% Sampling
Fs = 10e6 ;
Fc = 921.5e6 ;
%% Transmit Signal
signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
Sxx = 10*log10(rms(signalIQ).^2);
disp(['Transmit Power   = ' num2str(Sxx) ' dBm']);

%% Add Noise
Snr = 10;
noise = randn(size(signalIQ))*std(signalIQ)/db2mag(Snr);
disp(['SNR = ' num2str(snr(signalIQ,noise))]);
s = signalIQ+noise;
%% scatter
scatterplot(s)
%% Plots
figure(1);
spectrogram(s,500,0,500,Fs,'yaxis','centered');
%figure(2);
%obw(s,Fs);
%% Received Signal
message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
%% Message Out
disp(['Message Received = ' char(message_out)]);
%% test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "Hello World!" ;
Fs = 10e6 ;
Fc = 921.5e6 ;
signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
Sxx = 10*log10(rms(signalIQ).^2);
disp(['Transmit Power   = ' num2str(Sxx) ' dBm']);
for i=-39:0.1:-35
    Snr = i;
    noise = randn(size(signalIQ))*std(signalIQ)/db2mag(Snr);
    disp(['SNR = ' num2str(snr(signalIQ,noise))]);
    s = signalIQ+noise;
    message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
    disp(['Message Received = ' char(message_out)]);
end
%% 
a=zeros(2,3);
a(1,2)=2;
%% big test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "Hello World!" ;
Fs = 10e6 ;
Fc = 921.5e6 ;
res=zeros(2,41);
for i=-39:0.1:-35
    success = 0;
    for j=1:20
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        Snr = i;
        noise = randn(size(signalIQ))*std(signalIQ)/db2mag(Snr);
        s = signalIQ+noise;
        message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
        if char(message_out)==message
            success = success+1;
        end
    end
    res(1,int64((i+39)*10)+1)=i;
    res(2,int64((i+39)*10)+1)=success/10;
    disp([num2str(((i+39)*10+1)*100/40) '% done' ])
end
%% big test2
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "Hello World!" ;
Fs = 10e6 ;
Fc = 921.5e6 ;
res3=zeros(2,10);
for i=-33.9:0.1:-33
    success = 0;
    for j=1:20
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        Snr = i;
        noise = randn(size(signalIQ))*std(signalIQ)/db2mag(Snr);
        s = signalIQ+noise;
        message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
        if char(message_out)==message
            success = success+1;
        end
    end
    res3(1,int64((i+33.9)*10)+1)=i;
    res3(2,int64((i+33.9)*10)+1)=success/10;
    disp([num2str(((i+33.9)*10+1)*100/10) '% done' ])
end
%% plot
res_m = cat(2,res_m,res3);
figure
plot(res_m(1,:),res_m(2,:)/2)
xlabel('snr(dB)')
ylabel('success rate')