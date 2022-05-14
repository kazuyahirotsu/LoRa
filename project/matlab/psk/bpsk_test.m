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

%% qpsk snr test
snr_start = -40;
snr_end = 20;
res_qpsk=zeros(2,snr_end-snr_start);

pskModulator = comm.PSKModulator(ModulationOrder=2);
sampleNum = 2000;
for snr = snr_start:snr_end
    SERAve = 0;
    repNum = 200;
    for i = 1:repNum
        message = randi([0 1],sampleNum,1);
        modData = pskModulator(message);
        channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",snr);
        channelOutput = channel(modData);
        %scatterplot(modData)
        %scatterplot(channelOutput)
        pskDemodulator = comm.PSKDemodulator(ModulationOrder=2);
        demodData = pskDemodulator(channelOutput);
        SER = 1- nnz(message-demodData)/sampleNum;
        SERAve = SER + SER/repNum;
    end
    res_qpsk(1,int64(snr-snr_start)+1)=snr;
    res_qpsk(2,int64(snr-snr_start)+1)=SERAve;
    disp([num2str((snr-snr_start+1)*100/(snr_end-snr_start+1)) '% done' ])
end
figure
plot(res_qpsk(1,:),res_qpsk(2,:))
xlabel('SNR(dB)')
ylabel('SER')