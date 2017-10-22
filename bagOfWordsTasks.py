import codecs
import csv
import ast
import os
import sys
from os import listdir
from os.path import isfile, join

from data import tasks

searched_nodes = [
    "Add", "And", "AssList", "Bitand", "Bitor", "Bitxor", "Break", "CallFunc", "Class", "Compare", "Continue", "Const",
    "Dict", "Div", "For", "FloorDiv", "Function", "If", "Invert", "Keyword", "Lambda", "LeftShift", "List", "ListComp",
    "ListCompFor", "ListCompIf", "Mul", "Mod", "Not", "Or", "Power", "Raise", "RightShift", "Sub", "TryExcept",
    "TryFinally", "UnaryAdd", "UnarySub", "While"
    ]


class AnalyseResults:

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


def analyze_solution(task, results):
    data_vector = {}

    solution = task.solution.replace("\\n", "\n")

    try:
        tree = ast.parse(solution)
        MyVisitor(data_vector).visit(tree)
    except SyntaxError:
        print("ERROR: Failed to parse this line: %", solution)

    results.stats[task.name] = data_vector


def analyze_tasks():
    results = AnalyseResults()
    for task in tasks:
        analyze_solution(task, results)
    print(results)

analyze_tasks()
