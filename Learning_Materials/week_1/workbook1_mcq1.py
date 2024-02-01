import ipywidgets as widgets
from IPython.display import clear_output


def create_multiple_choice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)

    correct_answer_index = options.index(correct_answer)

    radio_options = [(words, i) for i, words in enumerate(options)]
    the_alternative = widgets.RadioButtons(
        options=radio_options, description="", disabled=False
    )

    description_out = widgets.Output()
    with description_out:
        print(description)

    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(the_alternative.value)
        if a == correct_answer_index:
            s = "\x1b[6;30;42m" + "Correct." + "\x1b[0m" + "\n"  # green color
        else:
            s = "\x1b[5;30;41m" + "Wrong. " + "\x1b[0m" + "\n"  # red color
        with feedback_out:
            clear_output()
            print(s)
        return

    check = widgets.Button(description="check")
    check.on_click(check_selection)

    return widgets.VBox([description_out, the_alternative, check, feedback_out])


text1 = (
    "Q1: If there are four tumblers each taking a value from the set {0,1,...,9}, "
    "how many attempts will your algorithm try ON AVERAGE"
)
Q1 = create_multiple_choice_widget(
    text1,
    ["1", "4", "9", "1000", "5000", "10000"],
    "5000",
)
text2 = (
    "Q2:If there are four tumblers each taking a value from the set {0,1,...,9} "
    "how many attempts will your algorithm try IN THE BEST CASE"
)

Q2 = create_multiple_choice_widget(
    text2,
    ["1", "4", "9", "1000", "5000", "10000"],
    "1",
)
Q3 = create_multiple_choice_widget(
    (
        "Q3: If there are four tumblers each taking a value from the set {0,1,...,9}, "
        "how many attempts will your algorithm try IN THE WORST CASE"
    ),
    ["1", "4", "9", "1000", "5000", "10000"],
    "10000",
)

Q4 = create_multiple_choice_widget(
    (
        "Q4: If there are four tumblers each taking a value from the set {0,1,...,4}, "
        "how many attempts will your algorithm try ON AVERAGE"
    ),
    ["1", "5", "100", "500", "312.5", "625", "1000"],
    "312.5",
)
Q5 = create_multiple_choice_widget(
    (
        "Q5: If there are five tumblers each taking a value from the set {0,1,...,9}, "
        "how many attempts will your algorithm try ON AVERAGE"
    ),
    ["1000", "5000", "10000", "50000"],
    "50000",
)
Q6 = create_multiple_choice_widget(
    (
        "Q6: If there are four tumblers each taking a value from the set {0,1,...,20}, "
        "how many attempts will your algorithm try ON AVERAGE"
    ),
    ["1000", "5000", "10000", "80000"],
    "80000",
)

Q7 = create_multiple_choice_widget(
    (
        "Q7:As you increase their values, "
        "which parameter makes the number of possible answers grow fastest"
    ),
    ["don't know", "the number of tumblers", "the number of options for each tumbler"],
    "the number of tumblers",
)


def check_submitted_answers(answer_dict):
    global answer1, answer2, answer3, answer4, answer5, answer6, answer7
    try:
        assert answer_dict["Q1"] == 5000, "numerical value wrong"
        assert answer_dict["Q2"] == 1, "numerical value wrong"
        assert answer_dict["Q3"] == 10000, "numerical value wrong"
        assert answer_dict["Q4"] == 312.5, "numerical value wrong"
        assert answer_dict["Q5"] == 50000, "numerical value wrong"
        assert answer_dict["Q6"] == 80000, "numerical value wrong"
        assert (
            answer_dict["Q7"] == "the number of tumblers"
        ), "Did you get the spelling and spacing right?"
        print("These answers are all correctly stored and ready to submit")
    except AssertionError:
        print("some of these answers are not correct")
