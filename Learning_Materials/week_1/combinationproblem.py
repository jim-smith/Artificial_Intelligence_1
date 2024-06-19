from candidatesolution import CandidateSolution
from problem import Problem
import random

class CombinationProblem(Problem):
    """
    Class to create simple combination lock problems
    and report whether a guess opens the lock
    """

    def __init__(self, N: int = 4, num_options: int = 10):
        """Create a new instance with a random solution
        Parameters
        ----------
        N:int
           number of tumblers
           default 4
        num_options:int
           number of possible values (positions) for each tumbler
           this version assumes they are a consecutive integers from 1 to num_options
           default 10
        """

        self.solution_length = N  # number of tumblers
        # set the allowed values in each position
        self.value_set = []
        for val in range(1, num_options + 1):
            self.value_set.append(val)

        # set  new random goal (unlock code)
        self.goal = []
        for position in range(N):
            new_random_val = random.choice(self.value_set)
            self.goal.append(new_random_val)

    def print_goal(self) -> str:
        """helper function -prints  target combinbation to screen"""
        return f"{self.goal}"

    def evaluate(self, attempt: CandidateSolution) -> (int, str):
        """
        Tests whether a provided attempt matches the combination
        Parameters
        ----------
        attempt: list
            list of values that define a proposed solution
        Returns
        ---------
        int
            quality
            -1 means  attempt is invalid, (e.g. too few or wrong values)
            0 means valid but incorrect,
            1 means correct
        str
            reason why solution is invalid
            empty string if solution is ok
        """
        #  how long is the solution?
        N = len(attempt.variable_values)
        if N is not self.solution_length:
            return -1, "attempt is wrong length"

        # is the solution made up of valid choices?
        for pos in range(N):
            if attempt.variable_values[pos] not in self.value_set:
                return -1, "error, invalid value found in solution"

        # have we found the right combination?
        if attempt.variable_values == self.goal:
            return 1, ""
        else:
            return 0, ""

