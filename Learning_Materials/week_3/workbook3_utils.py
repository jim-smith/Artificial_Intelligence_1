import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

# from candidatesolution import CandidateSolution
from IPython.display import clear_output
from matplotlib import cm

# from matplotlib.ticker import FormatStrFormatter, LinearLocator
# from maze import Maze
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# ======================================================
def make_different_landscapes_plot():
    """Makes illustrative plot of 2 landscapes
    created from the same underlying function
    but plotted (i.e. quality function) at different levels of precision.
    """

    # Make data.
    x = np.arange(-5, 5, 0.01)
    y = np.arange(-5, 5, 0.01)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x**2 + x**2)
    z1 = np.round(np.sin(r) * 2, 0)
    z2 = np.round(np.sin(r) * 2, 1)
    # Plot the surfaces.
    # z1 (left) only has integer parts
    # z2 (right) has one decimal place
    fig = plt.figure(figsize=(16, 12))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    fig.suptitle(
        "Example search landscape with different precision for quality function"
    )
    ax1.set_title("Integer ")
    ax2.set_title("float with one decimal place ")
    _ = ax1.plot_surface(x, y, z1, cmap=cm.jet, antialiased=True)
    _ = ax2.plot_surface(x, y, z2, cmap=cm.jet, antialiased=True)
    plt.tight_layout()
    plt.savefig("figures/2landscapes.png")


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
