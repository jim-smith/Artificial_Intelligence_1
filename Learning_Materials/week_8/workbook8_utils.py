
# basics for manipulating and outputting arrays etc
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import matplotlib.pyplot as plt
import numpy as np
from random import random

## MLP specific stuff
from sklearn.neural_network import MLPClassifier
import VisualiseNN as VisNN





















#================================================================
import ipywidgets as widgets
import sys
from IPython.display import display
from IPython.display import clear_output
from IPython.display import HTML

def create_multipleChoice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if a==correct_answer_index:
            s = '\x1b[6;30;42m' + "Correct." + '\x1b[0m' +"\n" #green color
        else:
            s = '\x1b[5;30;41m' + "Wrong. " + '\x1b[0m' +"\n" #red color
        with feedback_out:
            clear_output()
            print(s)
        return
    
    check = widgets.Button(description="submit")
    check.on_click(check_selection)
    
    
    return widgets.VBox([description_out, alternativ, check, feedback_out])

Q0 = create_multipleChoice_widget('What type of search is the algorithm below implementing?',['Constructive','Perturbative'],'Constructive')
Q1 = create_multipleChoice_widget('From your understanding of Depth-First Search, why did the algorithm fdail to complete?',['It completed','It got stuck in a loop','It was not allowed enough iterations'],'It got stuck in a loop')
Q2 = create_multipleChoice_widget('Is depth-first search complete',['yes','no'],'no')
Q3 = create_multipleChoice_widget('What is the minimum depth needed to solve the fox-chicken-grain problem?',['4','5','6','7','8'],'7')
Q4 = create_multipleChoice_widget('Will imposing a maximum depth on the solution  make Depth-First Search complete successfully for every problem',['yes','no'],'no')
Q5 = create_multipleChoice_widget('Does the depth of the solution found by breadth-first match that needed to solve using the amended versin of depth-first?',['yes','no'],'yes')