import ast
import re
import codecs
from collections import namedtuple


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

class MyNode:

    def __eq__(self, other):
        if self.__name == other.__name:
            if len(self.__children) != len(other.__children):
                return False
            else:
                for child, other_child in zip(self.__children, other.__children):
                    if not child.__eq__(other_child):
                        return False

                # for i in range(len(self.__children)):
                #     child = self.__children.__getitem__(i)
                #     other_child = other.__children.__getitem(i)
                return True
        else:
            return False

    def __init__(self):
        self.__children = []
        self.__name = None

    def add_child(self, child):
        self.__children.append(child)

    def get_children(self):
        return self.__children

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


class MyVisitor():

    def my_visit(self, node, parent):
        child_nodes = ast.iter_child_nodes(node)
        my_node = MyNode()
        my_node.set_name(node.__class__.__name__)
        for child in child_nodes:
            MyVisitor.my_visit(self, child, my_node)

        if len(my_node.get_children()) == 0:
            if my_node.get_name() in skipped_node_names:
                return
        if my_node.get_name() in replace_node_with_first_child:
            for child in my_node.get_children():
                parent.add_child(child)
            return
        parent.add_child(my_node)


def print_node(node, lvl=0):
    text = ""
    for i in range(lvl):
        text += '\t'
    text += node.get_name()
    print text
    for child in node.get_children():
        print_node(child, lvl + 1)


skipped_node_names = ["Load", "Name", "Param", "arguments", "Store", "Num", "Compare", "Call", "Subscript", "Index", "Eq"]
replace_node_with_first_child = ["BinOp"]

tree = ast.parse("def vyhodnot(retezec):\n    a=0\n    for i in range(len(retezec)):\n        if int(retezec[i])==1:\n            a=a+2**(len(retezec)-1-i)\n    return a\n")
other_tree = ast.parse("def vyhodnot(retezec):\n    a=0\n    for i in range(len(retezec)):\n        if int(retezec[i])==1:\n            a=a-2**(len(retezec)-1-i)\n    return a\n")

root_node = MyNode()
root_node.set_name("root")
other_root_node = MyNode()
other_root_node.set_name("root")
MyVisitor().my_visit(tree, root_node)
MyVisitor().my_visit(other_tree, other_root_node)

print(str(root_node.__eq__(other_root_node)))

print_node(root_node)
print_node(other_root_node)





















