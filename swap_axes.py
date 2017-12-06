import codecs
import csv

x_size = 25
y_size = 13

matrix = [[0 for x in range(x_size - 1)] for y in range(y_size - 1)]


def invert_matrix(file_path):
    with codecs.open(file_path, 'rb', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        counter_x = 0
        for line in reader:

            counter_y = 0
            for item in line:
                matrix[counter_y][counter_x] = item
                counter_y += 1
            counter_x += 1

    with codecs.open(file_path[:-4] + "_swapped.csv", 'w') as f:

        for line in matrix:
            row = ""
            for item in line:
                row += str(item)
                row += ","
            row = row[:-1]
            print(row, file=f, flush=True)


invert_matrix("resources/parsed/resultsAvarage2_selectedFeatures_v2.csv")
