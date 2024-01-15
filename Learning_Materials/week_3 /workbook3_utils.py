import copy
from time import sleep

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

from ../week_2/candidatesolution import CandidateSolution
from ../week_2/problem import Problem


# ==========================================================
class Maze:  # this assumes maze is rectangular
    # TODO add bounds checking for valid ids
    def __init__(self):
        self.contents = []
        self.width = 0
        self.height = 0
        self.start = 0
        self.goal = 0

    def setup(
        self, mazefilename: str = "", start: tuple = (0, 0), end: tuple = (10, 10)
    ):
        self.load_from_txt("maze.txt")
        self.set_start(0, 9)
        self.set_goal(20, 11)

        self.show_maze()

        # define the amount to add to the previous cellid for each move
        # can only do this once the maze has been read in so we know how big it is!
        self.left_move = -1
        self.right_move = 1
        self.up_move = -(self.last_column_id)
        self.down_move = self.last_column_id
        # define the set of move so we can iterate through them
        self.move_set = [self.left_move, self.down_move, self.right_move, self.up_move]

        return self.move_set

    def load_from_txt(self, filename):
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

    def show_maze(self, cmap="Set1"):
        green = 0.3
        yellow = 0.65

        # colour start and end point
        self.colour_cell_from_id(self.start, green)
        self.colour_cell_from_id(self.goal, yellow)

        plt.figure(figsize=(5, 5))
        plt.imshow(self.contents, cmap=cmap, norm=None)
        plt.xticks(np.arange(0, self.width, 2))
        plt.yticks(np.arange(0, self.height, 2))

    def set_start(self, x, y):
        self.start = y + self.last_column_id * x

    def set_goal(self, x, y):
        self.goal = y + self.last_column_id * x

    def cellid_to_coords(self, cellid):
        y = cellid % (self.width - 1)
        x = int(cellid / (self.last_column_id))
        return x, y

    def coords_to_cellid(self, x, y):
        cellid = y + x * (self.last_column_id)
        return cellid

    def colour_cell_from_id(self, cellid, colour):
        x, y = self.cellid_to_coords(cellid)
        self.contents[x][y] = colour

    def evaluate(self, solution: CandidateSolution):
        """
        Method to give feedback on the value of a candidate solution.

        Parameters
        ----------
        solution : CandidateSolution
            the current attempt being tested

        Returns
        -------
        int
            the quality with -1 for invalid
        string
            the reason why a solution is invalid
        """
        reason = ""
        quality = 1

        # we only need to look at the last position for checking
        position = solution.variable_values[-1]

        if len(solution.variable_values) > 1:
            lastposition = solution.variable_values[-2]
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
            quality = -1

        # and isn;t a wall- which are coded as zero
        elif self.contents[xnew][ynew] == 0:
            reason = (
                f"move from {xold},{yold} to {xnew},{ynew} takes route through wall"
            )
            quality = -1

        # and isn't going backwards
        elif (
            len(solution.variable_values) > 2
            and position == solution.variable_values[-3]
        ):
            reason = "move goes back on itself"
            quality = -1

        else:  # valid move
            # get coords of goal
            x2, y2 = self.cellid_to_coords(self.goal)

            # calculate manhattan distance from pythagoras theorem
            np.sqrt((xnew - x2) * (xnew - x2) + (ynew - y2) * (ynew - y2))
            manhattan_distance = np.abs(xnew - x2) + np.abs(ynew - y2)

            quality = manhattan_distance

        return quality, reason

    def is_at_goal(self, soln: CandidateSolution) -> bool:
        """Says is a soltino is at the maze goal."""
        last_cell = soln.variable_values[len(soln.variable_values) - 1]
        if last_cell == self.goal:
            return True
        else:
            return False


# ======================================================


# ======================================================
def display_search_state(
    the_maze: Maze,
    current: CandidateSolution,
    open_list,
    algname,
    steps,
    refresh_rate=0.0075,
):
    # make a copy of the maze so we can colour in the paths
    newmaze = copy.deepcopy(the_maze)

    # set up the colour scheme
    green = 0.3
    yellow = 0.65
    blue = 0.2
    orange = 0.5

    startx, starty = newmaze.cellid_to_coords(newmaze.start)
    endx, endy = newmaze.cellid_to_coords(newmaze.goal)

    # colour start and end point
    newmaze.colour_cell_from_id(newmaze.start, green)
    newmaze.colour_cell_from_id(newmaze.goal, yellow)

    # put the path on the current solution in orange
    for position in current.variable_values:
        newmaze.colour_cell_from_id(position, orange)

    # put the endpoints of each partial solution in the openlist in blue
    for item in open_list:
        lastpos = item.variable_values[-1]
        newmaze.colour_cell_from_id(lastpos, blue)

    # leave the old picture on screen for long enough to see then refresh
    sleep(refresh_rate)
    clear_output(wait=True)
    plt.figure(figsize=(5, 5))
    title = f"progress for {algname} after testing {steps} solutions."
    title = title + "\n Current working candidate in orange.\n"
    title = title + "Blue cells indicate solutions on openList"
    plt.title(title)
    plt.axis("off")
    plt.imshow(newmaze.contents, cmap="Set1")
    plt.show()
    # display(fig)


# ================================================================


def create_multiple_choice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)

    correct_answer_index = options.index(correct_answer)

    radio_options = [(words, i) for i, words in enumerate(options)]
    alternative = widgets.RadioButtons(
        options=radio_options, description="", disabled=False
    )

    description_out = widgets.Output()
    with description_out:
        print(description)

    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternative.value)
        if a == correct_answer_index:
            s = "\x1b[6;30;42m" + "Correct." + "\x1b[0m" + "\n"  # green color
        else:
            s = "\x1b[5;30;41m" + "Wrong. " + "\x1b[0m" + "\n"  # red color
        with feedback_out:
            clear_output()
            print(s)
        return

    check = widgets.Button(description="submit")
    check.on_click(check_selection)

    return widgets.VBox([description_out, alternative, check, feedback_out])


Q1 = create_multiple_choice_widget(
    "What type of search is implemented?",
    ["Constructive", "Perturbative"],
    "Constructive",
)
Q2 = create_multiple_choice_widget(
    "Which algorithm found a path to the goal state after examining the fewest solutions?",
    ["Depth-First", "Breadth-First", "Best-First", "Astar"],
    "Depth-First",
)
Q3 = create_multiple_choice_widget(
    "How did the quality of solutions found by depth and breadth first compare?",
    ["depth-first was better", "breadth-first was better", "they were the same"],
    "breadth-first was better",
)
Q4 = create_multiple_choice_widget(
    "Of the algorithms that found the optimal solution, which examined fewest solutions?",
    ["Depth-First", "Breadth-First", "Best-First", "Astar"],
    "Astar",
)
Q5 = create_multiple_choice_widget(
    "Does depth-first successfully solve all instances of this problem?",
    ["yes", "no"],
    "no",
)
text6 = (
    "Does the rank-order of efficiency for "
    "the complete algorithms depend on the problem instance?"
)
Q6 = create_multiple_choice_widget(
    text6,
    ["yes", "no"],
    "yes",
)
