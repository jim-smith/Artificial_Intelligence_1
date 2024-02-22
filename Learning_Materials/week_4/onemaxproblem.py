"""Python implementation of superclass for problems
author:james.smith@uwe.ac.uk 2023.
"""

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
    quality is sum of the  decision variables
    uses assertions to ensure solutions are valid
    
    self.value_set is interpeted as limits (min,max) on acceptable range of values
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
            assert val >= self.value_set[0],errmsg1
            assert val <= self.value_set[1],errmsg1
            
        errmsg = f"solution has length {len(solution)} should be {self.numdecisions}"
        assert len(solution)== self.numdecisions, errmsg2
        
        # calculate score
        for i in range (self.numdecisions):
            score += solution[i]
        return score, ""