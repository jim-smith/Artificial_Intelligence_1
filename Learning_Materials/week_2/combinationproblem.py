import random


class CombinationProblem:
    """
    Class to create simple combination lock problems
    and report whether a guess opens the lock.
    """

    def __init__(self, tumblers: int = 4, num_options: int = 10):
        """Create a new instance with a random solution.

        Parameters
        ----------
        tumblers : int   number of wheels in the lock
        num_options : int.  number of different positions each wheel can be in
        """

        self.numdecisions = tumblers  # how many decisions *must* valid solution specify
        self.num_options = num_options  # how many values can each decision take
        self.value_set = list(range(0, num_options))

        # use random.choices to create a list holding the combination to be guessed
        self.answer = random.choices(self.value_set, k=self.numdecisions)

    def evaluate(self, attempt: list) -> tuple[int, str]:
        """Tests whether a provided attempt matches the combination."""

        try:  # use try ...except with assertions to make our code more robust
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
