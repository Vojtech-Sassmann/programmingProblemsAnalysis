from data import tasks
import codecs
from new_bagOfWords_vector import searched_nodes

import new_bagOfWords_vector as bagAnalysis


def foo():
    bagAnalysis.run = False
    bagAnalysis.binary = False
    bagAnalysis.solution_number = 1
    bagAnalysis.submission_limit = 1
    bagAnalysis.minimal_vector_size = 1
    bagAnalysis.output_path = "resources/example/exampleBoW.csv"

    bagAnalysis.save_header()
    for task in tasks:
        results = bagAnalysis.AnalyseResults()
        bagAnalysis.analyze_solution(task.solution, results)
        bagAnalysis.save_results(results, task.name)
foo()
