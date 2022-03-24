import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import matplotlib.pyplot as plt
import numpy as np


##==============================================



def showPerceptron( w1,w2,bias,func): 
    in1 = np.linspace(-5,5,100)
    if (w2==0):
        y=0
    else:
        y = -(bias/w2)  - in1*(w1/w2)
    plt.plot(in1, y, '-r',label="Decision Boundary")
        # plot sample functions
    if(func != ''):
        plt.plot(0,0,'or')
        if(func=='AND'):
            m01 = m10 = 'or'
        else:
            m01=m10='og'
        if(func=='XOR'):
            m11 = 'or'
        else:
            m11 = 'og'
        plt.plot(0,1,m01)
        plt.plot(1,0,m10)
        plt.plot(1,1,m11)
    
    plt.title('Graph of Perceptron decision Boundary')
    plt.xlabel('input1', color='#1C2833')
    plt.ylabel('input2', color='#1C2833')

    plt.xlim(-1.0,2.0)
    plt.ylim(-1.0,2.0)
    plt.legend(loc='upper left')
    plt.grid()
    
    
    
    
##=============================================
#¢plot the decision surface
## code from https://machinelearningmastery.com/plot-a-decision-surface-for-machine-learning/

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
    surface = plt.contourf(x_grid, y_grid, pp_grid, cmap='Pastel1')
    plt.colorbar(surface)
    # create scatter plot for samples from each class
    for class_value in range(2):
        # get row indexes for samples with this class
        row_ix = np.where(y == class_value)
        # create scatter of these samples
        plt.scatter(X[row_ix, 0], X[row_ix, 1], cmap='Pastel1')
    # show the plot
    fig = plt.gcf()
    fig.set_size_inches(7.5, 7.5)