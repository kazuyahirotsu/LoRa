%% multipath test
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

%multipath
%mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
mpChan = [0.8 0 0.4 -0.8 0 0 0.1 0 -0.5 0 0.5 0.2 0.4 0 0 0.9 0.34].';
mpChanOut = filter(mpChan,1,signalIQ);

for i=-39:0.1:-35
    Snr = i;
    noise = randn(size(mpChanOut))*std(mpChanOut)/db2mag(Snr);
    disp(['SNR = ' num2str(snr(mpChanOut,noise))]);
    s = mpChanOut+noise;
    message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
    disp(['Message Received = ' char(message_out)]);
end
%% comparison
specAn = dsp.SpectrumAnalyzer("NumInputPorts",2, ...
    "SpectralAverages",50, ...
    "ShowLegend",true);
specAn(signalIQ,mpChanOut)
%% big multipath test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "Hello World!" ;
Fs = 10e6 ;
Fc = 921.5e6 ;
res_multi=zeros(2,61);
for i=-39:0.1:-33
    success = 0;
    for j=1:20
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        mpChanOut = filter(mpChan,1,signalIQ);
        Snr = i;
        noise = randn(size(mpChanOut))*std(mpChanOut)/db2mag(Snr);
        s = mpChanOut+noise;
        message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
        if char(message_out)==message
            success = success+1;
        end
    end
    res_multi(1,int64((i+39)*10)+1)=i;
    res_multi(2,int64((i+39)*10)+1)=success/20;
    disp([num2str(((i+39)*10+1)*100/61) '% done' ])
end
%% plot
figure
plot(res_multi(1,:),res_multi(2,:))
xlabel('snr(dB)')
ylabel('success rate')
