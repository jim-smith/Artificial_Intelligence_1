import copy
from time import sleep

import ipywidgets as widgets
import matplotlib.pyplot as plt
from candidatesolution import CandidateSolution
from IPython.display import clear_output
from maze import Maze


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
