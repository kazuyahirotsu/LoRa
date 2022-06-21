import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# lon0, lat0 = 35.650798, 139.779477
lon0, lat0 = 38.721527, 141.092104
r = 6378.137*1000
data_path='data_6_16_2.csv'
data = pd.read_csv(data_path, names=['RSSI','LONGITUDE', 'LATITUDE'], sep=',')

data['DISTANCE'] = r*np.arccos(np.sin(lat0*np.pi/180)*np.sin(data['LATITUDE']*np.pi/180)+np.cos(lat0*np.pi/180)*np.cos(data['LATITUDE']*np.pi/180)*np.cos(lon0*np.pi/180-data['LONGITUDE']*np.pi/180))

x=data[['DISTANCE']]
y=data[['RSSI']]

sample = LinearRegression()
sample.fit(x,y)

#sim_power = [-83.000, -83.000, -83.050, -83.110, -83.040, -83.160, -83.080, -83.150, -83.220, -83.220, -83.260, -83.330, -83.290, -83.360, -83.480, -83.430, -83.510, -83.460, -83.580, -83.660, -83.610, -83.690, -83.760, -83.760, -83.870, -83.820, -83.910, -84.040, -83.980, -84.080, -84.180, -84.140, -84.260, -84.370, -84.330, -84.430, -84.430, -84.510, -84.620, -84.580, -84.690, -84.830, -84.800, -84.910, -84.870, -85.010, -85.120, -85.080, -85.190, -85.330, -85.300, -85.410, -85.510, -85.510, -85.620, -85.620, -85.730, -85.830, -85.830, -85.940, -86.050, -86.050, -86.160, -86.160, -86.260, -86.370, -86.370, -86.480, -86.610, -86.580, -86.710, -86.830, -86.830, -86.940, -86.940, -87.050, -87.160, -87.160, -87.260, -87.390, -87.390, -87.510, -87.620, -87.620, -87.730, -87.730, -87.830, -87.960, -87.970, -88.070, -88.190, -88.190, -88.300, -88.300, -88.410, -88.510, -88.510, -88.640, -88.750, -88.760, -88.870, -88.980, -88.980, -89.080, -89.080, -89.210, -89.320, -89.320, -89.430, -89.540, -89.550, -89.660, -89.660, -89.760, -89.870, -89.890, -89.980,-90.080,-90.080,-90.210,-90.320,-90.320,-90.410,-90.440,-90.540,-90.620,-90.640,-90.750,-90.750]
# sim_power = [-83.25, -83.250, -83.290, -83.330, -83.230, -83.370, -83.290, -83.330, -83.390, -83.300, -83.440, -83.500, -83.430, -83.480, -83.480, -83.550, -83.620, -83.550, -83.690, -83.620, -83.690, -83.760, -83.690, -83.830, -83.770, -83.860, -83.940, -83.940, -84.010, -83.970, -84.050, -84.140, -84.140, -84.220, -84.160, -84.260, -84.400, -84.360, -84.440, -84.550, -84.500, -84.640, -84.590, -84.690, -84.800, -84.800, -84.900, -84.860, -84.960, -85.070, -85.070, -85.160, -85.140, -85.250, -85.370, -85.340, -85.460, -85.440, -85.570, -85.680, -85.660, -85.760, -85.730, -85.870, -85.980, -85.960, -86.070, -86.190, -86.190, -86.300, -86.270, -86.400, -86.510, -86.510, -86.620, -86.610, -86.730, -86.830, -86.830, -86.940, -86.940, -87.050, -87.160, -87.160, -87.270, -87.270, -87.390, -87.510, -87.510, -87.620, -87.620, -87.730, -87.830, -87.830, -87.960, -88.070, -88.070, -88.190, -88.190, -88.300, -88.410, -88.410, -88.520, -88.520, -88.640, -88.750, -88.760, -88.860, -88.870, -88.980, -89.080, -89.090, -89.190, -89.210, -89.320]
# sim_distance = []
# for i in range(len(sim_power)):
#     sim_distance.append(np.sqrt(460.36**2+(i*5)**2))
# print(sim_distance)
# plt.plot(sim_distance,sim_power,color="orange")
plt.scatter(x,y)
plt.plot(x, sample.predict(x),color="red")
plt.xlabel("Distance from Tx(m)")
plt.ylabel("RSSI(dBm)")
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.legend(["simulation","measured value","linear regression of measured value"])
plt.legend(["measured value","linear regression of measured value"])