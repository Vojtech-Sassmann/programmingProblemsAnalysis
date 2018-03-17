import codecs
import csv
from collections import namedtuple
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='vectoun', api_key='U9FbUzXONbG5og16upmm')

Group = namedtuple(
    'Group',
    ['count',
     'label']
)


def load_groups_for_item(file_name, threshold):
    groups = []
    total_solutions_count = 0
    with codecs.open(file_name, mode='r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) == 2:
                count = int(line[0])
                label = line[1]
                if not count < threshold:
                    groups.append(Group(count=count, label=label))
                total_solutions_count += count

    # result_groups = []
    # others_group_count = 0
    # for group in groups:
    #     if group.count / total_solutions_count < threshold:
    #         others_group_count += group.count
    #     else:
    #         result_groups.append(group)
    #
    # others_group = Group(count=others_group_count, label="Others")
    # result_groups.append(others_group)
    #
    # return result_groups

    return groups


def show_groups(groups):
    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)']

    data = []
    total_count = 0
    for group in groups:
        total_count += group.count
    index = 0
    for group in groups:
        color = 255 * group.count / total_count
        print(color)
        data.append(go.Bar(
            y=['AST'],
            x=[group.count],
            name=str(group.count),
            orientation='h',
            marker=dict(
                # color='rgba(' + str(color) + ', ' + str(color) + ', ' + str(color) + ', 0.6)',
                color=colors[index % len(colors)],
                line=dict(
                    # color='rgba(' + str(color) + ', ' + str(color) + ', ' + str(color) + ', 1.0)',
                    color=colors[index % len(colors)],
                    width=3)
            )
        ))
        index += 1

    layout = go.Layout(
        barmode='stack',
        legend=dict(
            traceorder='inverted'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Nejvetsi spolecny delitel_ast_10')


groups = load_groups_for_item("./resources/solutiongroups/ast/Nejvetsi spolecny delitel.csv", 0)
show_groups(groups)
