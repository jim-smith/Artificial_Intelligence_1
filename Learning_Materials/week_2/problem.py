"""Python implementation of superclass for problems
author:james.smith@uwe.ac.uk 2023.
"""


class Problem:
    """Generic super class we will use for problems."""

    def __init__(self):
        self.numdecisions: int = -1
        self.value_set: list = []

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

        return -1, "evaluation function has not been defined for problem!"
