from data import tasks
import codecs
from new_bagOfWords import searched_nodes

import new_bagOfWords as bagAnalysis


def foo():
    bagAnalysis.binary = False
    bagAnalysis.solution_number = 1
    bagAnalysis.submission_limit = 1
    bagAnalysis.binary = True
    bagAnalysis.output_path = "resources/example/bagOfWordsBin.csv"

    bagAnalysis.save_header()
    for task in tasks:
        results = bagAnalysis.AnalyseResults()
        bagAnalysis.analyze_solution(task.solution, results)
        bagAnalysis.save_results(results, task.name)
foo()
