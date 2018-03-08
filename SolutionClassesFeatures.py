import csv
from os import listdir
from os.path import isfile, join
import codecs


searched_features = [
    "+", "-", "*", "/", "for", "while", "print", "%", "if", "==", "is"
]


class FeaturesGroup(object):
    def __init__(self, base_features):
        self.base_features = base_features
        self.features_vectors = list()
        self.features_vectors.append(base_features)

    def calc_distance(self, features):
        distance = 0
        for f in searched_features:
            if self.base_features[f] != features[f]:
                distance += 1
        return distance

    def add_features(self, tree):
        self.features_vectors.append(tree)

    def __str__(self):
        return self.base_features.__str__()

    def get_features_vectors(self):
        return self.features_vectors

    def get_base_features(self):
        return self.base_features

    def get_size(self):
        return len(self.features_vectors)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Statistics(object):
    def __init__(self, threshold):
        self.groups = list()
        self.threshold = threshold

    def add_features(self, features):
        best_group = None
        best_distance = None
        for group in self.groups:
            if best_distance == 0:
                break
            distance = group.calc_distance(features)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_group = group
        if best_group is None or best_distance > self.threshold:
            new_group = FeaturesGroup(features)
            self.groups.append(new_group)
        else:
            best_group.add_features(features)

    def get_groups(self):
        return self.groups


def find_features(solution):
    features = {}
    for feature in searched_features:
        features[feature] = solution.count(feature)
        if features[feature] > 1:
            features[feature] = 1
    return features


def analyze_solution(solution, statistics):
    features = find_features(solution)
    statistics.add_features(features)


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

    save_data(file_name, groups)
    for group in groups:
        print(group)
        print(group.get_size())
    #     print str(len(group.get_trees())) + " -> " + str(group)
    #     Parser.print_node(group.get_base_tree())


def save_data(file_name, groups):
    file_name = file_name[:-3]
    file_name += "csv"

    groups.sort(key=lambda x: x.get_size(), reverse=True)

    with codecs.open(output + file_name, 'w', encoding='UTF-8') as f:
        for group in groups:

            f.write(str(group.get_size()) + ";" + str(group))
            f.write('\n')


def analyze_files(threshold):
    path = 'resources/tasks/parsed'

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f, threshold)


output = "./resources/solutiongroups/features/2/"
similarity_threshold = 2

analyze_files(similarity_threshold)
