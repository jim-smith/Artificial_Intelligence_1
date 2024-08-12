"""
Candidatesolution.py
Implements a very simple class
to hold all the variables associated with a candidate solution to a search problem.
Should probably use some private attributes and provide getters and setters
Author: Jim Smith 2023.
"""


class CandidateSolution:
    def __init__(self):
        self.variable_values = []
        self.quality = 0
        self.meets_constraints = False
        self.reason = ""

    def print_values(self):
        print(self.variable_values)
