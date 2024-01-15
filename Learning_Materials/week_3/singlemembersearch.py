"""
Singlemembersearch.py
common framework for single member search on graphs.

LINES BEGINNINNG #PS are pseudocode copied from lecture slides
author james.smith@uwe.ac.uk 2023
"""

from copy import deepcopy

from candidatesolution import CandidateSolution
from problem import Problem


class SingleMemberSearch:
    """Common framework for single member search on graphs."""

    def __init__(
        self,
        problem: Problem,
        verbose: bool = False,
        constructive: bool = False,
        max_attempts: int = 50,
    ):
        """Constructor for search algorithm in a given problem.
        starts a search with an empty solution on the open list.

        Parameters
        ----------
        problem : Problem
            the specific instance of a problem to be solved
        verbose : bool (optional)
            the level of feedback
        constructive : bool (optional)
            can solutions have different lengths (True) or not(False)
        max_attempts : int (optional)
            maximum number of solutions to test (to avoid endless loops)
        """

        # Store parameters as instance variables
        self.verbose: bool = verbose
        self.problem: Problem = problem
        self.constructive = constructive
        self.max_attempts: int = max_attempts
        self.algorithm: str = "not set"

        # Implementation specific storage
        self.trials = 0
        self.solved = False
        self.result: list = []
        # list of positions to be changed during search
        self.positions = [-1] if constructive else list(range(0, problem.numdecisions))
        # PS Set open_list, closed_list ← EmptyList
        self.open_list: list = []
        self.closed_list: list = []

        # PS working_candidate ← Initialise (CandidateSolution)
        working_candidate = CandidateSolution()
        # for constructive we start with no moves, depth 0,
        # otherwise start with first valid value in every position
        if not constructive:
            firstval = problem.value_set[0]
            working_candidate.variable_values = [firstval] * problem.numdecisions

        # PS Test ( working_candidate)        Problem-specific code
        working_candidate.quality, _ = self.problem.evaluate(
            working_candidate.variable_values
        )
        if working_candidate.quality == 1:  # lucky guess
            self.trials = 1
            self.result = working_candidate.variable_values
            self.solved = True

        # PS AppendToOpenList(working_candidate)
        self.open_list.append(working_candidate)

    # ============= this function defines which algorithm is being used ================
    def select_and_move_from_openlist(self, algorithm: str) -> CandidateSolution:
        """
        Not intended to be used in super class,
        so throws an assertion if not over-ridden.

        In sub-classes should implement different algorithms
        depending on what item it picks from open_list
        and what it then does to the open list.

        Parameters
        ----------
        algorithm : str
          the name of the algorithm being applied

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        dummy = CandidateSolution()
        errmsg = (
            "The super class is not intended to be called directly.\n"
            "You should call a sub-class where:\n"
            "  - the algorithm name is defined\n"
            " - and get_next_item() is defined.\n"
        )
        assert algorithm == "not set", errmsg
        return dummy

    # =========== Helper function to avoid duplicating effort ====================
    def already_seen(self, attempt: CandidateSolution) -> bool:
        """Checks is an attempt is already in a list."""
        seen = False
        # open list first
        for existing in self.open_list:
            if attempt.variable_values == existing.variable_values:
                seen = True
                break
        # now closed list
        if not seen:
            for existing in self.closed_list:
                if attempt.variable_values == existing.variable_values:
                    seen = True
                    break
        return seen

    # =========== the main search loop ======================================
    def run_search(self) -> bool:
        """The main loop for single member search.
        Returns True/False for success or failure.
        """
        self.trials = 1  # used 1 in init

        # PS  WHILE IsNotEmpty( open_list) DO
        # add a couple of other conditions to provide early stopping
        while (
            self.trials < self.max_attempts
            and len(self.open_list) > 0
            and not self.solved
        ):
            if self.verbose:
                print(f"{len(self.open_list)} candidates on the openList")

            # PS working_candidate <- SelectAndMoveFromOpenList(algorithm_name)
            working_candidate = self.select_and_move_from_openlist(self.algorithm)

            # PS FOR sample in SAMPLE_SIZE DO

            for pos in self.positions:
                for newval in self.problem.value_set:
                    # ==== GENERATE === #
                    # make deepcopy so the original is not changed
                    neighbour = deepcopy(working_candidate)

                    # PS neighbour ← ApplyMoveOperator (working_candidate)
                    if self.constructive:  # extend current solution
                        neighbour.variable_values.append(newval)

                    else:  # perturbative changes existing values
                        neighbour.variable_values[pos] = newval
                        oldval = working_candidate.variable_values[pos]
                        # avoid retesting to be efficient
                        if self.already_seen(neighbour) or newval == oldval:
                            continue

                    # === TEST === #
                    # PS status ← Test ( neighbour)       Problem-specific code
                    neighbour.quality, neighbour.reason = self.problem.evaluate(
                        neighbour.variable_values
                    )
                    self.trials += 1

                    # === UPDATE WORKING MEMORY === #
                    self.update_working_memory(neighbour)
                    if self.solved:
                        return True

            # end over loop of neighbors of working candidate
            # PS AppendToClosedList(workingCandidate)
            self.closed_list.append(working_candidate)

        # while loop has ended
        if not self.solved:
            print("failed to find solution to the problem in the time allowed!")
        return self.solved

    # ======= updates working memory ==========================
    def update_working_memory(self, neighbour: CandidateSolution):
        """Update what we have learned about the problem
        after evaluating a new candidate
        Could have left this code in the main loop
        but separating it out makes it easier to read.
        """
        # PS IF status IS AtGoal THEN Return(SUCCESS)
        # for decision problems this means quality==1
        if neighbour.quality == 1:
            self.result = neighbour.variable_values
            self.solved = True

        # PS ELSE IF status IS BREAKS_CONSTRAINTS THEN
        elif neighbour.quality == -1:
            if self.verbose:
                print(
                    f"because    {neighbour.reason}"
                    f"discarding invalid solution {neighbour.variable_values}: "
                )
            # PS AppendToClosedList(neighbour)
            self.closed_list.append(neighbour)

        # PS ELSE AppendToOpenList(neighbour)
        else:
            if self.verbose:
                print(
                    "adding solution to openlist"
                    f": to examine later: {neighbour.variable_values}"
                )
            self.open_list.append(neighbour)
