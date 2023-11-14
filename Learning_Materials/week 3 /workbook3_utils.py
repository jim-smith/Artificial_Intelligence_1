import matplotlib.pyplot as plt
import copy
import numpy as np
from time import sleep
from IPython.display import clear_output,display




#==========================================================
class Maze: # this assumes maze is rectangular
    # TODO add bounds checking for valid ids
    def __init__(self):
        self.contents = []
        self.width = 0
        self.height = 0
        self.start = 0
        self.goal = 0

    def setup(self, 
                  mazefilename:str =None,
                  start:tuple=(0,0),
                  end:tuple= (10,10)):
        self.loadFromTxt("maze.txt")
        self.setStart(0,9)
        self.setGoal(20,11)

        self.showMaze()


        #define the amount to add to the previous cellid for each move
        # can only do this once the maze has been read in so we know how big it is!
        self.left_move = -1
        self.right_move = 1
        self.up_move = - (self.last_column_id)
        self.down_move = (maze.last_column_id)
        # define the set of move so we can iterate through them
        self.moveSet = [leftMove,downMove,rightMove, upMove]

        return moveSet

    def load_from_txt(self,filename):
        file = open(filename, 'r')
        for line in file.readlines():
            row = []
            for c in line:
                if(c.isspace() and (c!="\n")):
                    row.append(1)
                elif(c!="\n"):
                    row.append(0)
            self.contents.append(row)
        self.height = len(self.contents)
        self.width = len(self.contents[0])
        self.last_column_id = self.width -1

                        
    def show_maze(self,cmap="Set1"):
        green = 0.3
        yellow = 0.65
    
        #colour start and end point
        self.colourCellFromId( self.start,green)
        self.colourCellFromId( self.goal,yellow)
        
        plt.figure(figsize=(5,5))
        plt.imshow(self.contents,cmap=cmap,norm=None)
        plt.xticks(np.arange(0,self.width,2))
        plt.yticks(np.arange(0,self.height,2))

        
    def setStart(self,x,y):
        self.start = y + self.lastColumnId*x
        
    def setGoal(self,x,y):
        self.goal = y + self.lastColumnId*x    

    def cellidToCoords(self,cellid):
        y = cellid% (self.width -1)
        x = int(cellid/(self.lastColumnId))
        return x,y
    
    def coordsToCellid(self,x,y):
        cellid = y+x*(self.lastColumnId)
        return cellid
    
    def colourCellFromId(self,cellid,colour):
        x,y = self.cellidToCoords(cellid)
        self.contents[x][y] = colour

    def evaluate(self, solution:CandidateSolution):
        """
        method to give feedback on the value of a candidate solution

        Parameters
        ----------
        solution: CandidateSolution
            the current attmept being tested

        Returns
        --------
        int
            the quality with -1 for invalid
        string
            the reason why a soltion is invalid
        """
        reason = ""
        quality =1
        
        #we only need to look at the last position for checking
        position = solution.variableValues[-1]
        
        if(len(solution.variableValues)>1):
            lastposition = solution.variableValues[-2]
            xold,yold = self.cellidToCoords(lastposition)
    
        #check is in the maze
        xnew,ynew = self.cellidToCoords(position)
        if ((xnew < 0) or (xnew> self.lastColumnId) or (ynew < 0) or (ynew> (self.height -1))):
            reason = "move takes route out of the maze"
            quality = -1
            
        # and isn;t a wall- which are coded as zero
        elif (maze.contents[xnew][ynew] == 0):
            reason = "move from {},{} to {},{} takes route through wall".format(xold,yold,xnew,ynew)
            quality = -1
    
        # and isn't going backwards
        elif( len(solution.variableValues)>2 and position==solution.variableValues[-3]):
            reason = "move goes back on itself"
            quality=-1
            
        else: # valid move
            #get coords of goal
            x2,y2 = maze.cellidToCoords(maze.goal)
    
            #calculate manhattan distance from pythagoras theorem
            euclideanDistance = np.sqrt( (xnew - x2)*(xnew-x2) + (ynew-y2)*(ynew-y2))
            manhattanDistance = np.abs(xnew-x2) + np.abs(ynew-y2)
        
            quality =  manhattanDistance
            
        
        return quality,reason    

#======================================================


#======================================================
class CandidateSolution:
    def __init__(self):
        self.variableValues = []
        self.quality = 0

#======================================================        
 
#python 3 lets us define the types of parameters if we want to
def IsAtGoal(soln:CandidateSolution, theMaze:Maze): 
    lastCell = soln.variableValues [ len(soln.variableValues) -1]
    if (lastCell== theMaze.goal) :
        return True
    else:
        return False
    
    

   
    
    
    
    
#======================================================           
def displaySearchState(theMaze:Maze, current:CandidateSolution, openList,algname,steps, refresh_rate= 0.0075):
    # make a copy of the maze so we can colour in the paths
    newmaze = copy.deepcopy(theMaze)
 
    #set up the colour scheme
    cmap = "Set1"
    green = 0.3
    yellow = 0.65
    blue = 0.2
    orange = 0.5
    
    startx,starty = newmaze.cellidToCoords(newmaze.start)
    endx,endy = newmaze.cellidToCoords(newmaze.goal)
    
    #colour start and end point
    newmaze.colourCellFromId( newmaze.start,green)
    newmaze.colourCellFromId( newmaze.goal,yellow)
    
    # put the path on the current solution in orange
    for position in current.variableValues:
        newmaze.colourCellFromId(position,orange)
 
    
    # put the endpoints of each partial solution in the openlist in blue
    for item in openList:
        lastpos = item.variableValues[-1]
        newmaze.colourCellFromId(lastpos,blue)

    #leave the old picture on screen for long enough to see then refresh
    sleep(refresh_rate)
    clear_output(wait=True)
    plt.figure(figsize = (7.5,7.5))
    title = f"progress for {algname} after testing {steps} solutions."
    title = title + "\n Current working candidate in orange.\n"
    title = title + "Blue cells indicate solutions on openList"
    plt.title(title)
    plt.axis('off')
    plt.imshow(newmaze.contents,cmap="Set1")
    plt.show()  
    #display(fig)
    
    
#================================================================
import ipywidgets as widgets
import sys
from IPython.display import display
from IPython.display import clear_output
from IPython.display import HTML

def create_multipleChoice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if a==correct_answer_index:
            s = '\x1b[6;30;42m' + "Correct." + '\x1b[0m' +"\n" #green color
        else:
            s = '\x1b[5;30;41m' + "Wrong. " + '\x1b[0m' +"\n" #red color
        with feedback_out:
            clear_output()
            print(s)
        return
    
    check = widgets.Button(description="submit")
    check.on_click(check_selection)
    
    
    return widgets.VBox([description_out, alternativ, check, feedback_out])

Q1 = create_multipleChoice_widget('What type of search is implemented?',['Constructive','Perturbative'],'Constructive')
Q2 = create_multipleChoice_widget('Which algorithm found a path to the goal state after examining the fewest solutions?',['Depth-First','Breadth-First','Best-First','Astar'],'Depth-First')
Q3 = create_multipleChoice_widget('How did the quality of solutions found by depth and breadth first compare?',['depth-first was better','breadth-first was better','they were the same'],'breadth-first was better')
Q4 = create_multipleChoice_widget('Of the algorithms that found the optimal solution, which examined fewest solutions?',['Depth-First','Breadth-First','Best-First','Astar'],'Astar')
Q5 = create_multipleChoice_widget('Does depth-first successfully solve all instances of this problem?',['yes','no'],'no')
Q6 = create_multipleChoice_widget('Does the rank-order of efficiency the complete algorithms depend on the problem instance?',['yes','no'],'yes')
         