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
def plot_decision_surface(train_y_x,train_yy,the_classifier,the_title,feature_names,xvar=0,yvar=1,step_size=2.0,min_zero=False):
    #create and prettify the plot
    cmap="Set3"
    fig,ax= plt.subplots(figsize=(8, 8))
    ax.set_title(the_title)
    ax.set_xlabel(feature_names[xvar])
    ax.set_ylabel(feature_names[yvar])

    #define a grid we use to plot the decision boundaries
      #get max/min values for grid edges
    columnMax,columnMin = np.max(train_y_x,axis=0), np.min(train_y_x,axis=0)
    if(min_zero==True):
        x_min , y_min= 0,0
    else:
        x_min, y_min = columnMin[ xvar]*0.95, columnMin[yvar]*0.95
    x_max, y_max = columnMax[xvar]*1.05, columnMax[yvar]*1.05 
    #make the grid
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step_size),np.arange(y_min, y_max, step_size))

    #predict and plotfor every point on the grid
    Z = the_classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z,cmap=cmap)

    # Plot also the train_ying points
    if type(train_yy==list):
        train_yy = np.array(train_yy)
    ax.scatter(x=train_y_x[:,xvar ],y= train_y_x[:, yvar], c=train_yy.astype(float), alpha=1.0, cmap=cmap, edgecolor="black")
    plt.show()
    
    
def show_scatterplot_matrix(X,y,feature_names,title=None):
    f = X.shape[1]
    if(len(y) != X.shape[0]):
        print("Error,   the y array  must have the same length as there are rows in X")
        return
    fig, ax = plt.subplots(f,f,figsize=(10,10))
    plt.set_cmap('jet')
    for feature1 in range(f):
        ax[feature1,0].set_ylabel( feature_names[feature1])
        ax[0,feature1].set_xlabel( feature_names[feature1])
        ax[0,feature1].xaxis.set_label_position('top') 
        for feature2 in range(f):
            xdata = X[:,feature1]
            ydata = X[:,feature2]
            ax[feature1, feature2].scatter(xdata,ydata,c=y)
    if title != None:
        fig.suptitle(title,fontsize=16,y=0.925)