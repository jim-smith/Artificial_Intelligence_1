"""
Singlemembersearch.py
common framework for single member search on graphs.

LINES BEGINNINNG #PS are pseudocode copied from lecture slides
author james.smith@uwe.ac.uk 2023
"""

from copy import deepcopy

from candidatesolution import CandidateSolution
from problem import Problem

# this needs to be bigger than the quality is ever likely to be
BIGNUM = 10000000


class SingleMemberSearch:
    """Common framework for single member search on graphs."""

    def __init__(
        self,
        problem: Problem,
        constructive: bool = False,
        max_attempts: int = 50,
        minimise=True,
        target_quality=1,
    ):
        """Constructor for search algorithm in a given problem.
        starts a search with an empty solution on the open list.

        Parameters
        ----------
        problem : Problem
            the specific instance of a problem to be solved
        constructive : bool (optional)
            can solutions have different lengths (True) or not(False)
        max_attempts : int (optional)
            maximum number of solutions to test (to avoid endless loops)
        minimise : bool
            whether the aim is find a solution with  minimum or maximum quality
        target_quality : int
            sometimes we know the best possible quality
            (e.g. 100% accuracy)
        """

        # Store parameters as instance variables
        self.problem: Problem = problem
        self.constructive = constructive
        self.max_attempts: int = max_attempts
        self.minimise = minimise

        # Implementation specific storage
        self.runlog = ""  # any messages we want to store"
        self.trials = 0  # number of attempts so far
        self.solved = False  # have we resched the goal?
        self.best_so_far = BIGNUM
        self.result: list = []  # best solution found
        # list of positions to be changed during search loop
        # i.e. just the last for constructive or all for perturbative
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
        if self.constructive and self.minimise:
            working_candidate.quality = BIGNUM
        else:
            working_candidate.quality, _ = self.problem.evaluate(
                working_candidate.variable_values
            )

        # normally we want to remember quality of best solution seen during search
        self.best_so_far = working_candidate.quality

        # check for lucky first guess (only really likely for perturbative)
        if working_candidate.quality == target_quality:  # lucky guess
            self.trials = 1
            self.result = working_candidate.variable_values
            self.solved = True

        # PS AppendToOpenList(working_candidate)
        self.open_list.append(working_candidate)

    def __str__(self) -> str:
        """Returns name of algorithm
        not set in superclass.
        """
        return "not set"

    def a_beats_b(self, a: int, b: int) -> bool:
        """Comparison taking into account whether we are minimising."""
        better: bool = False
        if a < b and self.minimise:
            better = True
        if a > b and not self.minimise:
            better = True
        return better

    # ============= this function defines which algorithm is being used ================
    def select_and_move_from_openlist(self) -> CandidateSolution:
        """
        Not intended to be used in super class,
        so throws an assertion if not over-ridden.

        In sub-classes should implement different algorithms
        depending on what item it picks from open_list
        and what it then does to the open list.

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
        assert self.__str__() == "not set", errmsg
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
        while self.trials < self.max_attempts and not self.solved:
            self.runlog += f"{len(self.open_list)} candidates on the openList.\n"

            # PS working_candidate <- SelectAndMoveFromOpenList(algorithm_name)
            working_candidate = self.select_and_move_from_openlist()
            if working_candidate is None:
                self.runlog += "ran out of promising solutions to test\n"
                return False

            # PS FOR sample in SAMPLE_SIZE DO
            self.runlog += (
                " Next iteration working candidate quality "
                f"{working_candidate.quality}.\n"
            )
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
            self.runlog += "failed to find solution to the problem in the time allowed!"
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
        elif neighbour.reason != "":
            self.runlog += (
                f"discarding invalid solution {neighbour.variable_values} "
                f"because    {neighbour.reason}\n"
            )
            # PS AppendToClosedList(neighbour)
            self.closed_list.append(neighbour)

        # PS ELSE AppendToOpenList(neighbour)
        else:
            self.runlog += (
                "adding solution to openlist"
                f": to examine later: {neighbour.variable_values}\t"
                f" quality {neighbour.quality}\n"
            )
            self.open_list.append(neighbour)
