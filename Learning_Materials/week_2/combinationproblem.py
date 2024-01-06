import numpy as np


class CombinationProblem:
    """
    Class to create simple combination lock problems
    and report whether a guess opens the lock.
    """

    def __init__(self, tumblers: int = 4, num_options: int = 10):
        """Create a new instance with a random solution."""
        self.answer = []
        self.numdecisions = tumblers
        self.num_options = num_options
        self.value_set = []
        for val in range(self.num_options):
            self.value_set.append(val)
        for _position in range(self.numdecisions):
            new_random_val = np.random.randint(0, num_options)
            self.answer.append(new_random_val)

    def evaluate(self, attempt: list) -> tuple[int, str]:
        """Tests whether a provided attempt matches the combination."""

        try:
            assert (
                len(attempt) == self.numdecisions
            )  # stop here if attempt is wrong length
            for val in attempt:
                assert val in self.value_set
            if attempt == self.answer:
                return 1, ""
            else:
                return 0, ""
        except AssertionError:
            errstr = (
                f" attempt had length {len(attempt)}, should have been {self.numdecisions}"
                f"or values were out of range in {attempt}"
            )
            return -1, errstr

    def display(self, guess: list):
        """Displays a guess at the combination
        simple print as guess does not need any decoding.

        Parameters
        ----------
        attempt : candidateSolution
            object whose variable values are to be displayed
        """
        print(guess)
