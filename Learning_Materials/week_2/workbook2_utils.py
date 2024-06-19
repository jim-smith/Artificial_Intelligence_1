import random

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output


def create_multiple_choice_widget(description, options, correct_answer_index):
    # if correct_answer not in options:
    #    options.append(correct_answer)
    layout = widgets.Layout(width="auto", height="auto")  # set width and height

    # correct_answer_index = options.index(correct_answer)

    radio_options = [(words, i) for i, words in enumerate(options)]
    alternative = widgets.RadioButtons(
        options=radio_options, description="", disabled=False, layout=layout
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


yesno = ["yes", "no"]
yes = 0
no = 1

# =============== actual questions
#
q0text = "Is depth-first search complete"
q0 = create_multiple_choice_widget(q0text, yesno, no)
#
#
q1text = (
    "Lines 171--174 of the code implementation singlemembersearch.py extend the pseudocode.\n"
    "Which reason do you think is most likely?"
)
q1options = [
    "To avoid memory leaks",
    "To prevent depth-first search getting stuck in loops",
    "To reduce the chances that any algorithm will get stuck in loops",
]
q1 = create_multiple_choice_widget(q1text, q1options, 2)
#
#
q2text = (
    "Lines 171--174 of singlemembersearch.py "
    "prevent duplicate **encoded** representations of candidate solutions.\n"
    "For a constructive search, "
    "will this guarantee there are no loops?"
)
q2 = create_multiple_choice_widget(q2text, yesno, no)
#
#
q3text = (
    "Does the function test_breadthfirst_combination() "
    "fully test all of the class Breadth-First search?"
)
q3 = create_multiple_choice_widget(q3text, yesno, no)
#
#
q4text = (
    "which of these situations would cause the code to fail,"
    " but are NOT picked up by the tests"
)
q4options = [
    " If the algorithm code produced a solution with invalid values for decision",
    "A solution had with more or less values than the number of tumblers in a lock",
    "Neither of the above",
    "Both of the above",
]
q4 = create_multiple_choice_widget(q4text, q4options, 3)
#
#
q5text = (
    "How many candidate solutions were allowed before the search process completed?"
)
q5options = ["100", "500", "1000", "5000", "10000", "unlimited"]
q5 = create_multiple_choice_widget(q5text, q5options, 2)
#
#
q6text = (
    "Did Breadth-first-Search find a solution "
    "to the fox-chicken-grain problem in the time allowed?"
)
q6 = create_multiple_choice_widget(q6text, yesno, yes)
#
#
q7text = "From your understanding of Depth-First Search, what happened when the algorithm ran?"
q7options = [
    "It completed",
    "It got stuck in a loop",
    "It was not allowed enough iterations",
]
q7 = create_multiple_choice_widget(q7text, q7options, 1)
#
#
q8text = (
    "Would allowing depth-first more attempts let it solve the problem?\n"
    "If you're not sure, experiment to find out "
    "by changing the value of max_attempts in the code cell."
)
q8 = create_multiple_choice_widget(q8text, yesno, no)
#
#
q9text = (
    "From you understanding of the depth-first algorithm,"
    "what is the minimum number of moves needed "
    "to solve the fox-chicken-grain problem?"
)
q9options = ["4", "5", "6", "7", "8", "not possible to say"]
q9 = create_multiple_choice_widget(q9text, q9options, 3)
#
#
q10text = (
    "Will imposing a maximum depth on the solution  "
    "make Depth-First Search complete successfully "
    "for *every* problem"
)
q10 = create_multiple_choice_widget(q10text, yesno, no)
##
q11text = (
    "Does the depth of the solution "
    "found by breadth-first match the smallest value that works for your/n"
    "RestrictedDepthFirstSearch() algorithm?"
)
q11 = create_multiple_choice_widget(q11text, yesno, yes)

#
q12text = "Are  more solutions examined  for breadth than depth?"
q12 = create_multiple_choice_widget(q12text, yesno, yes)
#
#
q13text = (
    "The memory used is determined by the maximum size of the openlist \n"
    "at any stage during the search process.\n"
    "Would you expect this to be bigger for depth-first than breadth first search?"
)
q13 = create_multiple_choice_widget(q13text, yesno, no)


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
