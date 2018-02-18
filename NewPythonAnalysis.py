import codecs
import csv
import unicodedata
from base64 import b64encode, b64decode


def encode_program(program):
    return b64encode(bytes(program, "utf-8")).decode("utf-8")


def decode_program(code):
    missing_padding = len(code) % 4
    for i in range(missing_padding):
        code += '='
    return b64decode(code).decode("utf-8")


def parse_new_data():
    correct = 0
    errd = 0
    dict = {}

    translation = get_translation()
    with codecs.open("resources/newTutor/ipython_log.csv", 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        ln = 0
        for line in reader:
            ln += 1
            # skip invalid log lines
            if ln > 1892:
                try:
                    if not line[5] == '-1':
                        print(line)
                    if line[4] == '1':
                        program = decode_program(line[3])
                        name = translation[line[2]]
                        with codecs.open("resources/tasks/new/" + name + ".txt", "a") as output:
                            output.write(program + "\n")
                except Exception as e:
                    print(e)
                    pass


def remove_diacritics(line):
    line = unicodedata.normalize('NFKD', line)

    output = ''
    for c in line:
        if not unicodedata.combining(c):
            output += c
    return output


def get_translation():
    translations = {}
    with codecs.open("resources/newTutor/ipython_item.csv", 'rb', encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        ln = 0
        for line in reader:
            ln += 1
            # skip first line
            if ln == 1:
                continue
            translations[line[0]] = remove_diacritics(line[1])
    return translations

print(get_translation())
parse_new_data()
