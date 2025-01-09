# File testcode.py
# Jim Smith 2025 james.samith@uwe.ac.uk
#provided to test studetns code for syntax errors prior ot submission for marking


#import your code
import traceback
from sys import path
path.append("../common")
from approvedimports import *
student_codepath = "studentcode"
path.append(student_codepath)
from student_wb1 import get_names
from student_wb1 import exhaustive_search_4tumblers
from student_wb1 import check_sudoku_array

#====================================================
def mark_exhaustive_search_4tumblers():
    """function to test implementation of exhaustive search"""
    # create new puzzle
    puzzle = CombinationProblem(tumblers=4, num_options=10)
 
    message= "Testing your code with a single random combination.<br>"
    score = 0
    try:
        search_answer = exhaustive_search_4tumblers(puzzle)
        if search_answer == puzzle.goal:
            message += ("Your code ran successfully."
                        " It would score some marks but not necessarily all,"
                          " because this is only one test.<br>"  )
            score = 2
        else:
            message += ("Your code ran but did not pass <b>this</b> test." 
                        " It is not clear if it will score marks.<br>"
                      )
            score=1

    except Exception as e:
        message +=  ("Something went wrong with your code.<br>"
                     "Here is the stack trace which should let you find the error.<br>"
                    )
        message += traceback.format_exc()
        message += "<br>"

        score=0

    return score, message

#========================================================
def mark_sudoku_checker():
    
    attempt = np.array(
    [
        [4,8,3,9,2,1,6,5,7],
        [9,6,7,3,4,5,8,2,1],
        [2,5,1,8,7,6,4,9,3],
        [5,4,8,1,3,2,9,7,6],
        [7,2,9,5,6,4,1,3,8],
        [1,3,6,7,9,8,2,4,5],
        [3,7,2,6,8,9,5,1,4],
        [8,9,4,2,5,3,7,6,9],
        [6,1,5,4,1,7,3,8,2]
    ]
    )  #swapped second column value for bottom two rows
      #so they fail but all columns and squares are ok 

    message="Trying your code with a single sodoku grid.<br>"
    score=0
    try:
        
        passed = check_sudoku_array(attempt)
        if (passed==25):
            message += ("Your code ran and gave the correct result for this test."
                        " It would score some marks."
                       )
            score=2
        else:
            message += ("Your code ran but gave the incorrect result for this test."
                        " It <b>might</b> score some marks."
                       )
            score=1            
        

    except Exception as e:
        message += "Something went wrong with your code.<br>"
        message += "Here is the stack trace which should let you find the error<br>"
        message += traceback.format_exc()
        message += "<br>"
        score=0
        
    
    return score, message


#====================================================
# run this cell to test your function
def mark_get_names():
    """
    an example of writing a test to check code does what it should,
    building and using an error string to give more information.
    NOTE: we will test your code using different arrays, so you can't hard-code the answers!
    """
    message= "Trying your code with a single array of names.<br>"
    score=0
    tutors_names2 = np.array(
        [
            ["j", "u", "r", "g", "e", "n", " ", "k", "l", "o", "p", "p", " "],
            ["p", "o", "l", "l", "y", " ", " ", "h", "a", "r", "v", "e", "y"],
            ["t", "r", "e", "n", "t", " ", " ", "a", "r", "n", "o", "l", "d"],
        ],
        dtype=str,
    )
    try:
        returned_value = get_names(tutors_names2)
        correct_value = ["klopp ", "harvey", "arnold"]
        if returned_value == correct_value:
            score=2
            message += "Your code correctly pulled out the names on a test and would score marks.<br>"
        else:
            score=1
            message += ("Your code ran ok but returned a set of incorrect values.<br>"
                        " It is not clear if you will score any marks.<br>"
                   )
    except Exception as e:
        message += "Something went wrong with your code.<br>"
        message += "Here is the stack trace which should let you find the error<br>"
        message += traceback.format_exc()
        message += "<br>"
        score=0
        
    
    return score, message


#======================

def MarkingFunction(sFile):


    MarkFunctions = [mark_exhaustive_search_4tumblers,
                     mark_get_names, 
                     mark_sudoku_checker]
    Names = ['exhaustive_search_4tumblers',
                     'get_names', 
                     'sudoku_checker']

    overallScore = 0         # score of the results from the three functions

    overallFeedback = ''

    for task in range (len(MarkFunctions)):
        markFunction= MarkFunctions[task]
        name = Names[task]
        this_score, this_feedback = markFunction() # returns an int and feedback text
        headerStr = ( "<p></p><div style='border:2px solid darkred;padding:5px'>"
                     "<b>Testing "+ name+"</b><p></p>"
                    "<p> You score " +repr(this_score) +" for this part</b></p>"
                    )

        overallFeedback += (headerStr+this_feedback+"</div>")
        overallScore += this_score

    return overallScore, overallFeedback