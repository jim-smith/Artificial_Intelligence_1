import ipywidgets as widgets
import sys
from IPython.display import display
from IPython.display import clear_output
from IPython.display import HTML


def create_multipleChoice_widgetNEW(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)

    correct_answer_index = options.index(correct_answer)

    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        options=radio_options,
        description='',
        disabled=False,
        indent=False,
        align='center',
    )

    description_out = widgets.Output(layout=widgets.Layout(width='auto'))

    with description_out:
        print(description)

    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if a == correct_answer_index:
            s = '\x1b[6;30;42m' + "correct" + '\x1b[0m' + "\n"
        else:
            s = '\x1b[5;30;41m' + "try again" + '\x1b[0m' + "\n"
        with feedback_out:
            feedback_out.clear_output()
            print(s)
        return

    check = widgets.Button(description="check")
    check.on_click(check_selection)

    return widgets.VBox([description_out,
                         alternativ,
                         widgets.HBox([check]), feedback_out],
                        layout=widgets.Layout(display='flex',
                                              flex_flow='column',
                                              align_items='stretch',
                                              width='auto'))


def create_multipleChoice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)

    correct_answer_index = options.index(correct_answer)

    style = {'description_width': 'initial'}
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        style=style,
        options=radio_options,
        description='',
        disabled=False
    )

    description_out = widgets.Output()
    with description_out:
        print(description)

    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if a == correct_answer_index:
            s = '\x1b[6;30;42m' + "Correct." + '\x1b[0m' + "\n"  # green color
        else:
            s = '\x1b[5;30;41m' + "Wrong. " + '\x1b[0m' + "\n"  # red color
        with feedback_out:
            clear_output()
            print(s)
        return

    check = widgets.Button(description="submit")
    check.on_click(check_selection)

    return widgets.VBox([description_out, alternativ, check, feedback_out])


Q1 = create_multipleChoice_widget('How many clusters do the botanists think you might find in the data?',
                                  ['1', '2', '3', '4', '5', '6'], '3')

Q2 = create_multipleChoice_widget(
    'What symbol do you use to specify the marker type so that data in a scatter plot is displayed as upside-down triangles ?',
    ['.', 's', 'v', '^', 'x', '+'], 'v')

Q3 = create_multipleChoice_widget('How tall is the figure created by the call: fig,ax=plt.subplots(figsize=(10, 5))?',
                                  ['10 inches', '5 inches', '10 cm', '5 cm'], '5 inches')
Q4 = create_multipleChoice_widget('How wide is that figure if the next line of code is: fig,ax=plt.subplots(figsize=(5, 10))',
                                  ['10 inches', '5 inches', '10 cm', '5 cm'], '5 inches')

Q5 = create_multipleChoice_widget(
    'What is the effect on KMeans if one feature has much larger range of values than the others?',
    ['None', 'That feature dominates the clustering', 'That feature is ignored'],
    'That feature dominates the clustering')

Q6 = create_multipleChoice_widget('What is  effect does the MinMaxScale() have on each feature (column)',
                                  ['None', 'It scales it evenly to the range [0,1]',
                                   'It compresses high and low values', 'It changes it to mean 0 and std. deviation 1',
                                   'It scales the data to the range [-1,1]'], 'It scales it evenly to the range [0,1]')

Q7 = create_multipleChoice_widget('What is the effect on kMeans clustering of the noisy features?',
                                  ['none', 'unstable'], 'unstable')
Q8 = create_multipleChoice_widget(
    'What do you predict would happen if each value had been measured using a \"noisy\" sensor i.e. a random value from the range [-0.2,0.2] was added to each value in X',
    ['Results stay broadly the same', 'can distinguish one class but not the two others',
     'unable to reliably identify distinct clusters'], 'can distinguish one class but not the two others')
Q9 = create_multipleChoice_widget(
    'Which combonation showed the least distinction between classes? ',
    ['0,1','3,1','2,0','3,2'], '0,1')
Q10 = create_multipleChoice_widget(
    'What number of classes makes the data make most sense? ',
    ['5','4','3','2'], '2')
