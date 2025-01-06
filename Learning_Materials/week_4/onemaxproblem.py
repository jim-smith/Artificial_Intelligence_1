"""Python implementation of superclass for problems
author:james.smith@uwe.ac.uk 2023.
"""
import numpy as np
from problem import Problem
class OneMaxBinary(Problem):
    """OneMax problem with N binary decisions.
    quality is number of decisions with value 1
    in other words, the sum of the decision variables
    uses assertions to ensure solutions are valid
    """

    def __init__(self, N = 20):
        self.numdecisions: int = N
        self.value_set: list = [0,1]

    def evaluate(self, solution: list) -> int:
        """Evaluate function.

        Parameters
         ----------
         attempt : list
             list of values that define a proposed solution

         Returns
         -------
         int
             quality
             -1 means invalid,
         Raises
         -------
         ValueError(str)
             reason why solution is invalid
        """
        
        score = 0.0
        # validity checking
        for val in solution:
            if not val in self.value_set:
                errmsg = f"invalid value {val} found in solution"
                raise ValueError(errmsg)
            
        
        if len(solution)!= self.numdecisions:
            errmsg = (f'solution has length {len(solution)} '
                      'should be {self.numdecisions}'
                     )
            raise ValueError(errmsg)
        
        # calculate score
        for i in range (self.numdecisions):
            score += solution[i]
        return score

class OneMaxContinuous(Problem):
    """OneMax problem with N  decisions in [0,1].
    uses assertions to ensure solutions are valid
    and self.value_set is interpeted as limits (min,max) on acceptable range of values
    
    The quality is sum of the  squares of the distance of decision variables from 1.0
    i.e sum of (1.0 - decision)^2
    This means we can also provide a gradient function
    
    """

    def __init__(self, N = 20):
        self.numdecisions: int = N
        self.value_set: list = [0,2]
        self.gradient:np.array= np.zeros(N) 
        self.target:np.array= np.ones(N) 

    def evaluate(self, solution: list) -> int:
        """Evaluate function.
        Sum of squared distance from 1.0 for each decision
        Parameters
         ----------
         attempt : list
             list of values that define a proposed solution

         Returns
         -------
         int
             quality
             -1 means invalid,
         Raises
         -------
             ValueError(str)
             reason why solution is invalid
        """
        
        score = 0.0
        #convert to numpy array for ease
        solution = np.asarray(solution)

        # validity checking
        max = np.max(solution)
        min = np.min(solution)
        if  min < self.value_set[0]:
            errmsg=f'Error: found value {min} outside valid range {self.value_set}.'
            raise ValueError(errmsg)
        if max > self.value_set[1]:
            errmsg=f'Error: found value {max} outside valid range {self.value_set}.'
            raise ValueError(errmsg)

        if solution.shape[0]!= self.numdecisions:
            errmsg = (f"solution has length {solution.shape[0]}"
                      f"should be {self.numdecisions}"
                     )
            raise ValueError(errmsg)
        
        # calculate gradient and score
        self.gradient = self.target - solution
        score = 0.5 * np.square(self.gradient).sum() 

        # round to 2 significant digits
        score=round(score,2)
            
        return score
    
    def get_gradient(self):
        return self.gradient