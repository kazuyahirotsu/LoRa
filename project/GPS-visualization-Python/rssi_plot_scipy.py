import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

data_path='data.csv'
data = pd.read_csv(data_path, names=['RSSI','LATITUDE', 'LONGITUDE'], sep=',')
x=data[['LONGITUDE']]
y=data[['RSSI']]

def func(x, a, b):
    return a + b * np.log(x)

x = x.to_numpy()[:, 0]
y = y.to_numpy()[:, 0]

# a, b = 1.2, 2
# x = np.linspace(0.001, 10, 100)
# y = func(x, a, b) + np.random.normal(0, 0.5, len(x))

popt, pcov = curve_fit(func,x,y) 
print(popt)
y_pred = func(x, popt[0], popt[1])
plt.plot(x,y_pred,color="red")

plt.scatter(x,y)
plt.xlabel("Longitude")
plt.ylabel("RSSI(dBm)")
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.legend(["fit curve","measured value","linear regression of measured value"])
