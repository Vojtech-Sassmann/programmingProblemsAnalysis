import ast
import codecs
import csv
import seaborn as sns
import ASTParser as Parser
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA
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


def save_data(file_name, groups):
    file_name = file_name[:-3]
    file_name += "csv"

    groups.sort(key=lambda x: x.get_size(), reverse=True)

    with codecs.open(output + file_name, 'w', encoding='UTF-8') as f:
        for group in groups:
            print >> f, str(group.get_size()) + ";" + str(group)


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

    distance_matrix = {}
    labels = []

    save_data(file_name, groups)
    for group in groups:
        print str(len(group.get_trees())) + " -> " + str(group)
        Parser.print_node(group.get_base_tree())
    # for tree in sorted(statistics.data):
    #     print str(tree) + " -> " + str(statistics.data[tree])
    #     labels.append(group.get_base_tree().get_raw())
    #     for other_group in groups:
    #         distance = group.calc_distance(other_group.get_base_tree())
    #         if group not in distance_matrix:
    #             distance_matrix[group] = [distance]
    #         else:
    #             distance_matrix[group].append(distance)
    #
    # print distance_matrix
    # metrics_frame = pd.DataFrame(data=distance_matrix, index=labels)
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

output = "./resources/solutiongroups/ast/8/"
similarity_threshold = 8

analyze_files(similarity_threshold)
