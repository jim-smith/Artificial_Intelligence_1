import random
from problem import Problem

class CombinationProblem(Problem):
    """
    Class to create simple combination lock problems
    and report whether a guess opens the lock
    """

    def __init__(self, tumblers: int = 4, num_options: int = 10):
        """Create a new instance with a random solution
        Parameters
        ----------
        tumblers:int
           number of tumblers
           default 4
        num_options:int
           number of possible values (positions) for each tumbler
           this version assumes they are a consecutive integers from 1 to num_options
           default 10
        """

        self.numdecisions = tumblers  # number of tumblers
        # set the allowed values in each position
        self.value_set = []
        for val in range(1, num_options + 1):
            self.value_set.append(val)

        # set  new random goal (unlock code)
        self.goal = []
        for position in range(tumblers):
            new_random_val = random.choice(self.value_set)
            self.goal.append(new_random_val)

    def get_goal(self) -> list:
        """helper function -prints  target combinbation to screen"""
        return self.goal
    
    def set_goal(self,newgoal:list):
        if len(newgoal) != self.numdecisions:
            raise ValueError('newgoal has the wrong length')
        else:
            for pos,val in enumerate(newgoal):
                self.goal[pos]=val

    def evaluate(self, attempt: list) -> int:
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
        Raises
        ------
        ValueError with reason why solution is invalid
        """
        #  how long is the solution?
        N = len(attempt)
        if N is not self.numdecisions:
            raise ValueError( "Error:attempt is wrong length")

        # is the solution made up of valid choices?
        for pos in range(N):
            if attempt[pos] not in self.value_set:
                raise ValueError( "Error: invalid value found in solution")

        # have we found the right combination?
        if attempt == self.goal:
            return 1
        else:
            return 0
        
        
    def display(self, guess: list):
        """Displays a guess at the combination
        simple print as guess does not need any decoding.

        Parameters
        ----------
        attempt : candidateSolution
            object whose variable values are to be displayed
        """
        print(guess)
