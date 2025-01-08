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
    # call function to solve the puzzle
    # wrap it in a try...except to help debug incorrect code
    
    worked = False
    score = 0
    try:
        search_answer = exhaustive_search_4tumblers(puzzle)
        if search_answer == puzzle.goal:
            worked=True
        else:
            message = (
                f"Something went wrong: your code returned the answer {search_answer}<br>"
            )
            message += f" but the real answer was {puzzle.goal}"
    except Exception as e:
        message = "Something went wrong with your code.<br>"
        message += "Here is the stack trace which should let you find the error<br>"
        message += traceback.format_exc()
    # assertion fails and prints the message if something went wrong
    
    if worked:
        message = f"Well done, your code correctly found the solution {puzzle.goal}"
        score = 40
    
    return score, message

#========================================================
def mark_sudoku_checker():
    attempt1 = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
    ]
    )
    
    attempt2 = np.array(
    [
        [4,8,3,9,2,1,6,5,7],
        [9,6,7,3,4,5,8,2,1],
        [2,5,1,8,7,6,4,9,3],
        [5,4,8,1,3,2,9,7,6],
        [7,2,9,5,6,4,1,3,8],
        [1,3,6,7,9,8,2,4,5],
        [3,7,2,6,8,9,5,1,4],
        [8,1,4,2,5,3,7,6,9],
        [6,9,5,4,1,7,3,8,2]
    ]
    )   

    score = 0
    
    msg1=''
    passed = check_sudoku_array(attempt1)
    if  passed==27:
        msg1= "Your code incorrectly said this invalid array was ok.<br>"
    else:
        score +=5
        msg1= ("Your code correctly said this was not a Sudoku solution"  
               f" because it failed {27 -passed} conditions.<br>"
              )
    for row in range(attempt1.shape[0]):
        msg1 += f'{attempt1[row]}<br>'
    
    msg2=''
    passed = check_sudoku_array(attempt2)
    if  passed==27:
        msg2= "Your code correctly said this was ok.<br>"
        score += 5
    else:
        msg2= ("Your code incorrectly said this  valid Sudoku solution"    
               f" failed {27-passed} tests.<br>"
              )
    for row in range(attempt2.shape[0]):
        msg2 += f'{attempt2[row]}<br>'
    
    return score, msg1 +'<br>' +msg2


#====================================================
# run this cell to test your function
def mark_get_names():
    """
    an example of writing a test to check code does what it should,
    building and using an error string to give more information.
    NOTE: we will test your code using different arrays, so you can't hard-code the answers!
    """
    tutors_names2 = np.array(
        [
            ["j", "u", "r", "g", "e", "n", " ", "k", "l", "o", "p", "p", " "],
            ["p", "o", "l", "l", "y", " ", " ", "h", "a", "r", "v", "e", "y"],
            ["t", "r", "e", "n", "t", " ", " ", "a", "r", "n", "o", "l", "d"],
        ],
        dtype=str,
    )
    returned_value = get_names(tutors_names2)
    correct_value = ["klopp ", "harvey", "arnold"]
    error_msg = f"returned value {returned_value} should be {correct_value}"
    if returned_value == correct_value:
        return 10, f"Well done, your code correctly pulled out the names in this test"
    else:
        return  0, ("Your code returned a set of incorrect values.<br>"
                    "To help you, all first names and family names in the test have length 5 or 6."
                   )


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