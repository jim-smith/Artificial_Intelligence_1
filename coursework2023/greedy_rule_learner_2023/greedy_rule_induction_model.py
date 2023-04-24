'''
Template submission for coursework task implementing greedy rule induction algorithm
 @Jim Smith: james.smith@uwe.ac.uk 2023
 Students should implement the pseudocode provided 
 to complete the two funtions fit() and predict_one() as  indicated below
 
 
'''
from learned_rule_model import LearnedRuleModel
import numpy as np

#define some constants for where things are in a rule
FEATURE=0
OPERATOR=1
THRESHOLD=2
LABEL = 3



class GreedyRuleInductionModel(LearnedRuleModel):
    '''
    sub-class that uses greedy constrcutive search to find a set of rules
    that classify a dataset
    '''
    def __init__(self,max_rules=10, increments=25):
        '''constructor 
        calls the init function for the super class
        and inherit all the other methods
        '''
        super().__init__(max_rules=max_rules, increments=increments)


        
    def fit( self,train_X:np.ndarray,train_y:list):
        ''' Learns a set of rules that fit the training data
             calls then extends the superclass method.
            Makes repeated use of the method __get_examples_covered_by()
            
            Parameters
            ----------
            train_X - 2D numpy array of instance feature values
                      shape (num_examples, num_features)
            train_y - 1D numpy array of labels, shape(num_examples,0)
        '''

        #  superclass method preprocesses the training set  
        super().fit(train_X,train_y)     
        
        ###== YOUR CODE HERE====####
            ## I suggest you copy in the pseudocode for the function function GreedyRuleInduction
            ##from the lecture then code to that
            ## some of the lines in that pseudocode have been covered above
            ##
            ## HINT 1: you probably want to use the superclass method _get_examples_covered_by()
            ##
            ## HINT 2: smaller_array = numpy.delete(my_array, my_set , axis=0) creates a smaller_array
            ## by removing all the rows from my_array with indexes in the list my_set
            ##
            ## HINT 3: during development it might help to put in varous print() statements
            ## for example, each time around the main loop
            ##
            ##  HINT 4: you can add a 1D array called 'best_new_rule' to the rule set using
            ##.  self.rule_set= np.row_stack((self.rule_set, best_new_rule)).astype(int)

        

        
    
    def predict_one(self, example:np.ndarray)->int:
        '''
        Method that overrides the naive code in the superclass
        function GreedyRuleInduction.
        
        Parameters
         ---------
        example: numpy array of feature values that represent one exanple
    
        Returns: valid label in form of int index into set of values found in the training set
        '''
        prediction=999
        
  
        ###== YOUR CODE HERE====####
        ### Start copy-pasting in the pseudocode for 
        ### function       makePrediction(example,ruleset)
        ###
        ### Hint 1: you should have set self.default_prediction in your fit() method
        ###
        ### Hint 2 : You may well want to make use of the supporting method _meets_conditions() 
        ###
        ### Hint 3: make sure your code changes what is held in the variable prediction!
        return prediction
    

