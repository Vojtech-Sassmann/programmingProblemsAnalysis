import codecs
import csv
import ast
import os
import sys
from os import listdir
from os.path import isfile, join


def parse_code(line):
    prefix_size = len(line[0])
    return line[2][prefix_size:]


def save_solution(solution, file_name):
    with codecs.open("resources/tasks/parsed/" + file_name, 'a') as f:
        print(solution, file=f)


def analyze_file(file_name):

    with codecs.open("resources/tasks/" + file_name, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='♠', quoting=csv.QUOTE_NONE)

        solution = r""

        new_solution = True
        for line in reader:
            if len(line) is not 1:
                new_solution = True
                continue
            split = line[0].split(";", 2)
            if len(split) is 3:
                code = parse_code(split)

                if code.startswith("SUBMIT"):
                    new_solution = False
                    save_solution(solution, file_name)
                    solution = code[6:]
                # else:
                #     if code.startswith("RUN"):
                #         new_solution = True
                #     else:
                #         if not new_solution:
                #             solution = solution[:-1]
                #             solution += code
            else:
                new_solution = True


def analyze_files():
    path = 'resources/tasks/'

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        analyze_file(f)

analyze_files()