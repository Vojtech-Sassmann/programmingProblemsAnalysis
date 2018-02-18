import codecs
import csv
import ast
import os
import sys
import math
from os import listdir
from os.path import isfile, join
from collections import namedtuple

from data import tasks

searched_nodes = [
    "+", "-", "*", "/", "for", "while", "print", "%", "if", "==", "is"
]

# searched_nodes = [
#     "Add", "And", "AssList", "Bitand", "Bitor", "Bitxor", "Break", "CallFunc", "Class", "Compare", "Continue", "Const",
#     "Dict", "Div", "For", "FloorDiv", "Function", "If", "Invert", "Keyword", "Lambda", "LeftShift", "List", "ListComp",
#     "ListCompFor", "ListCompIf", "Mul", "Mod", "Not", "Or", "Power", "Raise", "RightShift", "Sub", "TryExcept",
#     "TryFinally", "UnaryAdd", "UnarySub", "While"
#     ]

output_path = "resources/tmp/top1.csv"
binary = False
# solution_number = 1
avarage_number = 1
minimal_vector_size = 2
minimal_subbmited = 300


class Solution:
    def __init__(self, data_vector, example):
        self.data_vector = data_vector
        self.example = example
        self.count = 1

    def __hash__(self):
        return self.data_vector.__hash__()

    def __eq__(self, other):
        return self.data_vector.__eq__(other.data_vector)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class AnalyseResults:
    def __init__(self):
        self.submitted = 0
        self.parsable = 0
        self.correct = 0
        self.solutions = {}


class MyVisitor(ast.NodeVisitor):

    data_vector = None

    def __init__(self, data_vector):
        self.data_vector = data_vector
        for searched_node in searched_nodes:
            data_vector[searched_node] = 0

    def generic_visit(self, node):
        node_type = type(node).__name__
        if node_type in searched_nodes:
            self.increase_data(node_type)
        ast.NodeVisitor.generic_visit(self, node)

    def increase_data(self, key):
        if self.data_vector[key] == 0:
            self.data_vector[key] = 1
        else:
            if not binary:
                self.data_vector[key] += 1


def to_data_string(data):
    result = ""
    empty = True
    for key, value in data.items():
        if value > 0:
            empty = False
        result += str(value) + ";"
    if empty:
        return ""
    result = result[:-1]
    return result


def check_features(solution, data_vector):
    for node in searched_nodes:
        data_vector[node] = solution.count(node)
        if binary:
            if data_vector[node] > 0:
                data_vector[node] = 1


def analyze_solution(raw_solution, results):
    data_vector = {}
    results.submitted += 1
    solution_string = raw_solution.replace("\\n", "\n")

    check_features(solution_string, data_vector)

    result = HashableDict(data_vector)
    solution = Solution(result, solution_string)

    if calculate_vector_size(result) >= minimal_vector_size:
        if solution not in results.solutions:
            results.solutions[solution] = 1
        else:
            results.solutions[solution] += 1

#
# def analyze_solution(raw_solution, results):
#     data_vector = {}
#
#     solution = raw_solution.replace("\\n", "\n")
#
#     try:
#         tree = ast.parse(solution)
#         MyVisitor(data_vector).visit(tree)
#         results.parsable += 1
#     except SyntaxError:
#         return
#
#     # result = to_data_string(data_vector)
#     result = HashableDict(data_vector)
#     if result not in results.stats:
#         results.stats[result] = 1
#     results.stats[result] += 1


def parse_code(line):
    prefix_size = len(line[0])
    return line[2][prefix_size:]


def process_line(line, results):
    code = parse_code(line)

    if code.startswith("SUBMIT"):
        analyze_solution(code[6:], results)


def check_line(line, results):
    if len(line) is 3:
        process_line(line, results)


def print_results(results):
    print("submitted: %s" % str(results.submitted))
    print("compilable: %s" % str(results.parsable))
    '''"" TODO""'''
    # print("correct: %s" % str(results.correct))
    # print("\n-----\n")
    #
    number_of_printed_solutions = 5
    for solution, count in sorted(results.solutions.items(), key=lambda x: x[1], reverse=True):
        if len(solution.data_vector) > 0:
            print(solution.data_vector, "-> ", count)
            number_of_printed_solutions -= 1
            if number_of_printed_solutions is 0:
                break


def print_header(file_name):
    # print("")
    print("--------------------------------------------------------------------------------")
    print("----- ", file_name, " -----")
    # print("")


def save_results(results, file_name):
    if results.submitted < minimal_subbmited:
        return

    with codecs.open(output_path, 'a') as f:
        counter = 0
        average_data_vector = None
        f.write(file_name[:-4] + ";")
        for solution, value in sorted(results.solutions.items(), key=lambda x: x[1], reverse=True):
            counter += 1
            data_vector = solution.data_vector
            if counter == 1:
                average_data_vector = data_vector
            else:
                for key in data_vector:
                    average_data_vector[key] += data_vector[key]
            if counter == avarage_number:
                break
        for key in average_data_vector:
            average_data_vector[key] /= counter
        first = True
        for key in average_data_vector:
            if first:
                f.write(str('%.2f' % average_data_vector[key]))
                first = False
            else:
                f.write(";" + str('%.2f' % average_data_vector[key]))
        f.write("\n")


def analyze_file(file_name):

    print_header(file_name)

    results = AnalyseResults()

    with codecs.open("resources/tasks/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        for line in reader:
            check_line(line, results)

    print_results(results)
    save_results(results, file_name)


def calculate_vector_size(v):
    size = 0
    for key in v:
        size += v[key]
    return size


def save_header():
    """prepare output file"""
    header = "name"
    with codecs.open(output_path, 'w') as f:
        for node in searched_nodes:
            header += ";"
            header += node
        print(header, file=f)


def analyze_files():
    path = 'resources/tasks'

    save_header()

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f)


analyze_files()
