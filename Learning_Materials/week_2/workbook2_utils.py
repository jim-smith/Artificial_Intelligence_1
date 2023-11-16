import random

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output


# ======================================================
class CandidateSolution:
    def __init__(self):
        self.variable_values = []
        self.quality = 0
        self.depth = 0


# ======================================================
# python 3 lets us define the types of parameters if we want to
def is_atgoal(soln: CandidateSolution):
    if soln.quality == 1:
        return True
    else:
        return False


# ======================================================

# define the encoding we will use for moves
move_names = [
    "empty_0to1",
    "Grain_0to1",
    "Chicken_0to1",
    "Fox_0to1",
    "empty_1to0",
    "Grain_1to0",
    "Chicken_1to0",
    "Fox_1to0",
]

# moveNames = ["b01","G01","C01","F01","b10","G10", "C10", "F10"]


# =====================================================
def evaluate(soln: CandidateSolution) -> str:
    location = [0, 0, 0, 0]
    reason = ""
    boat = 3
    grain = 2
    chicken = 1
    fox = 0
    for move in soln.variable_values:
        if move == 0:
            if location[boat] != 0:
                reason = "boat is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = 1
        elif move == 1:
            if location[boat] != 0 or location[grain] != 0:
                reason = "boat and/or grain is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[grain] = 1
        elif move == 2:
            if location[boat] != 0 or location[chicken != 0]:
                reason = "boat and/or chicken is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[chicken] = 1
        elif move == 3:
            if location[boat] != 0 or location[fox] != 0:
                reason = " boat and/or fox is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[fox] = 1
        elif move == 4:
            if location[boat] != 1:
                reason = "boat is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = 0
        elif move == 5:
            if location[boat] != 1 or location[grain] != 1:
                reason = "boat and/or grain is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[grain] = 0
        elif move == 6:
            if location[boat] != 1 or location[chicken != 1]:
                reason = " boat and/or chicken is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[chicken] = 0
        elif move == 7:
            if location[boat] != 1 or location[fox] != 1:
                reason = " boat and/or fox is in wrong place"
                soln.quality = -1
                break
            else:
                location[boat] = location[fox] = 0

        else:
            print("error- unknown move encountered: " + str(move))

        # check for infeasible partial solutions
        if location[boat] != location[chicken]:
            if location[chicken] == location[fox]:
                reason = "fox eats chicken"
                soln.quality = -1
                break
            if location[chicken] == location[grain]:
                reason = "chicken eats grain"
                soln.quality = -1
                break
        # check for goal
        if location == [1, 1, 1, 1]:
            soln.quality = 1
            print("goal reached")
            break
    return reason


# ==================================================================
def translate_solution_as_string(soln: CandidateSolution):
    len(soln.variable_values)
    movelist = ""
    for move in soln.variable_values:
        # movelist = movelist + " -> " + moveNames [move]
        movelist = movelist + "->" + move_names[move]
    return movelist


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


Q0 = create_multiple_choice_widget(
    "What type of search is the algorithm below implementing?",
    ["Constructive", "Perturbative"],
    "Constructive",
)
Q1 = create_multiple_choice_widget(
    "From your understanding of Depth-First Search, why did the algorithm fail to complete?",
    ["It completed", "It got stuck in a loop", "It was not allowed enough iterations"],
    "It got stuck in a loop",
)
Q2 = create_multiple_choice_widget(
    "Is depth-first search complete", ["yes", "no"], "no"
)
text3 = "What is the minimum depth needed " "to solve the fox-chicken-grain problem?"
Q3 = create_multiple_choice_widget(
    text3,
    ["4", "5", "6", "7", "8"],
    "7",
)
text4 = (
    "Will imposing a maximum depth on the solution  "
    "make Depth-First Search complete successfully "
    "for every problem"
)
Q4 = create_multiple_choice_widget(
    text4,
    ["yes", "no"],
    "no",
)

text5 = (
    "Does the depth of the solution "
    "found by breadth-first match that needed "
    "to solve using the amended version of depth-first?"
)
Q5 = create_multiple_choice_widget(
    text5,
    ["yes", "no"],
    "yes",
)
Q6 = create_multiple_choice_widget(
    "Will the code below finish in success?", ["yes", "no"], "yes"
)
Q7 = create_multiple_choice_widget(
    "Are there more examined solutions for breadth or depth?",
    ["breadth", "depth"],
    "breadth",
)
Q8 = create_multiple_choice_widget(
    "At any point does breadth or depth have a bigger open list?",
    ["breadth", "depth"],
    "breadth",
)


# ===================================================
class TwoInputPerceptron:
    """Simple perceptron used to make learning traces."""

    def __init__(self, learning_rate):
        self.weight1 = random.random()
        self.weight2 = random.random()
        self.biasweight = random.random()
        self.bias = 1
        self.learning_rate = learning_rate
        # print(
        #    " starting with initial random weights "
        #    f'{self.weight1}, {self.weight2} '
        #    )

    def predict(self, input1, input2) -> int:
        """Makes a prediction for a data point.

        Parameters
        ----------
        input1, input2 : int
              variable values that define the data point
        """
        summed_input = (
            input1 * self.weight1 + input2 * self.weight2 + self.bias * self.biasweight
        )
        return 1 if summed_input > 0 else 0

    def update_weights(self, in1, in2, target) -> int:
        """Implements perceptron update rule.

        Parameters
        ----------
        in1 : int
        in2 : int
             together define a s ingle data point
        target : int
                corresponding desired output

        Returns
        -------
        Whether the output was coreect (0) or not (1)
        - used to plot error rate
        """

        error = target - self.predict(in1, in2)
        if error == 0:
            return 0
        else:
            self.biasweight += error * 1 * self.learning_rate  # bias is always +1
            if in1 > 0:
                self.weight1 += error * in1 * self.learning_rate
            if in2 > 0:
                self.weight2 += error * in2 * self.learning_rate
            return 1

    def fit(self, train_x, train_y, max_epochs, verbose=True):
        """Trains weights.

        Parameters
        ----------
        train_x : numpy ndarray
                 training set features
        train_y : numpy.array
                 training set labels
        max_epochs : int
                   when to stop training
        verbose : boolean
        """
        for _epoch in range(max_epochs):
            errors = 0
            # loop over every data point we are given to learn from
            for testcase in range(len(train_y)):
                errors += self.update_weights(
                    train_x[testcase][0], train_x[testcase][1], train_y[testcase]
                )
            if errors == 0:
                break
        return errors

    def get_weights(self):
        """Getter."""
        return self.biasweight, self.weight1, self.weight2


# =======================================
def show_perceptron_landscape():
    # set up grid
    x = np.asarray([0, 0, 0, 1, 1, 0, 1, 1])
    x = x.reshape(4, 2)
    y = [0, 0, 0, 1]
    sample_points = np.empty((0, 4))

    # set up figure to display grid

    _ = plt.figure(figsize=(6, 6))
    ax = plt.axes(projection="3d")

    colours = [
        "gray",
        "blue",
        "lightblue",
        "red",
        "green",
        "darkgreen",
        "orange",
        "brown",
        "purple",
        "black",
    ]
    ax.set_xlabel("w1")
    ax.set_ylabel("w2")
    ax.set_zlabel("errors", labelpad=0)

    # now plot the learning curves of errors vs weights
    for run in range(10):
        # print("run {}".format(run))

        # make new perceptron object
        perceptron = TwoInputPerceptron(0.01)
        for _epoch in range(100):
            # train for one epoch
            errors = perceptron.fit(x, y, max_epochs=1, verbose=False)
            _, w1, w2 = perceptron.get_weights()

            # store weights and errors for these weights
            sample_points = np.vstack((sample_points, [run, w1, w2, errors]))
            if errors == 0:
                # print(f" finished after {epoch} epochs")
                break

        # add run path to plot
        # clear_output()
        data = sample_points[np.where(sample_points[:, 0] == run)]
        zline = data[:, 3]
        xline = data[:, 1]
        yline = data[:, 2]
        this_colour = colours[run % 7]
        ax.plot3D(xline, yline, zline, this_colour, linewidth=2)
