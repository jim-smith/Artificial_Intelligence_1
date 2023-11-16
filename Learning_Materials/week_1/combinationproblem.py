import numpy as np
class CombinationProblem:
    """ 
    Class to create simple combination lock problems
    and report whether a guess opens the lock
        """
    def __init__(self,N:int=4,num_options:int =10):
        """ Create a new intance with a random solution"""
        self.answer = []
        self.num_options=num_options
        for position in range(N):
            new_random_val= np.random.randint(0,num_options)
            self.answer.append(new_random_val)
        print(f' The new code to find is {self.answer}')
        
        
    def evaluate(self, attempt:list)->bool:
        """ Tests whether a provided attempt matches the combination"""
        try:
            assert len(attempt) == N # stop here if attempt is wrong length
            for pos in range(N):
                assert attempt[pos] >0
                assert attempt[pos] <num_options
                #stop if any digit is out of range
            if attempt == self.answer :
                return True
            else:
                return False
        except AssertionError:
            print(f' attempt had length {len(attempt)}, should have been {N}')
            print('or values were out of range')
            return False
        
