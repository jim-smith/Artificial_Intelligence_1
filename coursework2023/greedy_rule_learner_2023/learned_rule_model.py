import numpy as np
from typing import Any

NO_PRED=-999

#define some constants for where things are in a rule
FEATURE=0
OPERATOR=1
THRESHOLD=2
LABEL = 3

class LearnedRuleModel:
    '''
    Super Class that holds a model in the form of
    a set of rules that reference a fixed set of operators and a 
    calculated set of labels and theshhold values
    '''
    
    def __init__(self,max_rules:int=5, increments:int=25):
        '''
        Super class constructor
        
        Paramters:
        ----------
        maxRules (int): maximum size of ruleset in the model
        increments (int): number of discrete values  to subdivide
                        the range for each feature        
        
        '''
        #read some user-configurable parameters 
        self.max_rules= max_rules
        self.num_thresholds=increments
        
        # initialise currentModel to be an empty array with no rules 
        self.rule_set = np.empty((0,4),dtype=np.uint)

        
        #allowed operations
        self.operator_set = ("<","==",">")
        self.default_prediction = NO_PRED
        
    
    def get_rule_set(self)->np.ndarray:
        '''
        returns the set of currently learned rules as a 2D numpy array
        '''
        return self.rule_set
    
    def format_rule(self,rule:np.array)->str:
        '''
        formats a single rule as a string
        Parameters:
        rule: 1D numpy array of length 4
        '''
        
        rule_feature = rule[FEATURE]
        rule_operator = self.operator_set[rule[OPERATOR]]
        rule_threshold= self.thresholds[rule_feature][rule[THRESHOLD]]
        rule_label = self.labels[rule[LABEL]]
        formatted = ( f'IF feature {rule_feature} '
                      f'{rule_operator} '
                      f'{rule_threshold:.3f} '
                      f'THEN label= {rule_label}'
                    )
        return formatted
    
    def print_rule_set(self):
        '''
        Formats and prints the current reule set
        '''
        num_rules = self.rule_set.shape[0]
        if num_rules==0:
            print("\t Empty Model - No rules learned")
        else:
            print("\tThe Learned Model is: ")
            for rule in range (num_rules ):
                rule_as_string = self.format_rule( self.rule_set[rule])
                start_string = "\t"
                if rule>0:
                    start_string = "\tELSE "
                print(start_string + rule_as_string)
            
        
    def fit(self, train_X:np.ndarray,train_y:np.ndarray):
        '''
        In the super class this will just preprocess the data but not use it
        
        Sub-classes should call this method then provide extra code to learn a model
        They will also need to set the default label to something valid from the dataset
        
        '''
        
        # store the set of different labels - don't assume what they are
        self.labels = np.unique(train_y)
        self.num_classes = len(self.labels)

        # remember how many features there are describing each training case
        self.num_features= train_X.shape[1]
        
        # preprocess the data to compute the set of thresholds  to be used in rules
        # there are self.num_thresholds of these for each feature
        self._calculate_feature_thresholds(train_X)
        
        # set default label- sub-classes need to override this
        self.default_prediction= NO_PRED
        
        # in sub-classes add code to:
        # (1) learn a set of rules from the training data ..
        # (2) set a sensible default prediction
        # in case the learned rules do not cover all possible examples
    
    def predict(self,examples:np.ndarray)->np.ndarray:
        '''
        Function to make predictions for a set of examples.
        Repeatedly calls a sub-function predict_one()
        
        Parameters
        ----------
        examples: numpy arrays of unlabelled examples
        
        Returns
        ----------
        ypred: a numpy array of predictions, one row for each row in examples.
        
        Values are initialised to self.default_prediction,
        and each will be overwritten if predict_one() returns a value         
        '''
        
        # create an  array to store the predictions in 
        #and fill it with default
        ypred = np.ones(examples.shape[0],dtype=int) * self.default_prediction
        
        # go into a loop making a prediction for each test case
        for i in range (len(ypred)):
            ypred[i] = self.predict_one(examples[i])
                
        # return the predicted label for each test case
        return ypred     
    
    
    def predict_one(self, example:np.ndarray)->int:
        ''' 
        placeholder for code that actually makes a prediction from a learned ruleset
        Sub-class needs to provide an implementation that over-rides this.
         - applying the rule set to see if it makes a prediction
         - or applying the default label otherwise

        This version simply selects random valid labels found in the training set

        Parameters
        ---------
        example: numpy array of feature values that represent one exanple

        Returns: valid label in form of int index into set of values found in the training set
        '''
        #this naive version just makes randon valid prediction
        index= np.random.randint(0, self.num_classes)
        
        return self.labels[index]
                               
                               

    def _calculate_feature_thresholds(self, data:np.ndarray):
        '''
        method to calculate the set of evenly-spaced threshold values to discretise each feature
        so they can be looped over.
        
        Parameters
        ----------
        data: 2D numpy array with one row for each traininfg example 
              and one column for. each feature
              
        Returns:
        2D array with one row for each feature and self.num_thresholds columns
        giving the sets of threshold values for rules to use 
        
        
        result is a set of evenly spaced thresholds for each feature that a rule set can refer to.
        '''
        num_items = data.shape[0]
        self.thresholds = np.empty((self.num_features, self.num_thresholds))
        
        maxValues = np.max(data,axis=0)
        minValues = np.min( data, axis=0)
    
        
        # loop through features
        for this_feature in range (self.num_features):
            minval= minValues[this_feature]
            this_range =  (maxValues[this_feature] - minval )
            this_increment= this_range / self.num_thresholds
            for threshold in range ( self.num_thresholds):
                self.thresholds[this_feature][threshold] = minval + ( threshold * this_increment )

                
    def _meets_conditions( self, instance:np.array,rule:np.array)->bool:
        '''
        method that checks whether  an instance meets the conditions for a rule to fire
        
        Parameters
        ----------
       instance: numpy array for feature values specifying an instance
       rule: numpy array containing tuple of [feature_index, operator, threshold_index,label_index]
                 (values being valid for the training data)
        
        Returns
        _______
              
        True:False depending on whether an instance (example) matches the condition of a rule
        '''

        #interpret the rule and make sure this method is being called correctly
        
        #This is an assertion because it is more serious than
        assert len(rule) == 4, (
                                "error in _meets_conditions() ",
                                "rule must contain exactly four values ",
                                f" not {len(rule)}.\n"
                               )

        
        feature = int(rule[FEATURE])
        assert ( feature >=0 and feature < self.num_features), (
                f'out of range feature id {feature} encountered, ',
                f'should be between 0 and {self.num_features}.')
    
        
        operator = int(rule[OPERATOR])
        assert( operator >=0 and operator < len(self.operator_set) ),(
            f'invalid operator id {operator} encountered, ',
            f'should be between 0 and {len(self.operator_set)}, '
            f' for operator set {self.operator_set}.' )

        
        threshold_id = int(rule[THRESHOLD])
        assert( threshold_id  >=0 and threshold_id < self.num_thresholds),(
            f'invalid threshold index {threshold_id} encountered, ',
            f'should be between 0 and {self.num_thresholds}.')
        
        #all ok so now get the actual threshold
        threshold = self.thresholds[feature][threshold_id]
            
        # and test the relevant conditions for the rule
        if( (operator==0) and  (instance [feature] < threshold) ): # op is "less than"
            return(True)
        elif (operator ==1 and  ( instance [feature] == threshold) ): #op is "equals"
            return True
        elif ( (operator ==2) and ( instance [feature]> threshold)): # op is "greater than"
            return True
        else:
             return False
        
                               
        
    def _get_examples_covered_by(self, rule:np.array, 
                                example_set:np.ndarray,
                                label_set: np.array,
                               )->np.ndarray:
        '''
        Function to find indexes of examples from a set that are covered by the rule
        Returns empty set if rule makes any wrong predictions
        
        
        Parameters
        ---------
        rule: numpy array of [feature,operator, threshold,prediction]
        
        example set: 2d numpy array with one row per example to check,
                     shape = (num_examples, num_features)
        label_set: numpy array holding the actual labels for these examples
                   with one entry for each example to check
                   
        
        Returns
        -------
        array holding indexes where: 
             - the feature values for the row of examples_set meet the rule conditions
             - the rule label matches the corresponding value in  label_set 
        '''                       
        #make sure everything is the right shape
        assert (example_set.shape[1] == self.num_features), (
            f' shape mismatch: example set has {example_set.shape[1]} features, ',
            f' but model expects to see {self.num_features}.')
        
        assert ( example_set.shape[0]== len(label_set)), (
                f' Mismatch: {example_set.shape[0]} examples but {len(label_set)} labels.')
        
        indexes_covered = []
        
        for example in range( example_set.shape[0]):
            if self._meets_conditions(example_set[example], rule) :
                if rule[LABEL] == label_set[example] :
                    indexes_covered.append(example)
                else:
                    indexes_covered = []
                    break
                
                    
        #sanity check
        for index in indexes_covered:
            assert label_set[index]==rule[LABEL]

        return indexes_covered        
        

