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

    def evaluate(self, solution: list) -> tuple[int, str]:
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
         str
             reason why solution is invalid
             empty string if solution is ok
        """
        
        score = 0.0
        # validity checking
        for val in solution:
            errmsg1 = f"invalid value {val} found in solution"
            assert val in self.value_set,errmsg1
            
        errmsg = f"solution has length {len(solution)} should be {self.numdecisions}"
        assert len(solution)== self.numdecisions, errmsg2
        
        # calculate score
        for i in range (self.numdecisions):
            score += solution[i]
        return score, ""

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
        self.value_set: list = [0,1]
        self.gradient:np.array= np.zeros(N) 
        self.target:np.array= np.ones(N)

    def evaluate(self, solution: list) -> tuple[int, str]:
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
         str
             reason why solution is invalid
             empty string if solution is ok
        """
        
        score = 0.0
        #convert to numpy array for ease
        solution = np.asarray(solution)

        # validity checking
        max = np.max(solution)
        min = np.min(solution)
        assert  min >= self.value_set[0],f'Error: found value {min} outside valid range'
        assert max <= self.value_set[1],f'Error: found value {max} outside valid range'
            
        errmsg = f"solution has length {solution.shape[0]} should be {self.numdecisions}"
        assert solution.shape[0]== self.numdecisions, errmsg2
        
        # calculate gradient and score
        self.gradient = self.target-solution
        score = np.square(self.gradient).sum() 
        # round to 6 sdignificant digits
        score=round(score,2)
            
        # toggle flag on whether gradient wil lbe new
        return score, ""
    
    def get_gradient(self):
        return self.gradient