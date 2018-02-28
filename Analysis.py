import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

sns.set()


def filter_columns(dataframe, min_count=300):

    filter_df = pd.DataFrame()

    for column in dataframe:

        c = dataframe[column]
        values_count = c.value_counts().sum()
        if values_count > min_count:
            filter_df[column] = c

    return filter_df


def print_heatmap(correlation, title="", annotate=False, width=18, height=18, square=False, x_labels_rotation=0,
                  y_labels_rotation=0, fmt='.2g', font_scale=1.0):
    with sns.plotting_context('paper', font_scale=font_scale):
        plt.figure(figsize=(width, height))
        plt.title(title, size=15)
        sns.heatmap(correlation, annot=annotate, square=square, center=0, fmt=fmt)
        plt.xticks(rotation=x_labels_rotation)
        plt.yticks(rotation=y_labels_rotation)
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


def adjust_columns(dataframes):
    for df1 in dataframes:
        for df2 in dataframes:
            filter_diff_columns(df1, df2)


def load_df(path, separator=','):
    df = pd.read_csv(path, sep=separator, index_col=0)
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


def split_df_in_half(df):
    length = len(df)
    half = int(length/2)
    return df.head(half), df.tail(len(df) - half)


def log_values_in_df(df):
    for col in df:
        df[col] += 1
    return df.apply(np.log2)

def null_not_top_values(dataframe):
    number_of_top = 4

    for series in dataframe:
        s = dataframe[series]

        so = s.sort_index().sort_values(kind="quicksort", ascending=False)

        top_item_names = []
        for i, key in enumerate(so.keys()):
            if i > 0:
                top_item_names.append(key)
            if i > number_of_top:
                break
        print(series, ": ", so)
        print(series, ": ", top_item_names)
        for k in dataframe[series].keys():
            # print("key: ", k)
            if k not in top_item_names:
                # print("NULLED")
                dataframe[series][k] = 0
                # print("New values set: ", dataframe[series][k])
            else:
                dataframe[series][k] = 1


def get_top_item_features(dataframe, top_count):
    new_series = {}
    for series in dataframe:
        s = dataframe[series]
        so = s.sort_values(kind="quicksort", ascending=False)

        serie = []
        for i, key in enumerate(so.keys()):
            # print("key: ", key, " ,value: ", so[key], "i: ", i)
            if i > 0:
                serie.append(key)
            if i > top_count:
                break
        new_series[series] = serie

    return pd.DataFrame(data=new_series)


def compare_item_values(v1, v2):
    match = 0
    for key1 in v1:
        for key2 in v2:
            if key1 == key2:
                match += 1 / len(v1)
    return match


def compare_top_item_features(features1, features2):
    itemsMatches = []
    for (k1, v1), (k2,v2) in zip(features1.items(), features2.items()):
        itemsMatches.append(compare_item_values(v1, v2))
    result = 0
    for match in itemsMatches:
        result += match
    result /= len(itemsMatches)

    return result

def show_df(df):
    cg = sns.clustermap(df)
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(cg.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
    plt.show()

def show_corr_from_features(features, method='pearson'):
    corr = features.corr(method=method)
    show_df(corr)


def compare_correlations(correlations, labels, method='pearson', title=''):
    data = {}
    for i in range(labels.__len__()):
        data[labels.__getitem__(i)] = correlations.__getitem__(i).values.flatten()
    frame = pd.DataFrame(data=data)
    final_df = frame.corr(method=method)
    print_heatmap(final_df, title, True, 8, 8)


"""Zjisteni, jestli mame dost dat"""

# data_user_time = load_df("resources/Python_user_time.csv")
# filtered_df_200 = filter_columns(data_user_time, min_count=200)
# filtered_df_300 = filter_columns(data_user_time, min_count=300)
# filtered_df_400 = filter_columns(data_user_time, min_count=400)
#
# df1, df2 = split_df_in_half(data_user_time)
# df1_f_200, df2_f_200 = split_df_in_half(filtered_df_200)
# df1_f_300, df2_f_300 = split_df_in_half(filtered_df_300)
# df1_f_400, df2_f_400 = split_df_in_half(filtered_df_400)
#
# corr_1_not_filtered_s = df1.corr(method='pearson')
# corr_2_not_filtered_s = df2.corr(method='pearson')
# corr_1_not_filtered_p = df1.corr(method='pearson')
# corr_2_not_filtered_p = df2.corr(method='pearson')
#
# corr_1_s_f_200 = df1_f_200.corr(method='pearson')
# corr_2_s_f_200 = df2_f_200.corr(method='pearson')
# corr_1_s_f_300 = df1_f_300.corr(method='pearson')
# corr_2_s_f_300 = df2_f_300.corr(method='pearson')
# corr_1_s_f_400 = df1_f_400.corr(method='pearson')
# corr_2_s_f_400 = df2_f_400.corr(method='pearson')
#
# data_corr_method = {
#     "Pearson": compare_corrs(corr_1_not_filtered_p, corr_2_not_filtered_p).item(1),
#     "Spearman": compare_corrs(corr_1_not_filtered_s, corr_2_not_filtered_s).item(1),
# }
#
# data = {"a) Not filtered (items:" + str(len(corr_1_not_filtered_s.columns)) + ")": compare_corrs(corr_1_not_filtered_s, corr_2_not_filtered_s).item(1),
#         "b) 200+ (items kept:" + str(len(corr_1_s_f_200.columns)) + ")": compare_corrs(corr_1_s_f_200, corr_2_s_f_200).item(1),
#         "c) 300+ (items kept:" + str(len(corr_1_s_f_300.columns)) + ")": compare_corrs(corr_1_s_f_300, corr_2_s_f_300).item(1),
#         "d) 400+ (items kept:" + str(len(corr_1_s_f_400.columns)) + ")": compare_corrs(corr_1_s_f_400, corr_2_s_f_400).item(1)}
# corr_method_df = pd.DataFrame(data=data_corr_method, index=["Correlation coefficient"])
# filter_df = pd.DataFrame(data=data, index=["Correlation coefficient"])
#
# print_heatmap(corr_method_df, annote=True, square=True, width=7, height=2)
# print_heatmap(filter_df.T, annote=True, square=True, width=12, height=4, font_scale=2.0)
#
# show_corr_from_features(data_user_time, method='spearman')
# show_corr_from_features(filtered_df_300, method='pearson')

"""Porovnani metod vyberu user solution pomoci korelace"""
# top_solution_df = load_df("resources/parsed/results10_swapped.csv")
# second_solution_df = load_df("resources/parsed/results20_swapped.csv")
# third_solution_df = load_df("resources/parsed/results30_swapped.csv")
# average2_solution_df = load_df("resources/parsed/resultsAvarage2_selectedFeatures_v2_swapped.csv")
# average3_solution_df = load_df("resources/parsed/resultsAvarage3_selectedFeatures_v2_swapped.csv")
# average4_solution_df = load_df("resources/parsed/resultsAvarage4_selectedFeatures_v2_swapped.csv")
# average5_solution_df = load_df("resources/parsed/resultsAvarage5_selectedFeatures_v2_swapped.csv")
# average6_solution_df = load_df("resources/parsed/resultsAvarage6_selectedFeatures_v2_swapped.csv")
# example_solution_df = load_df("resources/example/bagOfWords_swapped.csv")
# data_user_time = load_df("resources/Python_user_time.csv")
# performance_filtered_df = filter_columns(data_user_time)
# dfs = [
#     example_solution_df,
#     top_solution_df,
#     second_solution_df,
#     third_solution_df,
#     average2_solution_df,
#     average3_solution_df,
#     average4_solution_df,
#     average5_solution_df,
# ]
#
# names = [
#     'Sample solution',
#     'Top solution',
#     'Second solution',
#     'Third solution',
#     'Average of top2',
#     'Average of top3',
#     'Average of top4',
#     'Average of top5',
# ]
# adjust_columns(dfs)
#
# corrs = []
# for df in dfs:
#     corrs.append(df.corr(method='pearson'))
#
# data = {}
# values = []
# for i in range(names.__len__()):
#     values.append(corrs.__getitem__(i).values.flatten())
#     data[names.__getitem__(i)] = corrs.__getitem__(i).values.flatten()
#
# frame = pd.DataFrame(data=data)
# frame = frame[names]
# all_metric = frame.corr()
#
# print_heatmap(all_metric, '', True, 8, 8, square=True, x_labels_rotation=90)


"""Porovnani metod vyberu user solution pomoci korelace peti nejpodobnejsich prikladu"""
# top_solution_df = load_df("resources/parsed/results10_swapped.csv")
# second_solution_df = load_df("resources/parsed/results20_swapped.csv")
# third_solution_df = load_df("resources/parsed/results30_swapped.csv")
# average2_solution_df = load_df("resources/parsed/resultsAvarage2_selectedFeatures_v2_swapped.csv")
# average3_solution_df = load_df("resources/parsed/resultsAvarage3_selectedFeatures_v2_swapped.csv")
# average4_solution_df = load_df("resources/parsed/resultsAvarage4_selectedFeatures_v2_swapped.csv")
# average5_solution_df = load_df("resources/parsed/resultsAvarage5_selectedFeatures_v2_swapped.csv")
# average6_solution_df = load_df("resources/parsed/resultsAvarage6_selectedFeatures_v2_swapped.csv")
# example_solution_df = load_df("resources/example/bagOfWords_swapped.csv")
# data_user_time = load_df("resources/Python_user_time.csv")
# performance_filtered_df = filter_columns(data_user_time)
# dfs = [
#     top_solution_df,
#     second_solution_df,
#     third_solution_df,
#     average2_solution_df,
#     average3_solution_df,
#     average4_solution_df,
#     average5_solution_df,
#     average6_solution_df,
#     example_solution_df,
# ]
#
# names = [
#     '1. TopSolution',
#     '2. SecondSolution',
#     '3. ThirdSolution',
#     '4. AverageSolution2',
#     '5. AverageSolution3',
#     '6. AverageSolution4',
#     '7. AverageSolution5',
#     '8. AverageSolution6',
#     '9. Example',
# ]
# adjust_columns(dfs)
#
# corrs = []
# for df in dfs:
#     corrs.append(df.corr(method='pearson'))
#
#
#
#
#
# for correlation in corrs:
#     null_not_top_values(correlation)
#     print("-----------------")
#
#
# data = {}
# for i in range(names.__len__()):
#     data[names.__getitem__(i)] = corrs.__getitem__(i).values.flatten()
#
# frame = pd.DataFrame(data=data)
# top5_metric = frame.corr(method='pearson')
# print_heatmap(top5_metric, 'Comparison of solutions comparing top 5 item matches', True, 8, 8)

"""porovnani technik vsech podobnych itemu a top5"""
# metrics = {}
# metrics["Top5"] = top5_metric.values.flatten()
# metrics["All"] = all_metric.values.flatten()
#
# metrics_frame = pd.DataFrame(data=metrics)
# print_heatmap(metrics_frame.corr(), annote=True, title="Top5 vs All")

"""podrobne porovnani"""
# first_solution_df = load_df("resources/tmp/av5_AST_swapped.csv")
# second_solution_df = load_df("resources/tmp/p_av5_AST_swapped.csv")
#
# filter_diff_columns(first_solution_df, second_solution_df)
#
# avarage_corr = first_solution_df.corr(method='pearson')
# example_corr = second_solution_df.corr(method='pearson')
#
# corrs = {}
#
# for c1 in avarage_corr:
#     a = avarage_corr.get(c1).to_frame().corrwith(example_corr.get(c1).to_frame())
#     b = a.values
#     corrs[c1] = b.max()
#
# frame = pd.DataFrame(data=corrs, index=["Match"])
# print_heatmap(frame.T, 'Example solution, \'classic\' bag of words vs AST \'bag\' of words', annotate=True, width=8, height=8,
#               font_scale=1.2)




"""porovnani problemu pomoci jedne techniky"""
#
#
# comparison_df = load_df("resources/parsed/resultsAvarage3_swapped.csv")
# show_corr(comparison_df)

"""vykresleni feature matice"""
# average_solution_df = load_df("resources/parsed/resultsAvarage3_swapped.csv")
#
#
# def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
#                      header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
#                      bbox=[0, 0, 1, 1], header_columns=0,
#                      ax=None, **kwargs):
#
#     if ax is None:
#         size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
#         fig, ax = plt.subplots(figsize=size)
#         ax.axis('off')
#
#     mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
#
#     mpl_table.auto_set_font_size(False)
#     mpl_table.set_fontsize(font_size)
#
#     for k, cell in six.iteritems(mpl_table._cells):
#         cell.set_edgecolor(edge_color)
#         if k[0] == 0 or k[1] < header_columns:
#             cell.set_text_props(weight='bold', color='w')
#             cell.set_facecolor(header_color)
#         else:
#             cell.set_facecolor(row_colors[k[0] % len(row_colors)])
#     return ax
#
# render_mpl_table(average_solution_df, header_columns=0, col_width=2.0)
# plt.show()

"""correlace featur"""
# df = load_df("resources/parsed/resultsAvarage3_selectedFeatures_v2_swapped.csv", ",")
#
# show_corr(df)


""" Porovnani userPerformance vs bag of words pomoci korelace"""
# data_user_time = load_df("resources/Python_user_time.csv")
# filtered_df = filter_columns(data_user_time)
#
# data_bag_of_words_df = load_df("resources/parsed/resultsAvarage3_swapped.csv")
#
# user_time_corr = filtered_df.corr(method='spearman')
# bag_of_words_corr = data_bag_of_words_df.corr(method='spearman')
#
# filter_diff_columns(user_time_corr, filtered_df)
# filter_diff_columns(bag_of_words_corr, data_bag_of_words_df)
#
# filter_diff_columns(data_bag_of_words_df, filtered_df)
#
# user_time_corr = filtered_df.corr(method='spearman')
# bag_of_words_corr = data_bag_of_words_df.corr(method='spearman')
#
#
# metrics = {
#     "UserPerformance": user_time_corr.values.flatten(),
#     "BagOfWords": bag_of_words_corr.values.flatten()
# }
#
# metrics_frame = pd.DataFrame(data=metrics)
#
# print_heatmap(metrics_frame.corr(), annote=True, title="Bag of words vs User performance")
#
# comparisons = {}
#
# for top_count in range(3, 6):
#     topBoW = get_top_item_features(bag_of_words_corr, top_count)
#     topUP = get_top_item_features(user_time_corr, top_count)
#
#     match = compare_top_item_features(topBoW, topUP)
#
#     comparisons["Bag of words x UserPerformance(Top" + str(top_count) + ")"] = match
#
# print(comparisons)
#
# print_heatmap(pd.DataFrame(data=comparisons, index=["Match (%)"]).T, annote=True, title="Porovnani bag of words s User Performance pomoci ruznych technik")


""" (Deprecated) bagOfWords vs AST """
# # ast_av1 = load_df("resources/parsed/resultsAvarage1_selectedFeatures_AST_swapped.csv")
# # ast_av2 = load_df("resources/parsed/resultsAvarage2_selectedFeatures_AST_swapped.csv")
# # ast_av3 = load_df("resources/parsed/resultsAvarage3_selectedFeatures_AST_swapped.csv")
# # ast_av4 = load_df("resources/parsed/resultsAvarage4_selectedFeatures_AST_swapped.csv")
# # ast_av5 = load_df("resources/parsed/resultsAvarage5_selectedFeatures_AST_swapped.csv")
# ed_ast_av1 = load_df("resources/tmp/av1_AST_swapped.csv")
# ed_ast_av2 = load_df("resources/tmp/av2_AST_swapped.csv")
# ed_ast_av3 = load_df("resources/tmp/av3_AST_swapped.csv")
# ed_ast_av4 = load_df("resources/tmp/av4_AST_swapped.csv")
# ed_ast_av5 = load_df("resources/tmp/av5_AST_swapped.csv")
# p_ed_ast_av1 = load_df("resources/tmp/p_av1_AST_swapped.csv")
# p_ed_ast_av2 = load_df("resources/tmp/p_av2_AST_swapped.csv")
# p_ed_ast_av3 = load_df("resources/tmp/p_av3_AST_swapped.csv")
# p_ed_ast_av4 = load_df("resources/tmp/p_av4_AST_swapped.csv")
# p_ed_ast_av5 = load_df("resources/tmp/p_av5_AST_swapped.csv")
# ast_example = load_df("resources/example/AST_swapped.csv")
# dfs = [
#     # ast_av1,
#     # ast_av2,
#     # ast_av3,
#     # ast_av4,
#     # ast_av5,
#     ed_ast_av1,
#     ed_ast_av2,
#     ed_ast_av3,
#     ed_ast_av4,
#     ed_ast_av5,
#     p_ed_ast_av1,
#     p_ed_ast_av2,
#     p_ed_ast_av3,
#     p_ed_ast_av4,
#     p_ed_ast_av5,
#     ast_example
# ]
#
# names = [
#     # 'AST average1',
#     # 'AST average2',
#     # 'AST average3',
#     # 'AST average4',
#     # 'AST average5',
#     'AST average1 (filtered)',
#     'AST average2 (filtered)',
#     'AST average3 (filtered)',
#     'AST average4 (filtered)',
#     'AST average5 (filtered)',
#     'AST average1 (filtered) parsed',
#     'AST average2 (filtered) parsed',
#     'AST average3 (filtered) parsed',
#     'AST average4 (filtered) parsed',
#     'AST average5 (filtered) parsed',
#     'AST example solution',
# ]
# adjust_columns(dfs)
#
# corrs = []
# for df in dfs:
#     corrs.append(df.corr(method='pearson'))
#
# data = {}
# for i in range(names.__len__()):
#     data[names.__getitem__(i)] = corrs.__getitem__(i).values.flatten()
#
# frame = pd.DataFrame(data=data)
# frame = frame[names]
# all_metric = frame.corr()
#
# print_heatmap(all_metric, '', True, 8, 8, square=True, x_labels_rotation=90)


""" Podrobne klasicky bagOfWords vs AST """
# classic_av1 = load_df("resources/parsed/resultsAvarage1_selectedFeatures_v2_swapped.csv")
# classic_av2 = load_df("resources/parsed/resultsAvarage2_selectedFeatures_v2_swapped.csv")
# classic_av3 = load_df("resources/parsed/resultsAvarage3_selectedFeatures_v2_swapped.csv")
# classic_av4 = load_df("resources/parsed/resultsAvarage4_selectedFeatures_v2_swapped.csv")
# classic_av5 = load_df("resources/parsed/resultsAvarage5_selectedFeatures_v2_swapped.csv")
# classic_example = load_df("resources/example/classicBOW_swapped.csv")
# ast_av1 = load_df("resources/parsed/resultsAvarage1_selectedFeatures_AST_swapped.csv")
# ast_av2 = load_df("resources/parsed/resultsAvarage2_selectedFeatures_AST_swapped.csv")
# ast_av3 = load_df("resources/parsed/resultsAvarage3_selectedFeatures_AST_swapped.csv")
# ast_av4 = load_df("resources/parsed/resultsAvarage4_selectedFeatures_AST_swapped.csv")
# ast_av5 = load_df("resources/parsed/resultsAvarage5_selectedFeatures_AST_swapped.csv")
# ast_example = load_df("resources/example/AST_swapped.csv")
# dfs = [
#     classic_av1,
#     classic_av2,
#     classic_av3,
#     classic_av4,
#     classic_av5,
#     classic_example,
#     ast_av1,
#     ast_av2,
#     ast_av3,
#     ast_av4,
#     ast_av5,
#     ast_example
# ]
#
# names = [
#     'Average of top 1',
#     'Average of top 2',
#     'Average of top 3',
#     'Average of top 4',
#     'Average of top 5',
#     'Example solution',
# ]
#
# for i in range(names.__len__()):
#     adjust_columns([dfs.__getitem__(i), dfs.__getitem__(i + names.__len__())])
#
# corrs = []
# for df in dfs:
#     corrs.append(df.corr(method='pearson'))
#
# results = {}
# for i in range(names.__len__()):
#     df1 = pd.DataFrame(data=corrs.__getitem__(i).values.flatten())
#     df2 = pd.DataFrame(data=corrs.__getitem__(i + names.__len__()).values.flatten())
#     a = df1.corrwith(df2)
#     results[names.__getitem__(i)] = a.values.max()
#
# frame = pd.DataFrame(data=results, index=["Match"])
# print_heatmap(frame.T, 'Match between \'classic\' bag of words technique and \'AST\' bag of words', annotate=True,
#               width=8, height=10, square=True, font_scale=2.5)
