import time
import ast
import codecs
import csv
import seaborn as sns
import ASTParser as Parser
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA
import sys

from adjustText import adjust_text
import pandas as pd


class TreeGroup(object):
    def __init__(self, base_tree):
        self.base_tree = base_tree
        self.trees = list()
        self.trees.append(base_tree)

    def calc_distance(self, tree):
        return Parser.calculate_distance(self.base_tree, tree)

    def add_tree(self, tree):
        self.trees.append(tree)

    def __str__(self):
        return self.base_tree.__str__()

    def get_trees(self):
        return self.trees

    def get_base_tree(self):
        return self.base_tree

    def get_size(self):
        return len(self.get_trees())


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Statistics(object):
    def __init__(self, threshold):
        self.groups = []
        self.threshold = threshold

    def add_tree(self, tree):

        best_group = None
        best_distance = None
        if self.threshold == 0:
            new_group = TreeGroup(tree)
            self.groups.append(new_group)
            return

        for group in self.groups:
            if best_distance == 0:
                break
            distance = group.calc_distance(tree)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_group = group
        if best_group is None or best_distance > self.threshold:
            new_group = TreeGroup(tree)
            self.groups.append(new_group)
        else:
            best_group.add_tree(tree)

    def get_groups(self):
        return self.groups


def analyze_solution(raw_solution, statistics):
    solution_string = raw_solution.replace("\\n", "\n")

    try:
        ast_tree = ast.parse(solution_string)
        tree = Parser.parse_tree(ast_tree, raw=solution_string)
        statistics.add_tree(tree)
    except SyntaxError:
        return


def save_details(file_name, groups):
    file_name = file_name[:-3]
    file_name += "csv"

    groups.sort(key=lambda x: x.get_size(), reverse=True)

    for group, i in zip(groups, range(groups.__len__())):
        with codecs.open(output + 'details/' + file_name + '_' + str(i), 'w', encoding='UTF-8') as f:
            print >> f, str(group.get_size()) + ";" + str(group)
            for tree in group.get_trees():
                print >> f, tree.get_raw()


def save_data(file_name, groups):
    file_name = file_name[:-3]
    file_name += "csv"

    groups.sort(key=lambda x: x.get_size(), reverse=True)

    with codecs.open(output + file_name, 'w', encoding='UTF-8') as f:
        for group in groups:
            print >> f, str(group.get_size()) + ";" + str(group)


class SolutionsPair:
    def __init__(self, solution1, solution2):
        self.s1 = solution1
        self.s2 = solution2

    def __hash__(self):
        return self.s1.__hash__() * 31 * self.s2.__hash__()

    def __eq__(self, other):
        if self.s1 == other.s1 and self.s2 == other.s2:
            return True
        if self.s1 == other.s2 and self.s2 == other.s1:
            return True
        return False


def analyze_file(file_name, t):

    statistics = Statistics(t)

    with codecs.open("resources/tasks/parsed/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        previous_code = None

        for line in reader:
            if len(line) is 1:
                code = line[0]
                if code is not None:
                    if previous_code != code:
                        analyze_solution(code, statistics)
                previous_code = code

    groups = statistics.get_groups()

    print "found groups: " + str(len(groups))
    sys.stdout.flush()

    distance_matrix = []
    solutions = []

    # save_data(file_name, groups)
    # save_details(file_name, groups)
    distances_cache = {}
    for group in groups:

        solutions.append(group.get_base_tree().get_raw())
        group_distances = list()

        for other_group in groups:
            # solution_pair = SolutionsPair(group.get_base_tree(), other_group.get_base_tree())

            # check if distance has not already been computed
            # if distances_cache.__contains__(solution_pair):
            #     distance = distances_cache[solution_pair]
            #
            # else:
            distance = group.calc_distance(other_group.get_base_tree())

            # save calculation to cache
            # distances_cache[solution_pair] = distance
            # first iteration
            group_distances.append(distance)
        distance_matrix.append(group_distances)
        print "finished: {}%".format(float(distance_matrix.__len__()) / groups.__len__() * 100)


    # print distance_matrix
    metrics_frame = pd.DataFrame(data=distance_matrix, index=solutions)

    metrics_frame.to_pickle(output + "distances/" + file_name[:-3] + "pkl")

    # show_df(metrics_frame)
    # show_pca(metrics_frame)


def show_df(df):
    cg = sns.clustermap(df)
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
    plt.show()


def show_pca(df):
    model = PCA(n_components=2)
    results = model.fit(df.transpose())

    plt.figure(figsize=(20, 20))
    texts = []
    for i in range(len(df.index)):
        x, y = results.components_[0][i], results.components_[1][i]
        plt.plot(x, y, "o", color="blue")
        texts.append(plt.text(x, y, df.index[i], size=10))

    adjust_text(texts)
    plt.show()


def analyze_files(threshold):
    path = 'resources/tasks/parsed'

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        print f
        analyze_file(f, threshold)

output = "./resources/test/solutiongroups/dbscan/"
similarity_threshold = 0
DBSCAN_MIN_SIZE = 10
DBSCAN_EPSILON = 4
# analyze_files(similarity_threshold)
start_time = time.time()
print "AA: {}%".format(float(52) / 100 * 100)
analyze_file('Dvojnasobek.txt', similarity_threshold)
end_time = time.time()
print "Calculation finished in time: {}s".format(end_time - start_time)
