#!/usr/bin/python3

from adjustText import adjust_text
import pandas as pd
from sklearn.decomposition import PCA
import pylab as plt

data = pd.read_csv("resources/results.csv", sep=";", index_col=0)

model = PCA(n_components=2)
results = model.fit(data.transpose())

plt.figure(figsize=(20, 20))
texts = []
for i in range(len(data.index)):
    x, y = results.components_[0][i], results.components_[1][i]
    plt.plot(x, y, "o", color="blue")
    texts.append(plt.text(x, y, data.index[i], size=10))

adjust_text(texts)
plt.show()




