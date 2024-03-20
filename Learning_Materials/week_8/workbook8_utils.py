
# basics for manipulating and outputting arrays etc
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import matplotlib.pyplot as plt
import numpy as np
from random import random

## MLP specific stuff
from sklearn.neural_network import MLPClassifier
import VisualiseNN as VisNN




def plotDecisionSurface(model,X,y):
    min1, max1 = X[:, 0].min() - 1, X[:, 0].max() + 1 #1st feature
    min2, max2 = X[:, 1].min() - 1, X[:, 1].max() + 1 #2nd feature
    x1_scale = np.arange(min1, max1, 0.1)
    x2_scale = np.arange(min2, max2, 0.1)
    x_grid, y_grid = np.meshgrid(x1_scale, x2_scale)
    # flatten each grid to a vector
    x_g, y_g = x_grid.flatten(), y_grid.flatten()
    x_g, y_g = x_g.reshape((len(x_g), 1)), y_g.reshape((len(y_g), 1))
    # stack to produce hi-res grid in form like dataset
    grid = np.hstack((x_g, y_g))

    # make predictions for the grid
    y_pred_2 = model.predict(grid)
    
    #predict the probability
    p_pred = model.predict_proba(grid)
    # keep just the probabilities for class 0
    p_pred = p_pred[:, 0]
    # reshaping the results
    p_pred.shape
    pp_grid = p_pred.reshape(x_grid.shape)

    # plot the grid of x, y and z values as a surface
    levels=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    surface = plt.contourf(x_grid, y_grid, pp_grid, levels,cmap='Pastel1')
    plt.colorbar(surface)
    # create scatter plot for samples from each class
    for class_value in range(2):
        # get row indexes for samples with this class
        row_ix = np.where(y == class_value)
        # create scatter of these samples
        plt.scatter(X[row_ix, 0], X[row_ix, 1], cmap='Pastel1')
    # show the plot






















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