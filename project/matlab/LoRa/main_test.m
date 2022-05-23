%% big multipath SER test
SF = 10 ;
BW = 125e3 ;
fc = 915e6 ;
Power = 14 ;
message = "000000000000000000000000000000000000000000" ;
zeroNum = strlength(message);
Fs = 10e6 ;
Fc = 921.5e6 ;
res_multi_ser=zeros(2,21);
for i=-60:-40
    SERAve = 0;
    for j=1:20
        signalIQ = LoRa_Tx(message,BW,SF,Power,Fs,Fc - fc);
        %mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        %mpChanOut = filter(mpChan,1,signalIQ);
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
        SERAve = SERAve + SER/20;
    end
    disp(['SNR: ' num2str(i)]);
    disp(['SER: ' num2str(SERAve)]);
    res_multi_ser(1,int64((i+60))+1)=i;
    res_multi_ser(2,int64((i+60))+1)=SERAve;
    disp([num2str(((i+60)+1)*100/11) '% done' ])
end
%% bpsk snr test
snr_start = -60;
snr_end = 30;
res_bpsk=zeros(2,snr_end-snr_start);

pskModulator = comm.PSKModulator(ModulationOrder=2);
sampleNum = 200;
for snr = snr_start:snr_end
    SERAve = 0;
    repNum = 20;
    for i = 1:repNum
        message = randi([0 1],sampleNum,1);
        modData = pskModulator(message);
        channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
        channelOutput = channel(modData);
        %mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        %mpChanOut = filter(mpChan,1,channelOutput);
        pskDemodulator = comm.PSKDemodulator(ModulationOrder=2);
        %demodData = pskDemodulator(mpChanOut);
        demodData = pskDemodulator(channelOutput);
        SER = nnz(message-demodData)/sampleNum;
        SERAve = SERAve + SER/repNum;
    end
    res_bpsk(1,int64(snr-snr_start)+1)=snr;
    res_bpsk(2,int64(snr-snr_start)+1)=SERAve;
    disp([num2str((snr-snr_start+1)*100/(snr_end-snr_start+1)) '% done' ])
end
%% qpsk snr test
snr_start = -60;
snr_end = 30;
res_qpsk=zeros(2,snr_end-snr_start);

pskModulator = comm.PSKModulator(ModulationOrder=4);
sampleNum = 200;
for snr = snr_start:snr_end
    SERAve = 0;
    repNum = 200;
    for i = 1:repNum
        message = randi([0 3],sampleNum,1);
        modData = pskModulator(message);
        channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
        channelOutput = channel(modData);
        %mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        %mpChanOut = filter(mpChan,1,channelOutput);
        pskDemodulator = comm.PSKDemodulator(ModulationOrder=4);
        %demodData = pskDemodulator(mpChanOut);
        demodData = pskDemodulator(channelOutput);
        SER = nnz(message-demodData)/sampleNum;
        SERAve = SERAve + SER/repNum;
    end
    res_qpsk(1,int64(snr-snr_start)+1)=snr;
    res_qpsk(2,int64(snr-snr_start)+1)=SERAve;
    disp([num2str((snr-snr_start+1)*100/(snr_end-snr_start+1)) '% done' ])
end
plot(res_qpsk(1,:),res_qpsk(2,:))
%% plot
figure
plot(res_multi_ser(1,:),res_multi_ser(2,:))
xlabel('SNR(dB)')
ylabel('SER')

hold on
plot(res_bpsk(1,:),res_bpsk(2,:))
plot(res_qpsk(1,:),res_qpsk(2,:))
legend("LoRa","bpsk","qpsk")
