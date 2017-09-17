import codecs
import csv
import ast
import sys
from os import listdir
from os.path import isfile, join

searched_nodes = [
    "Add", "And", "AssList", "Bitand", "Bitor", "Bitxor", "Break", "CallFunc", "Class", "Compare", "Continue", "Const",
    "Dict", "Div", "For", "FloorDiv", "Function", "If", "Invert", "Keyword", "Lambda", "LeftShift", "List", "ListComp",
    "ListCompFor", "ListCompIf", "Mul", "Mod", "Not", "Or", "Power", "Raise", "RightShift", "Sub", "TryExcept",
    "TryFinally", "UnaryAdd", "UnarySub", "While"
    ]


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
        ""'''
        for searched_node in searched_nodes:
            data_vector[searched_node] = 0
        '''""

    def generic_visit(self, node):
        node_type = type(node).__name__
        if node_type in searched_nodes:
            self.increase_data(node_type)
        ast.NodeVisitor.generic_visit(self, node)

    def increase_data(self, key):
        if key not in self.data_vector:
            self.data_vector[key] = 1
        else:
            self.data_vector[key] += 1


def to_data_string(data):
    result = ""
    empty = True
    for key, value in sorted(data.iteritems(), key=lambda x: x[1], reverse=True):
        if value is not 0:
            empty = False
        result += key + ":" + str(value) + ";"
    if empty:
        return ""
    return result


def analyze_solution(solution, results):
    data_vector = {}

    solution = solution.replace("\\n", "\n")

    try:
        tree = ast.parse(solution)
        MyVisitor(data_vector).visit(tree)
        results.parsable += 1
    except SyntaxError:
        return

    result_string = to_data_string(data_vector)
    if result_string not in results.stats:
        results.stats[result_string] = 1
    results.stats[result_string] += 1


def parse_code(line):
    prefix_size = len(line[0])
    return line[2][prefix_size:]


def process_line(line, results):
    code = parse_code(line)

    if code.startswith("SUBMIT"):
        results.submitted += 1
        analyze_solution(code[6:], results)


def check_line(line, results):
    if len(line) is 3:
        process_line(line, results)


def print_results(results):
    print "submitted: %s" % str(results.submitted)
    print "compilable: %s" % str(results.parsable)
    '''"" TODO""'''
    print "correct: %s" % str(results.correct)
    print "\n-----\n"

    number_of_printed_solutions = 5
    for key, value in sorted(results.stats.iteritems(), key=lambda x: x[1], reverse=True):
        if len(key) > 0:
            print key, "-> ", value
            number_of_printed_solutions -= 1
            if number_of_printed_solutions is 0:
                break


def print_header(file_name):
    print ""
    print "--------------------------------------------------------------------------------"
    print "----- ", file_name, " -----"
    print ""


def analyze_file(file_name):

    print_header(file_name)

    results = AnalyseResults()

    with codecs.open("resources/tasks/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        for line in reader:
            check_line(line, results)

    print_results(results)


def analyze_files():
    path = 'resources/tasks/'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f)

csv.field_size_limit(sys.maxint)
analyze_files()
