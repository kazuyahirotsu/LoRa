import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sunny_time = pd.read_csv('sunny_time_10_1_to_9.csv',  sep=',', usecols=[0, 1], names=('datetime', 'sunny'))
sunny_time = sunny_time.fillna(0)
sunny_time['datetime'] = pd.to_datetime(sunny_time['datetime'])
print(sunny_time[0:10])
print(sunny_time.dtypes)
sunny_time.plot(x="datetime",y="sunny")


voltage = pd.read_csv('ambient_10_4_to_9.csv',  sep=',', usecols=[0, 1, 2], names=('date', 'time', 'voltage'), skiprows=1)
voltage['datetime'] = voltage['date'] + voltage['time']
voltage = voltage.drop(columns=['date', 'time'])
voltage['datetime'] = pd.to_datetime(voltage['datetime'], format='%m/%d/%Y %I:%M:%S %p.%f')
print(voltage[1140:])
print(voltage.dtypes)
voltage.plot(x="datetime",y="voltage")


merged_data = pd.merge(sunny_time, voltage, on='datetime', how='outer')
merged_data = merged_data.set_index('datetime').sort_index()
merged_data = merged_data.fillna({'sunny': 0})
print(merged_data[490:])


merged_data["2022-10-05":"2022-10-09"].plot(subplots=True, figsize=(20,4))