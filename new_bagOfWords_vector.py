import codecs
import csv
import ast
import os
import math
import sys
from os import listdir
from os.path import isfile, join

from data import tasks

searched_nodes = [
    "+", "-", "*", "/", "for", "while", "print", "%", "if", "==", "is"
]
# searched_nodes = [
#     "Add", "And", "AssList", "Bitand", "Bitor", "Bitxor", "Break", "CallFunc", "Class", "Compare", "Continue", "Const",
#     "Dict", "Div", "For", "FloorDiv", "Function", "If", "Invert", "Keyword", "Lambda", "LeftShift", "List", "ListComp",
#     "ListCompFor", "ListCompIf", "Mul", "Mod", "Not", "Or", "Power", "Raise", "RightShift", "Sub", "TryExcept",
#     "TryFinally", "UnaryAdd", "UnarySub", "While"
# ]


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class AnalyseResults:
    submitted = 0
    parsable = 0
    correct = 0

    stats = {}

    def __init__(self):
        self.stats = {}


class MyVisitor(ast.NodeVisitor):
    data_vector = None

    def __init__(self, data_vector):
        self.data_vector = data_vector
        for searched_node in searched_nodes:
            data_vector[searched_node] = 0.0

    def generic_visit(self, node):
        node_type = type(node).__name__
        if node_type in searched_nodes:
            self.increase_data(node_type)
        ast.NodeVisitor.generic_visit(self, node)

    def increase_data(self, key):
        if self.data_vector[key] == 0.0:
            self.data_vector[key] = 1.0
        else:
            if not binary:
                self.data_vector[key] += 1


def to_data_string(data):
    result = ""
    count = 0
    for key, value in data.items():
        if value > 0:
            count += 1
        result += str(value) + ";"
    if count < 1:
        return ""
    result = result[:-1]
    return result


def check_features(solution, data_vector):
    for node in searched_nodes:
        data_vector[node] = solution.count(node)
        if binary:
            if data_vector[node] > 0:
                data_vector[node] = 1


def calculate_vector_size(v):
    size = 0
    for key in v:
        size += v[key]
    return size


def analyze_solution(solution, results):
    data_vector = {}
    results.submitted += 1
    solution = solution.replace("\\n", "\n")

    check_features(solution, data_vector)

    result = HashableDict(data_vector)

    if calculate_vector_size(result) >= minimal_vector_size:
        if result not in results.stats:
            results.stats[result] = 1
        results.stats[result] += 1


def parse_code(line):
    prefix_size = len(line[0])
    return line[2][prefix_size:]


def print_results(results):
    print("submitted: %s" % str(results.submitted))
    print("compilable: %s" % str(results.parsable))
    '''"" TODO""'''
    # print("correct: %s" % str(results.correct))
    # print("\n-----\n")

    number_of_printed_solutions = 5
    for key, value in sorted(results.stats.items(), key=lambda x: x[1], reverse=True):
        if len(key) > 0:
            print(key, "-> ", value)
            number_of_printed_solutions -= 1
            if number_of_printed_solutions is 0:
                break


def print_header(file_name):
    # print("")
    print("--------------------------------------------------------------------------------")
    print("----- ", file_name, " -----")
    # print("")


def save_results(results, file_name):
    if results.submitted < submission_limit:
        return

    with codecs.open(output_path, 'a') as f:
        counter = 1
        n_solution = None
        f.write(file_name[:-4] + ";")
        for solution, value in sorted(results.stats.items(), key=lambda x: x[1], reverse=True):
            if counter == solution_number:
                n_solution = solution
            counter += 1

        # for key in n_solution:
        #     if n_solution[key] != 0:
        #         n_solution[key] += 1
        #         n_solution[key] = math.log(n_solution[key], 2)
        first = True
        for key in sorted(n_solution):
            if first:
                f.write(str(n_solution[key]))
                first = False
            else:
                f.write(";" + str(n_solution[key]))
        f.write("\n")


def analyze_file(file_name):
    print_header(file_name)

    results = AnalyseResults()

    with codecs.open("resources/tasks/parsed/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='♠', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) == 1:
                analyze_solution(line[0], results)

    print_results(results)
    save_results(results, file_name)


def save_header():
    """prepare output file"""
    header = "name"
    with codecs.open(output_path, 'w') as f:
        for node in sorted(searched_nodes):
            header += ";"
            header += node
        print(header, file=f)


def analyze_files():
    path = 'resources/tasks/parsed/'

    save_header()

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f)

minimal_vector_size = 2
run = True
binary = False
output_path = "resources/parsed/results10.csv"
solution_number = 1
submission_limit = 300
if run:
    analyze_files()
