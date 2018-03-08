import ast
import codecs
from os import listdir

from os.path import isfile, join

from ASTParser import MyNode
import ASTParser as Parser


# Task = namedtuple('Task', [
#     'task_id',
#     'name',
#     'solution'
#     # ,
#     # 'test'
# ])

#
# def change_state(previous):
#     if previous is 0:
#         return 1
#     if previous is 1:
#         return 2
#     if previous is 2:
#         return 0

# with open("resources/Python_zadani.txt", encoding="UTF-8") as f:
#     state = 0
#     task_id = 0
#     task_name = ""
#     task = None
#
#     with codecs.open("resources/tasks.txt", 'w', encoding="UTF-8") as o:
#         for line in f.readlines():
#             if state is 0:
#                 task_id, task_name = line.split(";")
#                 task_name = task_name[:-1]
#             if state is 1:
#                 task = line
#                 # task = task.replace("\\n", "\n")
#                 task = re.sub(r".*solution:\"", "", task)
#                 task = re.sub(r"\", attempt.*", "", task)
#                 # task = re.sub(r"\\", "", task)
#             if state is 2:
#                 t = Task(task_id=task_id, name=task_name, solution=task)
#                 print(t, file=o)
#             state = change_state(state)

# tree = ast.parse("def vyhodnot(retezec):\n    a=0\n    for i in range(len(retezec)):\n        if int(retezec[i])==1:\n            a=a+2**(len(retezec)-1-i)\n    return a\n")
# other_tree = ast.parse("def vyhodnot(retezec):\n    a=0\n    for i in range(len(retezec)):\n        if int(retezec[i])==1:\n            a=a+2**(len(retezec)-1-i)\n    return a\n")
#
# root_node = MyNode("root")
# other_root_node = MyNode("root")
# new_tree = MyNode("new")
# Parser.parse_node(tree, root_node)
# Parser.parse_node(other_tree, other_root_node)
# new_tree.addkid(other_root_node)
#
# print(str(root_node.__eq__(other_root_node)))
#
# Parser.print_node(root_node)
# Parser.print_node(other_root_node)
#
# print "distance: ", Parser.calculate_distance(new_tree, root_node)
def foo():
    path = 'resources/solutiongroups/ast/15'

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        print f
        with codecs.open(path + "/" + f, mode='r', encoding='UTF-8') as input:
            newName = f[:-3]
            newName += "csv"
            with codecs.open(path + "/" + newName, mode='w', encoding="UTF-8") as output:
                for line in input:
                    print >> output, line
foo()



















