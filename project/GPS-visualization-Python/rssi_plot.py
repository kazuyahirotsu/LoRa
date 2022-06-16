import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
sim_power = [-83.000, -83.000, -83.050, -83.110, -83.040, -83.160, -83.080, -83.150, -83.220, -83.220, -83.260, -83.330, -83.290, -83.360, -83.480, -83.430, -83.510, -83.460, -83.580, -83.660, -83.610, -83.690, -83.760, -83.760, -83.870, -83.820, -83.910, -84.040, -83.980, -84.080, -84.180, -84.140, -84.260, -84.370, -84.330, -84.430, -84.430, -84.510, -84.620, -84.580, -84.690, -84.830, -84.800, -84.910, -84.870, -85.010, -85.120, -85.080, -85.190, -85.330, -85.300, -85.410, -85.510, -85.510, -85.620, -85.620, -85.730, -85.830, -85.830, -85.940, -86.050, -86.050, -86.160, -86.160, -86.260, -86.370, -86.370, -86.480, -86.610, -86.580, -86.710, -86.830, -86.830, -86.940, -86.940, -87.050, -87.160, -87.160, -87.260, -87.390, -87.390, -87.510, -87.620, -87.620, -87.730, -87.730, -87.830, -87.960, -87.970, -88.070, -88.190, -88.190, -88.300, -88.300, -88.410, -88.510, -88.510, -88.640, -88.750, -88.760, -88.870, -88.980, -88.980, -89.080, -89.080, -89.210, -89.320, -89.320, -89.430, -89.540, -89.550, -89.660, -89.660, -89.760, -89.870, -89.890, -89.980,-90.080,-90.080,-90.210,-90.320,-90.320,-90.410,-90.440,-90.540,-90.620,-90.640,-90.750,-90.750]
sim_power.reverse()

data_path='data.csv'
data = pd.read_csv(data_path, names=['RSSI','LATITUDE', 'LONGITUDE'], sep=',')
x=data[['LONGITUDE']]
y=data[['RSSI']]
sample = LinearRegression()
sample.fit(x,y)

sim_power = [-83.000, -83.000, -83.050, -83.110, -83.040, -83.160, -83.080, -83.150, -83.220, -83.220, -83.260, -83.330, -83.290, -83.360, -83.480, -83.430, -83.510, -83.460, -83.580, -83.660, -83.610, -83.690, -83.760, -83.760, -83.870, -83.820, -83.910, -84.040, -83.980, -84.080, -84.180, -84.140, -84.260, -84.370, -84.330, -84.430, -84.430, -84.510, -84.620, -84.580, -84.690, -84.830, -84.800, -84.910, -84.870, -85.010, -85.120, -85.080, -85.190, -85.330, -85.300, -85.410, -85.510, -85.510, -85.620, -85.620, -85.730, -85.830, -85.830, -85.940, -86.050, -86.050, -86.160, -86.160, -86.260, -86.370, -86.370, -86.480, -86.610, -86.580, -86.710, -86.830, -86.830, -86.940, -86.940, -87.050, -87.160, -87.160, -87.260, -87.390, -87.390, -87.510, -87.620, -87.620, -87.730, -87.730, -87.830, -87.960, -87.970, -88.070, -88.190, -88.190, -88.300, -88.300, -88.410, -88.510, -88.510, -88.640, -88.750, -88.760, -88.870, -88.980, -88.980, -89.080, -89.080, -89.210, -89.320, -89.320, -89.430, -89.540, -89.550, -89.660, -89.660, -89.760, -89.870, -89.890, -89.980,-90.080,-90.080,-90.210,-90.320,-90.320,-90.410,-90.440,-90.540,-90.620,-90.640,-90.750,-90.750]
sim_power.reverse()
sim_longitude = np.linspace(139.776857,139.782648,129)
plt.plot(sim_longitude,sim_power,color="orange")
plt.scatter(x,y)
plt.plot(x, sample.predict(x),color="red")
plt.xlabel("Longitude")
plt.ylabel("RSSI(dBm)")
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.legend(["simulation","measured value","linear regression of measured value"])