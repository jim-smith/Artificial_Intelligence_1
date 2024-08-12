"""Maze.py
author @james.smith@uwe.ac.uk 2024
class for maze as subclass of problem.
"""
from time import sleep

import numpy as np
from IPython.display import clear_output
from matplotlib import pyplot as plt
from problem import Problem


class Maze(Problem):
    """Class definition for a rectangular maze problem."""

    # TODO add bounds checking for valid ids

    def __init__(self, mazefile: str):
        """Constructor.

        Parameter
        ---------
        mazefile(str)
           name of the file holding the maze definition
        """
        self.numdecisions: int = -1  # not fixed, one or more moves
        self.contents: list = []
        self.width: int = 0
        self.height: int = 0
        self.start: int = 0
        self.goal: int = 0

        self.value_set = self.setup(mazefile)

    def setup(self, mazefile: str = "", start: tuple = (0, 0), end: tuple = (10, 10)):
        """Load a maze from a given filename.

        Parameters
        ----------
        mazefile(str)
            name of file gholding definition
        start(tuple(int,int))
             coordinates of starting position
         end (tuple(int,int))
             coordinates of ending position (goal)
        """
        self.load_from_txt(mazefile)
        self.set_start(0, 9)
        self.set_goal(20, 11)

        self.show_maze()

        # define the amount to add to the previous cellid for each move
        # can only do this once the maze has been read in so we know how big it is!
        left_move = -1
        right_move = 1
        up_move = -(self.last_column_id)
        down_move = self.last_column_id
        # define the set of moves so we can iterate through them
        moveset = [left_move, down_move, right_move, up_move]

        return moveset

    def load_from_txt(self, filename):
        """Performs the actual file read."""
        file = open(filename)
        for line in file.readlines():
            row = []
            for c in line:
                if c.isspace() and (c != "\n"):
                    row.append(1)
                elif c != "\n":
                    row.append(0)
            self.contents.append(row)
        self.height = len(self.contents)
        self.width = len(self.contents[0])
        self.last_column_id = self.width - 1

    def save_to_txt(self, filename: str):
        """Write to file as 0s and 1s.

        Parameters
        ----------
        filename(str) name of file to write to
        """
        with open(filename, "w") as outfile:
            for row in self.contents:
                for col in row:
                    if col == 0:
                        outfile.write("1")
                    else:
                        outfile.write(" ")
                outfile.write("\n")

    def show_maze(self, cmap="Set1"):
        """Prints out a maze."""
        green = 0.3
        yellow = 0.65

        # colour start and end point
        self.colour_cell_from_id(self.start, green)
        self.colour_cell_from_id(self.goal, yellow)
        _ = plt.figure(figsize=(5, 5))
        plt.imshow(self.contents, cmap=cmap, norm=None)
        plt.show()

    def show_path(self, solution: list, refresh_rate: float = 0.05):
        """Shows the path through a maze taken by a given solution
        and also the current open list.
        """
        # set up the colour scheme
        green = 0.3
        yellow = 0.65
        blue = 0.2
        orange = 0.5
        purple = 0.4
        red=0.0
        grey = 0.95
        #red, blue,green , purple, orange, yellow,brown,pink, greycalanedqr
        # clear previous paths
        for row in range(len(self.contents)):
            for cell in range(len(self.contents[row])):
                #if self.contents[row][cell]>0.0:#!= red:
                #     self.contents[row][cell] = purple
                if self.contents[row][cell] == orange:
                    self.contents[row][cell] = grey
                if self.contents[row][cell] == blue:
                    self.contents[row][cell] = purple

        startx, starty = self.cellid_to_coords(self.start)
        endx, endy = self.cellid_to_coords(self.goal)

        # colour start and goal point
        self.colour_cell_from_id(self.start, green)
        self.colour_cell_from_id(self.goal, yellow)

        # put the path on the current solution in orange
        for position in solution:
            self.colour_cell_from_id(position, orange)

        # mark endpoint of path in blue
        self.colour_cell_from_id(solution[-1], blue)

        # leave the old picture on screen for long enough to see then refresh
        sleep(refresh_rate)
        clear_output(wait=True)
        _ = plt.figure(figsize=(5, 5))
        title = (
            "Current working candidate in orange.\n"
            "Blue/purple cells indicate endpoints of solutions on open/closed list."
        )
        plt.title(title)
        plt.axis("off")
        plt.imshow(self.contents, cmap="Set1")
        plt.show()

    def set_start(self, x, y):
        """Converts a starting location into a single integer index.

        Parameters
        ----------
        x,y (integers)
             coordinates on grid
        """
        self.start = y + self.last_column_id * x

    def set_goal(self, x, y):
        """
        Cnverts a goal location into a single integer index.

        Parameters
        ----------
        x,y (integers)
        """
        self.goal = y + self.last_column_id * x

    def cellid_to_coords(self, cellid: int) -> tuple[int, int]:
        """Converts an index back to coordinates.

        Parameters
        ----------
        cellid(int)
            index

        Returns
        -------
        tuple(x coordinate,y coordianate)
        """
        y = cellid % (self.width - 1)
        x = int(cellid / (self.last_column_id))
        return x, y

    def coords_to_cellid(self, x, y) -> int:
        """
        Converts a goal location into a single integer index.

        Parameters
        ----------
        x,y (integers)

        Returns
        -------
        cell_id (int)
        """
        cellid = y + x * (self.last_column_id)
        return cellid

    def colour_cell_from_id(self, cellid: int, colour: float):
        """Assigns colour to cell in rectangular representation of maze.

        Parameters
        ----------
        cellid(int)
             index in list representation
        colour (float)
        """
        x, y = self.cellid_to_coords(cellid)
        self.contents[x][y] = colour

    def evaluate(self, solution: list) -> int:
        """
        Method to give feedback on the value of a candidate solution.

        Parameters
        ----------
        solution (list)
            the current attempt being tested
            Represented as a path of coordinates

        Returns
        -------
        int
            the quality with -1 for invalid
        Raises:
        ------
        ValueError(string)
            the reason why a solution is invalid
        """
        reason = ""
        quality = 1

        # no score for a solution that has not started yet
        if len(solution) == 0:
            return 0

        # decode solution to path
        path = [self.start]

        for move in range(len(solution)):
            change = solution[move]
            newpos = path[-1] + change
            path.append(newpos)
        # we only need to look at the last position for checking
        position = path[-1]

        if len(path) > 1:
            lastposition = path[-2]
            xold, yold = self.cellid_to_coords(lastposition)

        # check is in the maze
        xnew, ynew = self.cellid_to_coords(position)
        if (
            (xnew < 0)
            or (xnew > self.last_column_id)
            or (ynew < 0)
            or (ynew > (self.height - 1))
        ):
            reason = "move takes route out of the maze"
            raise ValueError(reason)

        # and isn't a wall- which are coded as zero
        elif self.contents[xnew][ynew] == 0:
            reason = (
                f"move from {xold},{yold} to {xnew},{ynew} takes route through wall"
            )
            raise ValueError(reason)

        # and isn't going backwards
        elif len(path) > 2 and position == path[-3]:
            reason = "path goes backwards"
            raise ValueError(reason)

        else:  # valid move
            # get coords of goal
            x2, y2 = self.cellid_to_coords(self.goal)

            # calculate euclidean and manhattan distance
            np.sqrt((xnew - x2) * (xnew - x2) + (ynew - y2) * (ynew - y2))
            manhattan_distance = np.abs(xnew - x2) + np.abs(ynew - y2)

            quality = manhattan_distance
            self.show_path(path)
            # print(f'solution {solution} decodes to {path}\n'
            #      f'  score is {quality} because{reason}'
            #      )
        return quality

    def is_at_goal(self, solution: list) -> bool:
        """Says is a solution is at the maze goal.

        Parameters
        ----------
        solution : List
            the current attempt being tested
            Represented as a path of coordinates
        """
        last_cell = solution[-1]
        if last_cell == self.goal:
            return True
        else:
            return False


# ======================================================
