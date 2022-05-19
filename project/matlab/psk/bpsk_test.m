%% qpsk test
pskModulator = comm.PSKModulator(ModulationOrder=2);
sampleNum = 200;
message = randi([0 1],sampleNum,1);
modData = pskModulator(message);
channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",-10);
channelOutput = channel(modData);
%scatterplot(modData)
%scatterplot(channelOutput)
pskDemodulator = comm.PSKDemodulator(ModulationOrder=2);
demodData = pskDemodulator(channelOutput);
SER = 1- nnz(message-demodData)/sampleNum;

%% bpsk snr test
snr_start = -40;
snr_end = 20;
res_bpsk=zeros(2,snr_end-snr_start);

pskModulator = comm.PSKModulator(ModulationOrder=2);
sampleNum = 200;
for snr = snr_start:snr_end
    SERAve = 0;
    repNum = 200;
    for i = 1:repNum
        message = randi([0 1],sampleNum,1);
        modData = pskModulator(message);
        channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
        channelOutput = channel(modData);
        mpChan = [0.8 0 0 0 0 0 0 0 -0.5 0 0 0 0 0 0 0 0.34].';
        mpChanOut = filter(mpChan,1,channelOutput);
        %scatterplot(modData)
        %scatterplot(channelOutput)
        pskDemodulator = comm.PSKDemodulator(ModulationOrder=2);
        demodData = pskDemodulator(mpChanOut);
        SER = 1- nnz(message-demodData)/sampleNum;
        SERAve = SER + SER/repNum;
    end
    res_bpsk(1,int64(snr-snr_start)+1)=snr;
    res_bpsk(2,int64(snr-snr_start)+1)=SERAve;
    disp([num2str((snr-snr_start+1)*100/(snr_end-snr_start+1)) '% done' ])
end
figure
plot(res_bpsk(1,:),res_bpsk(2,:))
xlabel('SNR(dB)')
ylabel('SER')
