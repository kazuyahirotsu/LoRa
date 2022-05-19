%% qpsk test
pskModulator = comm.PSKModulator(ModulationOrder=4);
sampleNum = 200;
message = randi([0 3],sampleNum,1);
modData = pskModulator(message);
channel = comm.AWGNChannel("NoiseMethod","Signal to noise ratio (SNR)","SNR",-10);
channelOutput = channel(modData);
%scatterplot(modData)
%scatterplot(channelOutput)
pskDemodulator = comm.PSKDemodulator(ModulationOrder=4);
demodData = pskDemodulator(channelOutput);
SER = 1- nnz(message-demodData)/sampleNum;

%% specular
er = 81;
c = physconst("lightspeed");
freq = 920 * 1e6;
ramda = c/freq;
sigmae = 
ec = er - 1i*60*ramda*sigmae;

specular_voltage = ps*sqrt(Gant)*abs(gammav)
