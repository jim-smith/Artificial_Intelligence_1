import math
import matplotlib.pyplot as plt
import numpy as np


def euclidean_distance(a,b):
    ''' gets the Euclidean (straight line) distance between two items a and b'''
    ''' this is just Pythagoras' theorem in N-dimensions'''
    #a and b must have same number of dimensions/feastures
    assert a.shape[0] == b.shape[0]
    distance=0.0
    for feature in range( a.shape[0]):
        difference = a[feature] - b[feature]
        distance= distance + difference*difference
    return math.sqrt(distance)      



# simple function - currently only works for 2D data - but could easily be extended
def PlotDecisionSurface(trainX,trainy,theClassifier,theTitle,featureNames,xvar=0,yvar=1,stepSize=2.0,minZero=False):
    #create and prettify the plot
    cmap="Set3"
    fig,ax= plt.subplots(figsize=(8, 8))
    ax.set_title(theTitle)
    ax.set_xlabel(featureNames[xvar])
    ax.set_ylabel(featureNames[yvar])

    #define a grid we use to plot the decision boundaries
      #get max/min values for gri edges
    columnMax,columnMin = np.max(trainX,axis=0), np.min(trainX,axis=0)
    if(minZero==True):
        x_min , y_min= 0,0
    else:
        x_min, y_min = columnMin[ xvar]*0.95, columnMin[yvar]*0.95
    x_max, y_max = columnMax[xvar]*1.05, columnMax[yvar]*1.05 
    #make the grid
    xx, yy = np.meshgrid(np.arange(x_min, x_max, stepSize),np.arange(y_min, y_max, stepSize))

    #predict and plotfor evey point on the grid
    Z = theClassifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z,cmap=cmap)

    # Plot also the training points
    if type(trainy==list):
        trainy = np.array(trainy)
    ax.scatter(x=trainX[:,xvar ],y= trainX[:, yvar], c=trainy.astype(float), alpha=1.0, cmap=cmap, edgecolor="black")
    plt.show()
    
    
def show_scatterplot_matrix(X,y,featureNames,title=None):
    f = X.shape[1]
    if(len(y) != X.shape[0]):
        print("Error,   the y array  must have the same length as there are rows in X")
        return
    fig, ax = plt.subplots(f,f,figsize=(12,12))
    plt.set_cmap('jet')
    for feature1 in range(f):
        ax[feature1,0].set_ylabel( featureNames[feature1])
        ax[0,feature1].set_xlabel( featureNames[feature1])
        ax[0,feature1].xaxis.set_label_position('top') 
        for feature2 in range(f):
            xdata = X[:,feature1]
            ydata = X[:,feature2]
            ax[feature1, feature2].scatter(xdata,ydata,c=y)
    if title != None:
        fig.suptitle(title,fontsize=16,y=0.925)