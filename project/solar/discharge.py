import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

battery_voltage = 12.788

data = pd.read_csv('battery_discharge.csv',  sep=',')
y=data['voltage'].astype(float)
y.plot()
y_sorted = y.sort_values()
print(
    "battery remaining: "
    + str((y_sorted.searchsorted(battery_voltage, side='right')+y_sorted.searchsorted(battery_voltage, side='left'))/(2*len(y_sorted)))
    )