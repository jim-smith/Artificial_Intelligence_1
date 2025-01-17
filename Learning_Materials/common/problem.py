"""Python implementation of superclass for problems
author:james.smith@uwe.ac.uk 2023.
"""


class Problem:
    """Generic super class we will use for problems."""

    def __init__(self):
        self.numdecisions: int = -1
        self.value_set: list = []

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
         -----
         ValueError(str)
             reason why solution is invalid
         or
         NotImplementedException
          if the sub class has not implemented an evaluate() method
        """
        raise NotImplementedException("evaluation function has not been defined for problem!")
        return -1, 
