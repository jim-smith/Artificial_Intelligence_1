"""Notshared.py
Code for search classes used in lecture.
Not available to students as it is a lab task for them
author:james.smith@uwe.ac.uk, 2024.
"""
from candidatesolution import CandidateSolution
from singlemembersearch import SingleMemberSearch


# ==========================================================================
class DepthFirstSearch(SingleMemberSearch):
    """Implementation of depth first search."""

    def __str__(self) -> str:
        return "depth-first"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Pops and returns oldest thing from openlist.

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        next_soln = CandidateSolution()
        if len(self.open_list) == 0:
            return None
        next_soln = self.open_list.pop()
        return next_soln


# ==========================================================================
class BreadthFirstSearch(SingleMemberSearch):
    """Implements Breadjh First Search."""

    def __str__(self) -> str:
        return "breadth-first"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Pops and returns first thing on openlist.

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        if len(self.open_list) == 0:
            return None
        next_soln = CandidateSolution()
        next_soln = self.open_list.pop(0)
        return next_soln


# ==========================================================================


class LocalSearch(SingleMemberSearch):
    """Implementation of local search."""

    def __str__(self) -> str:
        return "local search"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Pops best thing from list, clears rest of list, then ret.

        Returns
        -------
        next
           working candidate (solution) taken from open list
           if it is an improvem ent
        None
           IF list is empty OR next thing is worse than best so far
        """
        next_soln = CandidateSolution()

        # edge cases
        if len(self.open_list) == 0:
            self.runlog += "LS:empty open list\n"
            return None

        # get best child
        best_index = 0
        best_so_far = self.open_list[0].quality
        self.runlog += f"LS: {len(self.open_list)} children to examine\n"
        for index in range(1, len(self.open_list)):
            quality = self.open_list[index].quality
            if self.a_beats_b(quality, best_so_far):
                best_so_far = quality

        next_soln = self.open_list.pop(best_index)
        self.runlog += (
            f"\t best child quality {best_so_far},\n\t best so far {self.best_so_far}\n"
        )

        # always accept first move
        if self.trials == 1:
            better: bool = True
        # otherwise there must be an improvement
        else:
            better = self.a_beats_b(next_soln.quality, self.best_so_far)
        if better:
            self.best_so_far = next_soln.quality
            return next_soln
        else:
            return None


# ==========================================================================
class BestFirstSearch(SingleMemberSearch):
    """Implementation of BestFirstSearch."""

    def __str__(self):
        return "best first"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Implements Best First by finding, popping and returning member from openlist
        with lowest/highest quality depending on value of self.minimisation.

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        next_soln = CandidateSolution()

        # edge cases
        if len(self.open_list) == 0:
            return None
        # look at quality of first position
        bestindex = 0
        best_so_far = self.open_list[0].quality

        # loop through other looking for something better
        for index in range(1, len(self.open_list)):
            quality = self.open_list[index].quality
            if self.a_beats_b(quality, best_so_far):
                best_so_far = quality
                bestindex = index

        next_soln = self.open_list.pop(bestindex)
        return next_soln


# ==========================================================================
class AStarSearch(SingleMemberSearch):
    """Implementation of A Star  search."""

    def __str__(self):
        return "A star"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Implements AStar by finding, popping and returning member from openlist
        with lowest combined length+quality.

        Returns
        -------
        next working candidate (solution) taken from open list
        """
        CandidateSolution()

        # edge cases
        if len(self.open_list) == 0:
            return None

        # look at quality of first thing in list
        bestindex = 0
        quality = self.open_list[0].quality
        cost = len(self.open_list[0].variable_values)
        # A star look at the combination
        best_so_far = quality + cost

        # then loop through looking to see if there is anything better
        for index in range(1, len(self.open_list)):
            quality = self.open_list[index].quality
            cost = len(self.open_list[index].variable_values)
            combined = quality + cost
            if self.a_beats_b(combined, best_so_far):
                best_so_far = combined
                bestindex = index

        next_soln = self.open_list.pop(bestindex)
        return next_soln


# ==========================================================================


class DijkstraSearch(SingleMemberSearch):
    """Implements Dijkstra by finding, popping and returning member from openlist
    with lowest cost- interpreted as length/complexity.

    Returns
    -------
    next working candidate (solution) taken from open list
    """

    def __str__(self):
        return "Dijkstra search"

    def select_and_move_from_openlist(self) -> CandidateSolution:
        """Void in superclass
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
        next_soln = CandidateSolution()

        # edge cases
        if len(self.open_list) == 0:
            return None

        # look at cost of first solution
        bestindex = 0
        best_so_far = len(self.open_list[0].variable_values)
        # loop through looking for something with lower cost
        for index in range(1, len(self.open_list)):
            cost = len(self.open_list[index].variable_values)
            if cost < best_so_far:
                best_so_far = cost
                bestindex = index

        next_soln = self.open_list.pop(bestindex)
        return next_soln
