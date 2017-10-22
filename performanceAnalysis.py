import pandas as pd
import pylab as plt

data = pd.read_csv("resources/results_swapped.csv", sep=",", index_col=0)
corr = data.corr()

plt.matshow(corr)
plt.show()
corr.to_csv("resources\output.csv")
