#======================================================
class CandidateSolution:
    def __init__(self):
        self.variableValues = []
        self.quality = 0
        self.depth=0
        self.breaks_constraints = False
        self.reason =""