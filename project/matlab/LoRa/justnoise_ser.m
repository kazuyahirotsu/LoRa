%% big noise (without multipath) ser test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "0" ;
zeroNum = strlength(message);
Fs = 10e6 ;
Fc = 921.5e6 ;

low_snr = -45;
high_snr = -30;
snr_num = (high_snr - low_snr)*10 + 1;
simulation_num = 2;
res_justnoise_ser=zeros(2,snr_num);

for i=low_snr:0.1:high_snr
    SERAve = 0;
    for j=1:simulation_num
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        Snr = i;
        noise = randn(size(signalIQ))*std(signalIQ)/db2mag(Snr);
        s = signalIQ+noise;
        message_out = LoRa_Rx(s,BW,SF,2,Fs,Fc - fc);

        SER = 0;
        if ~isempty(char(message_out))
            for k=1:length(char(message_out))
                if char(message_out(k)) == "0"
                    SER = SER + (1/zeroNum);
                end
            end
        end
        SERAve = SERAve + SER/simulation_num;
    end
    res_justnoise_ser(1,int64((i-low_snr)*10)+1)=i;
    res_justnoise_ser(2,int64((i-low_snr)*10)+1)=SERAve;
    disp([num2str(((i-low_snr)*10+1)*100/snr_num) '% done' ])
end
%% plot
figure
plot(res_justnoise_ser(1,:),res_justnoise_ser(2,:))
xlabel('SNR(dB)')
ylabel('SER')