import ast
import zss


try:
    from editdist import distance as strdist
except ImportError:
    def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1


default_skipped_nodes = ["Load", "Name", "Param", "arguments", "Store", "Num", "Compare", "Subscript", "Index", "Eq"]
default_replace_nodes = ["BinOp"]


def my_distance(node1, node2):
    return strdist(node1, node2)


class MyNode(object):
    """
    Class representing tree node
    """
    def __init__(self, label, raw="None"):
        self.__label = label
        self.__children = list()
        self.__raw = raw

    def __eq__(self, other):
        if self.__label == other.__label:
            if len(self.__children) != len(other.__children):
                return False
            else:
                for child, other_child in zip(self.__children, other.__children):
                    if not child.__eq__(other_child):
                        return False
                return True
        else:
            return False

    def addkid(self, child):
        self.__children.append(child)
        return self

    def get_raw(self):
        return self.__raw

    @staticmethod
    def get_children(self):
        return self.__children

    @staticmethod
    def get_label(self):
        return self.__label

    def __hash__(self):
        return hash(self.__label)

    def __str__(self):
        value = ""
        value += self.__label + "{"
        for child in MyNode.get_children(self):
            value += child.__str__() + ", "
        value += "}"
        return value


def calculate_distance(tree1, tree2):
    """
    Calculates distance between two trees
    :param tree1: first tree
    :param tree2: second tree
    :return: distance of given trees
    """
    return zss.simple_distance(tree1, tree2, MyNode.get_children, MyNode.get_label, my_distance)


def parse_tree(tree, skipped_nodes=default_skipped_nodes, replace_nodes=default_replace_nodes, raw=None):
    root = MyNode("root", raw)

    return parse_node(tree, root, skipped_nodes, replace_nodes)


def parse_node(node, parent, skipped_nodes=default_skipped_nodes, replace_nodes=default_replace_nodes):
    """
    Transforms an AST node into a MyNodes
    :param node: AST tree node that will be parsed
    :param parent: parent MyNode of given node
    :param skipped_nodes: Names of nodes that will not be added to the tree
    if the contain no child nodes
    :param replace_nodes: Names of nodes that will be replaced by its children
    """
    child_nodes = ast.iter_child_nodes(node)
    node = MyNode(node.__class__.__name__, None)
    for child in child_nodes:
        parse_node(child, node, skipped_nodes, replace_nodes)

    if len(MyNode.get_children(node)) == 0:
        if MyNode.get_label(node) in skipped_nodes:
            return
    if MyNode.get_label(node) in replace_nodes:
        for child in MyNode.get_children(node):
            MyNode.addkid(parent, child)
        return
    parent.addkid(node)
    return parent


def print_node(node, lvl=0):
    """
    Prints the given node with its children to the standard output
    :param node: node that will be printed
    :param lvl: the distance of a node from root node
    """
    text = ""
    for i in range(lvl):
        text += '\t'
    text += MyNode.get_label(node)
    print text
    for child in MyNode.get_children(node):
        print_node(child, lvl + 1)
