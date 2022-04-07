

import copy


#======================================================
class candidateSolution:
    def __init__(self):
        self.variableValues = []
        self.quality = 0
        self.depth=0

#======================================================        
#python 3 lets us define the types of parameters if we want to
def IsAtGoal(soln:candidateSolution): 
    if(soln.quality==1):
        return True
    else:
        return False
    
    
#======================================================

# define the encoding we will use for moves    
moveNames = ["empty_0to1","Grain_0to1","Chicken_0to1","Fox_0to1","empty_1to0","Grain_1to0", "Chicken_1to0", "Fox_1to0"]    
    
#moveNames = ["b01","G01","C01","F01","b10","G10", "C10", "F10"]    
    
    
    
#=====================================================    
def Evaluate(soln: candidateSolution ):
    location = [0,0,0,0]
    global reason
    reason = ""
    boat=3
    grain=2
    chicken=1
    fox=0
    for move in soln.variableValues:
        valid = True
        if(move==0): 
            if(location[boat]!=0):
                valid = False
                reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=1
        elif(move==1):
            if( location[boat]!=0 or location[grain]!=0):
                valid = False
                reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 1
        elif(move==2):
            if( location[boat]!=0 or location[chicken !=0]):
                valid = False
                reason = "boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 1
        elif(move==3):
            if( location[boat]!=0 or location[fox]!=0):
                valid = False
                reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 1                
        elif(move==4): 
            if(location[boat]!=1):
                valid = False
                reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=0
        elif(move==5):
            if( location[boat]!=1 or location[grain]!=1):
                valid = False
                reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 0
        elif(move==6):
            if( location[boat]!=1 or location[chicken !=1]):
                valid = False
                reason = " boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 0
        elif(move==7):
            if( location[boat]!=1 or location[fox]!=1):
                valid = False
                reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 0                         
 
        else:
            print('error- unknown move encountered: ' +str(move))
            
        # check for infeasible partial solutions
        if( location[boat] != location[chicken]):
            if( location[chicken]==location[fox]):
                reason = 'fox eats chicken'
                soln.quality=-1
                break
            if(location[chicken]==location[grain]):
                reason = 'chicken eats grain'
                soln.quality=-1
                break
        #check for goal
        if (location == [1,1,1,1]):
            soln.quality=1
            print('goal reached')
            break
    return reason
            
#==================================================================            
def TranslateSolutionAsString(soln:candidateSolution):
    nummoves= len(soln.variableValues)
    movelist = ""
    for move in soln.variableValues:
        #movelist = movelist + " -> " + moveNames [move] 
        movelist = movelist + "->" + moveNames [move] 
    return movelist



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
Q1 = create_multipleChoice_widget('From your understanding of Depth-First Search, why did the algorithm fail to complete?',['It completed','It got stuck in a loop','It was not allowed enough iterations'],'It got stuck in a loop')
Q2 = create_multipleChoice_widget('Is depth-first search complete',['yes','no'],'no')
Q3 = create_multipleChoice_widget('What is the minimum depth needed to solve the fox-chicken-grain problem?',['4','5','6','7','8'],'7')
Q4 = create_multipleChoice_widget('Will imposing a maximum depth on the solution  make Depth-First Search complete successfully for every problem',['yes','no'],'no')
Q5 = create_multipleChoice_widget('Does the depth of the solution found by breadth-first match that needed to solve using the amended version of depth-first?',['yes','no'],'yes')
         