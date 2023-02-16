import math
import numpy as np


def euclidean_distance(a,b):
    ''' calculates the Euclidean (straight line) distance between two items a and b'''
    ''' this is just Pythagoras' theorem in N-dimensions'''
    #a and b must have same number of dimensions/feastures
    assert a.shape[0] == b.shape[0]
    distance=0.0
    for feature in range( a.shape[0]):
        difference = a[feature] - b[feature]
        distance= distance + difference*difference
    return math.sqrt(distance)    



class simple_1NN:

    def __init__(self, K,verbose = False):
        #we'll use straight line distance -code from week6 reproduced in this week's utils file
        self.distance = euclidean_distance
        # this version only looks at the single nearest neighbour
        self.K=1
        
        #just affects prints to screen
        self.verbose= verbose
        
    def fit(self,X,y):
        # ask the data how big it is and store that info
        self.numTrainingItems = X.shape[0]
        self.numFeatures = X.shape[1]
        # store a copy of the data (X) and the labels (y)
        self.modelX = X
        self.modelY = y
        self.labelsPresent = np.unique(self.modelY) # list the unique values found in the labels provided
        if (self.verbose):
            print(f"There are {self.numTrainingItems} training examples, each described by values for {self.numFeatures} features")
            print(f"So self.modelX is a 2D array of shape {self.modelX.shape}")
            print(f"self.modelY is a list with {len(self.modelY)} entries, each being one of these labels {self.labelsPresent}")
        
    def predict(self,newItems):
        # see how many  newitems there are
        numToPredict = newItems.shape[0]
        # make an empty list to hold their predicted labels
        predictions = np.empty(numToPredict)
        
        #loop through each new item each one
        for item in range(numToPredict):
            # predicting its label
            thisPrediction = self.predict_new_item ( newItems[item])
            # adding that prediction to our list
            predictions[item] = thisPrediction
        return predictions
    
    def predict_new_item(self,newItem):
        
        # Step 1: measure and store distance to each training item
        distFromNewItem = np.zeros((self.numTrainingItems)) # array with one entry for each training set item, intialised to zero
        for stored_example in range (self.numTrainingItems):
            distFromNewItem[stored_example] = self.distance(newItem,  self.modelX[stored_example])
  
        # Step 2: find the one closest training example: This is K=1, 
        closest = 0
        for stored_example in range (0, self.numTrainingItems):
            if  ( distFromNewItem[stored_example] < distFromNewItem[closest] ):
                closest=stored_example
 
        # step 3: count the votes - because this is for K=1 so we don't need to take a vote
        labelOfClosest = self.modelY[closest]
        return labelOfClosest
    