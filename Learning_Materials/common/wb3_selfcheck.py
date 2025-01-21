""" the_marking.py
Author : james.smith@uwe.ac.uk 2024
 marks workbook 1 from Artificial Intelligencw 1
 """
from __future__ import annotations
import numpy as np
import traceback
from candidatesolution import CandidateSolution
from problem import Problem
from singlemembersearch import SingleMemberSearch
from mazenodisplay import Maze

import student_wb3 as student

def run_on_maze(
    algorithm: SingleMemberSearch, 
    show_runlog: bool = False, 
    mazefile: str = "maze.txt"
     ) -> int:
    """ function that tries to run a search algorithm on a maze problem
    Parameters
    ----------
    algorithm: name of a class of search algorithm
    show_runlog (bool) whether to print debugging information
    mazefile (str): name of the file containing  definition of a specific maze instance
    """
    
    mymaze = Maze(mazefile=mazefile)
    mysearch = algorithm(mymaze, constructive=True, max_attempts=1500)
    name = mysearch.__str__()
    try:
        found = mysearch.run_search()
        if found:
            status=2
        else:
            status=1
    except Exception as e:
        print(f'Exception occurrred running your code for algortithm {name}.<br>'
              f'This stack trace may help you identify the problem.<br>'
              f'{traceback.format_exc()}'
        )
        status=0
    
    del mymaze
    return status, name

#======================================================================
# Search algorithms and desired behaviour


# code that runs those
def test_on_maze(algorithm: SingleMemberSearch, 
                 mazefile="maze.txt"):
    status, name = run_on_maze(algorithm, mazefile)

    
    outstr = f"Testing your code for {name} on the simple maze.<br>"

    if status==0:
        outstr= ("Your code caused an exception to be raised and did not complete running.<br>" 
        "You can use the stack trace printed above to help debug the problem.<br>"
                )
 
    elif status==1:
        outstr = (
            "Your code ran but did not find a solution on this maze.<br>"
            "You may get some marks.<br>"
        )
    else:
        outstr = (
            "Your code ran and found a solution on this maze.<br>"
            "You will get some marks.<br>"
        )
    outstr += f'<br>You score {status} out of 2 for your implementation of {name}.'
    return status,outstr

#============================================================
wall_colour= 0.0
hole_colour = 1.0
#=============================================================
def test_maze_that_breaks_depthfirst():
    outstr= "Testing your code that produces a maze that depth-first does not solve.<br>"
    score=0
    
    
    try:
        student.create_maze_breaks_depthfirst()
        mymaze=Maze('maze-breaks-depth.txt')
        outstr=("your code produced a mazefile  that could be loaded, "
               "so you may score some marks.<br>")
        score=2

    except FileNotFoundError: 
        outstr += ("Your function create_maze_breaks_depthfirst either did not run,<br>"
                   " or did not produce a file called maze-breaks-depth.txt as required.<br>"
                  )
        score=0
    except Exception as e:
        outstr=("Running your function caused the following ex eption to  be raised:<br>"
                "This stack trace may help you identify the problem<br>"
                f'{traceback.format_exc()}'
               )
        score=0
    return score, outstr
    

#================================================================
def test_maze_depth_better():
    ok:bool=True
    score:int=0
    outstr= "Testing your code that produces a maze where depth-first outperforms breadth-first.<br>"

    
    try:
        student.create_maze_depth_better()
        mymaze=Maze( 'maze-depth-better.txt')
        outstr=("your code produced a mazefile  that could be loaded.<br>"
               "You may score some marks.<br>")
        score=2

    except FileNotFoundError: 
        outstr += ("Your function create_maze_depth_better either did not run,<br>"
                   " or did not produce a file called maze-depth-better.txt as required.<br>"
                  )
        score=0
    except Exception as e:
        outstr=("Running your function caused the following exception to  be raised:<br>"
                "This stack trace may help you identify the problem.<br>"
                f'{traceback.format_exc()}'
               )
        score=0

    return score,outstr
#===============================================================================

def MarkingFunction(studentFile):
    
    overallScore = 0         # score of the results from the three functions
    overallFeedback = ''

    # test the different search algorithms
    algorithms= [student.DepthFirstSearch,student.BreadthFirstSearch,
            student.BestFirstSearch,student.AStarSearch]
    for algorithm in algorithms:
        this_score,this_feedback = test_on_maze(algorithm)
        
        headerStr = ( "<p></p><div style='border:2px solid darkred;padding:5px'>"
                    "<b>Testing your class definition code</b><p></p>"
                    )
        overallFeedback += (headerStr+this_feedback+"</div>")
        overallScore += this_score
    

    # test maze that defeats depth first
    this_score, this_feedback = test_maze_that_breaks_depthfirst() 
    headerStr = ( "<p></p><div style='border:2px solid darkred;padding:5px'>"
                  "<b>Testing your maze that breaks depth-first</b>"
                  "<br>using the <i>correct</i> search algorithm.<p></p>"
                   "<p></p>"
                    "<p> You score " +repr(this_score) +" for this part</b></p>"
                    )

    overallFeedback += (headerStr+this_feedback+"</div>")
    overallScore += this_score

    # test maze that suits depth first
    this_score, this_feedback = test_maze_depth_better() 
    headerStr = ( "<p></p><div style='border:2px solid darkred;padding:5px'>"
                  "<b>Testing your maze where depth-first outperforms breadth-first</b>"
                  "<br>using the <i>correct</i> search algorithm.<p></p>"
                    "<p> You score " +repr(this_score) +" for this part</b></p>"
                    )

    overallFeedback += (headerStr+this_feedback+"</div>")
    overallScore += this_score

    return overallScore, overallFeedback

