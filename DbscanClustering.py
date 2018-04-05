import time
import ast
import codecs
import csv
import ASTParser as Parser
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA
import numpy as np
import sys

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from adjustText import adjust_text
import pandas as pd


def cluster_dbscan(distance_matrix, file_name):
    try:
        db = DBSCAN(metric='precomputed', min_samples=DBSCAN_MIN_SIZE, eps=DBSCAN_EPSILON).fit(distance_matrix)
    except:
        print "Using default values"
        db = DBSCAN(metric='precomputed').fit(distance_matrix)

    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    for cluster, solution in zip(db.labels_, distance_matrix.index.values):
        if cluster is not -1:
            with codecs.open(path + file_name + "_" + str(cluster), 'a', encoding='UTF-8') as f:
                print >> f, solution

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    # for k, col in zip(unique_labels, colors):
    #     if k == -1:
    #         # Black used for noise.
    #         col = [0, 0, 0, 1]
    #
    #

    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    project(distance_matrix, labels)


def project(distance_matrix, labels):
    model = PCA(n_components=2)
    results = model.fit(distance_matrix.transpose())

    plt.figure(figsize=(20, 20))
    texts = []

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for i in range(len(distance_matrix.index)):
        x, y = results.components_[0][i], results.components_[1][i]
        color = colors[labels[i]]
        if labels[i] == -1:
            color = [0, 0, 0, 1]
        plt.plot(x, y, "o", markerfacecolor=tuple(color), markeredgecolor='k')
        # texts.append(plt.text(x, y, distance_matrix.index[i], size=10))

    adjust_text(texts)
    plt.show()


def analyze_file(file_name):
    df = pd.read_pickle(path + "distances/" + file_name)
    cluster_dbscan(df, file_name)


path = "./resources/test/solutiongroups/dbscan/"
DBSCAN_MIN_SIZE = 5
DBSCAN_EPSILON = 0.5

analyze_file("Dvojnasobek.pkl")