import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set()


def filter_columns(dataframe):

    filter_df = pd.DataFrame()

    for column in dataframe:

        c = dataframe[column]
        values_count = c.value_counts().sum()
        if values_count > 300:
            filter_df[column] = c

    return filter_df


def print_heatmap(correlation, title, annote=False, width=18, height=18):
    plt.figure(figsize=(width, height))
    plt.title(title, size=15)
    sns.heatmap(correlation, annot=annote, square=True, center=0)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()


def convert_names(list):
    converted = []
    for name in list:
        converted.append(name.replace(" ", ""))
    return converted


def is_name_in_df(name, df):
    s1 = name.replace(" ", "")

    for column in df:
        s2 = column.replace(" ", "")
        if s1 == s2:
            return True
    return False


def filter_diff_columns(df1, df2):

    for column in df1:
        if not is_name_in_df(column, df2):
            del df1[column]

    for column in df2:
        if not is_name_in_df(column, df1):
            del df2[column]


def load_df(path):
    df = pd.read_csv(path, sep=",", index_col=0)
    df.sort_index(axis=1, inplace=True)
    return df


def compare_corrs(corr1, corr2):
    c_f1 = corr1.values.flatten()
    c_f2 = corr2.values.flatten()
    return np.corrcoef(c_f1, c_f2)

""" Porovnani userPerformance vs bag of words"""
# data_user_time = load_df("resources/Python_user_time.csv")
# filtered_df = filter_columns(data_user_time)

# data_bag_of_words_df = load_df("resources/results_swapped.csv")
#
# filter_diff_columns(filtered_df, data_bag_of_words_df)
#
# user_time_corr = filtered_df.corr(method='spearman')
# user_time_corr_pearson = filtered_df.corr()
# bag_of_words_corr = data_bag_of_words_df.corr(method='spearman')
#
# technique_corr = compare_corrs(user_time_corr, bag_of_words_corr)
# pearson_spearman_corr = compare_corrs(user_time_corr, user_time_corr_pearson)
#
# print_heatmap(pearson_spearman_corr, 'Pearson/Spearman corr', annote=True)
# print_heatmap(technique_corr, 'Bag of words/User performance', annote=True)
# print_heatmap(user_time_corr, 'User performance filtered')
# print_heatmap(bag_of_words_corr, 'Bag of words')

"""Zjisteni, jestli mame dost dat"""


def split_df_in_half(df):
    length = len(df)
    half = int(length/2)
    return df.head(half), df.tail(len(df) - half)
#
# df1, df2 = split_df_in_half(filtered_df)
# corr_1 = df1.corr(method='spearman')
# corr_2 = df2.corr(method='spearman')
#
# corr_3 = compare_corrs(corr_1, corr_2)
#
# print_heatmap(corr_3, 'Compare correlation of user performance on split data', annote=True)


"""Porovnani reseni Bag of words"""
top_solution_df = load_df("resources/parsed/resultsTopBin_swapped.csv")
second_solution_df = load_df("resources/parsed/resultsSecondBin_swapped.csv")
third_solution_df = load_df("resources/parsed/resultsThirdBin_swapped.csv")
fourth_solution_df = load_df("resources/parsed/resultsFourthBin_swapped.csv")

top_corr = top_solution_df.corr(method='spearman')
second_corr = second_solution_df.corr(method='spearman')
third_corr = third_solution_df.corr(method='spearman')
fourth_corr = fourth_solution_df.corr(method='spearman')

# print_heatmap(top_corr, 'Top')
# print_heatmap(second_corr, 'Second')
# print_heatmap(third_corr, 'third')
# print_heatmap(fourth_corr, 'fourth')

top_values = top_corr.values.flatten()
second_values = second_corr.values.flatten()
third_values = third_corr.values.flatten()
fourth_values = fourth_corr.values.flatten()

frame = pd.DataFrame(data={'1. Top': top_values, '2. Second': second_values, '3. Third': third_values, '4. Fourth': fourth_values})
print_heatmap(frame.corr(), 'Comparison of solutions (Bin)', True, 6, 6)
