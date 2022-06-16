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
er = 3; %surface dielectric constant
c = physconst("lightspeed");
freq = 920 * 1e6;
ramda = c/freq; %wavelength
sigmae = 0.001; %surface conductivity
psi = 0.1; %grazing angle
sigmah = 0.3; %rms surface height variation
Gant = 1;

ec = er - 1i*60*ramda*sigmae;
Ps = 2*(2*pi*sigmah*sin(psi)/ramda)^2;
ps = exp(-Ps)*besseli(0,Ps);
gammav = (ec*sin(psi)-sqrt(ec-cos(psi)^2))/(ec*sin(psi)+sqrt(ec-cos(psi)^2));
gammah = (sin(psi)-sqrt(ec-cos(psi)^2))/(sin(psi)+sqrt(ec-cos(psi)^2));
specular_direct_voltage = ps*sqrt(Gant)*abs(gammav);

%% diffuse

diffuse_direct_voltage = 

