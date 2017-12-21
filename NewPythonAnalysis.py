import codecs
import csv
from base64 import b64encode, b64decode


def encode_program(program):
    return b64encode(bytes(program, "utf-8")).decode("utf-8")


def decode_program(code):
    missing_padding = len(code) % 4
    print(missing_padding)
    for i in range(missing_padding):
        code += '='
    return b64decode(code).decode("utf-8")


correct = 0
errd = 0
with codecs.open("resources/new/ipython_log.csv", 'rb', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

    with codecs.open("resources/new/erred.csv", 'w') as out:
        for line in reader:
            try:
                program = decode_program(line[3])
                correct += 1
            except:
                errd += 1
                print(line, file=out)

print("correct: ", correct)
print("erred: ", errd)
