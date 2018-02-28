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

# searched_nodes = [
#     "+", "-", "*", "/", "for", "while", "print", "%", "if", "==", "is"
# ]

searched_nodes = [
    "Add", "Sub", "Mult", "Div", "For", "While", "Print", "Mod", "If", "Eq", "Is",
]

output_path = "resources/tmp/test.csv"
binary = False
# solution_number = 1
avarage_number = 5
minimal_vector_size = 2
minimal_submitted = 300
parsed_solutions_mode = True
minimal_parsable = 10
skip_print = False


class Solution:
    def __init__(self, data_vector):
        self.data_vector = data_vector
        self.examples = []
        self.count = 1

    def __hash__(self):
        return self.data_vector.__hash__()

    def __eq__(self, other):
        return self.data_vector.__eq__(other.data_vector)

    def add_solution(self, solution):
        self.examples.append(solution)


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

    try:
        tree = ast.parse(solution_string)
        MyVisitor(data_vector).visit(tree)
        results.parsable += 1
    except SyntaxError:
        return

    result = HashableDict(data_vector)
    solution = Solution(result)

    if calculate_vector_size(result) >= minimal_vector_size:
        if solution not in results.solutions:
            solution.add_solution(raw_solution)
            results.solutions[solution] = 1
        else:
            results.solutions[solution] += 1
            for s in results.solutions:
                if s.__eq__(solution):
                    s.add_solution(raw_solution)


def parse_code(line):
    prefix_size = len(line[0])
    solution = line[2][prefix_size:]
    if solution.startswith("SUBMIT"):
        return solution[6:]
    else:
        return None


def print_results(results):
    print("submitted: %s" % str(results.submitted))
    print("parsable: %s" % str(results.parsable))
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
    print("--------------------------------------------------------------------------------")
    print("----- ", file_name, " -----")


def save_results(results, file_name):
    if results.submitted < minimal_submitted:
        return
    if results.parsable < minimal_parsable:
        return

    with codecs.open(output_path, 'a') as f:
        counter = 0
        average_data_vector = None
        f.write(file_name[:-4] + ";")
        sorted_solutions = sorted(results.solutions.items(), key=lambda x: x[1], reverse=True)
        for solution, value in sorted_solutions:
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
            average_data_vector[key] /= float(counter)
        first = True
        for node_type in searched_nodes:
            if first:
                f.write(str('%.2f' % average_data_vector[node_type]))
                first = False
            else:
                f.write(";" + str('%.2f' % average_data_vector[node_type]))

        f.write("\n")


def save_solutions(results, file_name):
    number_of_printed_feature_vectors = 500
    number_of_printed_feature_solutions = 20

    with codecs.open("resources/tmp/solutions/" + file_name, 'w', encoding="UTF-8") as f:
        for solution, count in sorted(results.solutions.items(), key=lambda x: x[1], reverse=True):
            if len(solution.data_vector) > 0:
                print >> f, solution.data_vector, count
                for example in solution.examples:
                    number_of_printed_feature_solutions -= 1
                    # print >> f, example
                    if number_of_printed_feature_solutions <= 0:
                        number_of_printed_feature_solutions = 20
                        break
                number_of_printed_feature_vectors -= 1
                if number_of_printed_feature_vectors == 0:
                    break


def analyze_file(file_name):

    print_header(file_name)

    results = AnalyseResults()

    with codecs.open("resources/tasks/parsed/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        previous_code = None

        for line in reader:
            if parsed_solutions_mode:
                if len(line) is 1:
                    code = line[0]
                    if code is not None:
                        if previous_code != code:
                            analyze_solution(code, results)
                    previous_code = code
            else:
                if len(line) is 3:
                    code = parse_code(line)
                    if code is not None:
                        if previous_code != code:
                            analyze_solution(code, results)
                    previous_code = code

    if not skip_print:
        print_results(results)
    save_solutions(results, file_name)
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
        # print(header, file=f)
        print >> f, header


def analyze_files():
    path = 'resources/tasks/parsed'

    save_header()

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f)


analyze_files()
