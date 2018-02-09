import ast
import re
import codecs
from collections import namedtuple


Task = namedtuple('Task', [
    'task_id',
    'name',
    'solution'
    # ,
    # 'test'
])


def change_state(previous):
    if previous is 0:
        return 1
    if previous is 1:
        return 2
    if previous is 2:
        return 0

with open("resources/Python_zadani.txt", encoding="UTF-8") as f:
    state = 0
    task_id = 0
    task_name = ""
    task = None

    with codecs.open("resources/tasks.txt", 'w', encoding="UTF-8") as o:
        for line in f.readlines():
            if state is 0:
                task_id, task_name = line.split(";")
                task_name = task_name[:-1]
            if state is 1:
                task = line
                # task = task.replace("\\n", "\n")
                task = re.sub(r".*solution:\"", "", task)
                task = re.sub(r"\", attempt.*", "", task)
                # task = re.sub(r"\\", "", task)
            if state is 2:
                t = Task(task_id=task_id, name=task_name, solution=task)
                print(t, file=o)
            state = change_state(state)

class MyVisitor(ast.NodeVisitor):

    data_vector = None

    def generic_visit(self, node):
        node_type = type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)


tree = ast.parse("print(2 * 2)")
MyVisitor().visit(tree)
print(tree)
