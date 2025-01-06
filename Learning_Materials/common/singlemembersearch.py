"""

Singlemembersearch.py
author james.smith@uwe.ac.uk 2023


This class implements the pseudocode for a 
common framework for single member search,
as described in the lectures for Artificial Intelligence 1.

Comment lines that begin with === PS are directly copied from the pseudocode
There are a lot of helper functions to try and make the main code more readable

"""

from copy import deepcopy

from candidatesolution import CandidateSolution
from problem import Problem

# this needs to be bigger than the quality is ever likely to be
BIGNUM = 10000000




class SingleMemberSearch:
    """Common framework for single member search on graphs.
    Attributes not definied in init method:
        open_list : list (of CandidateSolutions)
            the list of known solutions to be explored
        closed_list: : list (of CandidateSolutions)
            the list of known solutions we have explored
    
    """

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
            if we know the best possible quality  (e.g. 100% accuracy)
        """

        # Store parameters as instance variables
        self.problem: Problem = problem
        self.constructive: bool = constructive
        self.max_attempts: int = max_attempts
        self.minimise: bool = minimise
        self.target_quality = target_quality

        # Implementation specific storage
        self.runlog:str = ""  # any messages we want to store"
        self.trials = 0  # number of attempts so far
        self.solved = False  # have we reached the goal?
        self.best_so_far = BIGNUM
        self.result: list = []  # best solution found
        # list of positions where change can happen during search 
        self.positions = [-1] if constructive else list(range(0, problem.numdecisions))

        # === Pseudocode: Set open_list, closed_list ← EmptyList
        self.open_list: list = []
        self.closed_list: list = []

        #  === Pseudocode:  working_candidate ← Initialise (CandidateSolution)
        working_candidate = CandidateSolution()
        if constructive:
            working_candidate.variable_values = []
        else:
            firstval = problem.value_set[0]   # use first valid value in every pos
            working_candidate.variable_values = [firstval] * problem.numdecisions

        #  === Pseudocode:  Test ( working_candidate)  ======      Problem-specific code

        if self.constructive and self.minimise:
            working_candidate.quality = BIGNUM
        else:
            try:
                working_candidate.quality = self.problem.evaluate(
                working_candidate.variable_values
            )
            except ValueError as e:
                print(f'initial guess was invalid because {e}')
                working_candidate.quality = BIGNUM if self.minimise else 0
                

        # normally we want to remember quality of best solution seen during search
        self.best_so_far = working_candidate.quality

        # check for lucky first guess (only really likely for perturbative)
        if working_candidate.quality == target_quality:  # lucky guess
            self.trials = 1
            self.result = working_candidate.variable_values
            self.solved = True

        #  === Pseudocode:  AppendToOpenList(working_candidate)
        self.open_list.append(working_candidate)


    def __str__(self) -> str:
        """   Returns name of algorithm  """
        return "not set"



    # ============= this function defines which algorithm is being used ================
    def select_and_move_from_openlist(self) -> CandidateSolution:
        """
        Not intended to be used in super class.
        Overridden in sub-classes to implement different algorithms

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        dummy = CandidateSolution()
        errmsg = (
            "The super class is not intended to be called directly.\n"
            "You should over-ride this message in your sub-class.\n"
        )
        assert self.__str__() == "not set", errmsg
        return dummy


    # =========== the main search loop ======================================
    def run_search(self) -> bool:
        """The main loop for single member search.
        Returns True/False for success or failure.
        """
        self.trials = 1  # used 1 in init

        # === Pseudocode:  WHILE IsNotEmpty( open_list) DO
        # add a couple of other conditions to provide early stopping
        while self.trials < self.max_attempts and not self.solved:
            self.runlog += f"{len(self.open_list)} candidates on the openList.\n"

            # === Pseudocode: working_candidate <- SelectAndMoveFromOpenList(algorithm_name)
            working_candidate = self.select_and_move_from_openlist()
            if working_candidate is None:
                self.runlog += "ran out of promising solutions to test\n"
                return False

            # === Pseudocode: FOR sample in SAMPLE_SIZE DO
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
                    # === Pseudocode: status ← Test ( neighbour)       Problem-specific code
                    invalid_reason =''
                    try:
                        neighbour.quality = self.problem.evaluate(
                                                neighbour.variable_values
                                                )
                    except ValueError as e:
                        invalid_reason= e
                        neighbour.quality = BIGNUM if self.minimise else 0
                    self.trials += 1

                    # === UPDATE WORKING MEMORY === #
                    self.update_working_memory(neighbour,invalid_reason)
                    if self.solved:
                        return True

            # end over loop of neighbors of working candidate
            # === Pseudocode: AppendToClosedList(workingCandidate)
            self.closed_list.append(working_candidate)

        # while loop has ended
        if not self.solved:
            self.runlog += "failed to find solution to the problem in the time allowed!"
        return self.solved

    # ======= updates working memory ==========================
    def update_working_memory(self, neighbour: CandidateSolution,reason:str):
        """Update what we have learned about the problem
        after evaluating a new candidate
        Could have left this code in the main loop
        but separating it out makes it easier to read.
        """
        # === Pseudocode: IF status IS AtGoal THEN Return(SUCCESS)
        # for decision problems this means quality==1
        if neighbour.quality == self.target_quality:
            self.result = neighbour.variable_values
            self.solved = True

        # === Pseudocode: ELSE IF status IS BREAKS_CONSTRAINTS THEN
        elif reason != "":
            self.runlog += (
                f"discarding invalid solution {neighbour.variable_values} "
                f"because    {reason}\n"
            )
            # PS AppendToClosedList(neighbour)
            self.closed_list.append(neighbour)

        # === Pseudocode: ELSE AppendToOpenList(neighbour)
        else:
            self.runlog += (
                "adding solution to openlist"
                f": to examine later: {neighbour.variable_values}\t"
                f" quality {neighbour.quality}\n"
            )
            self.open_list.append(neighbour)


# =========== Helper functions  ====================            
   
    def a_better_than_b(self, a: int, b: int) -> bool:
        """ Compares two solutions taking into account whether we are minimising."""
        better: bool = False
        if a < b and self.minimise:
            better = True
        if a > b and not self.minimise:
            better = True
        return better

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
