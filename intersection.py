import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set()


def return_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))
    return intersection

data_1 = pd.read_csv("resources/results_swapped.csv", sep=",", index_col=0)
data_1.sort_index(axis=1, inplace=True)
corr_1 = data_1.corr()


data_2 = pd.read_csv("resources/Python_user_time.csv", sep=",", index_col=0)
data_2.sort_index(axis=1, inplace=True)
corr_2 = data_2.corr()


plt.figure(figsize=(18, 12))
plt.title('User performance spearman', size=15)
sns.heatmap(corr_2, square=True, center=0)
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.show()
