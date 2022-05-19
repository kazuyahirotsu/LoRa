%% multipath SER test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "0000000000" ;
zeroNum = strlength(message);
disp(['zeronum  = ' num2str(zeroNum)]);
Fs = 10e6 ;
Fc = 921.5e6 ;
signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
Sxx = 10*log10(rms(signalIQ).^2);
disp(['Transmit Power   = ' num2str(Sxx) ' dBm']);

%multipath
mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
mpChanOut = filter(mpChan,1,signalIQ);

for i=-60:-40
    %Snr = i;
    %noise = randn(size(mpChanOut))*std(mpChanOut)/db2mag(Snr);
    %disp(['SNR = ' num2str(snr(mpChanOut,noise))]);
    %s = mpChanOut+noise;
    %message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
    disp(['SNR: ' num2str(i)]);
    snr = i;
    channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
    channelOutput = channel(signalIQ);
    message_out = LoRa_Rx(channelOutput,BW,SF,2,Fs,Fc - fc);
    disp(['Message Received = ' char(message_out)]);
    if ~isempty(char(message_out))
        success_symbol = 0;
        for j=1:length(char(message_out))
            if char(message_out(j)) == "0"
                success_symbol = success_symbol+1;
            end
        end
    end
    SER = 1-success_symbol/zeroNum;
    disp(['SER = ' num2str(SER)]);
    disp(' ');
end

%% big multipath SER test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "000000000000000000000000000000000000000000" ;
zeroNum = strlength(message);
Fs = 10e6 ;
Fc = 921.5e6 ;
res_multi_ser=zeros(2,11);
for i=-55:-45
    SERAve = 0;
    for j=1:20
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        mpChanOut = filter(mpChan,1,signalIQ);
        %Snr = i;
        %noise = randn(size(mpChanOut))*std(mpChanOut)/db2mag(Snr);
        %disp(['SNR = ' num2str(snr(mpChanOut,noise))]);
        %s = mpChanOut+noise;
        %message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);
        disp(['SNR: ' num2str(i)]);
        snr = i;
        channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
        channelOutput = channel(signalIQ);
        message_out = LoRa_Rx(channelOutput,BW,SF,2,Fs,Fc - fc);

        if ~isempty(char(message_out))
            success_symbol = 0;
            for k=1:length(char(message_out))
                if char(message_out(k)) == "0"
                    success_symbol = success_symbol+1;
                end
            end
        end
        SER = 1-success_symbol/zeroNum;
        disp(['SER = ' num2str(SER)]);
        SERAve = SERAve + SER/20;
        
    end
    %res_multi_ser(1,int64((i+39)*10)+1)=i;
    %res_multi_ser(2,int64((i+39)*10)+1)=SERAve;
    %disp([num2str(((i+39)*10+1)*100/61) '% done' ])
    res_multi_ser(1,int64((i+55))+1)=i;
    res_multi_ser(2,int64((i+55))+1)=SERAve;
    disp([num2str(((i+55)+1)*100/11) '% done' ])
end
%% plot
figure
plot(res_multi_ser(1,:),res_multi_ser(2,:))
xlabel('SNR(dB)')
ylabel('SER')