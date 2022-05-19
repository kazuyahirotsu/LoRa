"run this on ipynb"
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data_path='data.csv'
data = pd.read_csv(data_path, names=['RSSI','LATITUDE', 'LONGITUDE'], sep=',')
x=data[['LONGITUDE']]
y=data[['RSSI']]
sample = LinearRegression()
sample.fit(x,y)
plt.scatter(x,y)
plt.plot(x, sample.predict(x),color="red")
plt.xlabel("Longitude")
plt.ylabel("RSSI(dBm)")
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)