import csv
import ast


searched_nodes = ["Add", "And", "Assign", "Break", "Class", "Compare", "Continue", "Dict", "Div", "For", "Function",
                  "If", "List", "Mul", "Mod", "Sub", "TryExcept", "TryFinally"]


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


def analyze_solution(stats, solution):
    data_vector = {}

    solution = solution.replace("\\n", "\n")

    try:
        tree = ast.parse(solution)
        MyVisitor(data_vector).visit(tree)
    except SyntaxError:
        return

    result_string = to_data_string(data_vector)
    if result_string not in stats:
        stats[result_string] = 1
    stats[result_string] += 1


def parse_code(line):
    prefix_size = len(line[0])
    return line[2][prefix_size:]


def process_line(stats, line):
    code = parse_code(line)

    if code.startswith("SUBMIT"):
        analyze_solution(stats, code[6:])


def check_line(stats, line):
    if len(line) is 3:
        process_line(stats, line)


def read_file():

    stats = {}

    f = open("tasks/Faktorial.txt", 'r')
    try:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            check_line(stats, line)
    finally:
        f.close()

    for key, value in sorted(stats.iteritems(), key=lambda x: x[1], reverse=True):
        if len(key) > 0:
            print key, "-> ", value


read_file()
