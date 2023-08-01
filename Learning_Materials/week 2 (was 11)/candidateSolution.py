"""
candidatesolution.py
Implements a very simple class to hold all the variables associated with a candidate solution to a search problem.
Should probably use some private attributes and provide getters and setters
Author: Jim Snith 2023
"""
class CandidateSolution:
    def __init__(self):
        self.variable_values = []
        self._quality = 0
        self.depth=0
        self._breaks_constraints = False
        self.reason =""
