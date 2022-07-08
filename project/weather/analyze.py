import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_path='data.csv'
data = pd.read_csv(data_path, names=['date','sunny', 'a', 'b'], sep=',')

x=data[['date']]
y=data[['sunny']]

print("averave hours = "+str(np.mean(y)))
plt.hist(y, range=(0,14), bins=28)