import ipywidgets as widgets
import sys
from IPython.display import display
from IPython.display import clear_output
from IPython.display import HTML

import numpy as np
import matplotlib.pyplot as plt


def showPerceptron( w1,w2,bias,func): 
    in1 = np.linspace(-5,5,100)
    if (abs(w2) < 0.001):
        y=np.zeros(100)
    else:
        y = -(bias/w2)  - in1*(w1/w2)
    plt.plot(in1, y, '-r',label="Decision Boundary")
        # plot sample functions
    if(func != ''):
        plt.plot(0,0,'or')
        if(func=='AND'):
            m01 = m10 = 'or'
        else:
            m01=m10='og'
        if(func=='XOR'):
            m11 = 'or'
        else:
            m11 = 'og'
        plt.plot(0,1,m01)
        plt.plot(1,0,m10)
        plt.plot(1,1,m11)
    
    plt.title('Graph of Perceptron decision Boundary')
    plt.xlabel('input1', color='#1C2833')
    plt.ylabel('input2', color='#1C2833')

    plt.xlim(-1.0,2.0)
    plt.ylim(-1.0,2.0)
    plt.legend(loc='upper left')
    plt.grid()




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


Q1 = create_multipleChoice_widget('If Input1 is 0, and Input2 is 1, and the perceptron makes an error, which weight will NOT be changed?',
                                  ['biasweight', 'weight1', 'weight2'], 'weight1')

Q2 = create_multipleChoice_widget('If  the perceptron makes an error, which weight will always be changed?',
                                  ['biasweight', 'weight1', 'weight2'], 'biasweight')


Q3 = create_multipleChoice_widget(    'If Input1 is 0, and Input2 is 1, and the perceptron outputs the right value, will any weights be changed?',
    ['yes', 'no'], 'no')


Q4 = create_multipleChoice_widget('If Input1 is 1,  and the perceptron outputs 1 when it should output 0, what is the change to weight1?',
                                  ['it is increased', 'it is decreased'], 'it is decreased')


Q5 = create_multipleChoice_widget('If Input1 is 1,  and the perceptron outputs 0 when it should output 1, what is the change to weight1?',
                                  ['it is increased', 'it is decreased'], 'it is increased')

Q6 = create_multipleChoice_widget(    'Is there only one set of weights that would output the right predictions for the OR problem?',
    ['yes', 'no'], 'no')

Q7 = create_multipleChoice_widget('if a perceptron has learned to correctly predict responses for the OR problem, which one weight can we adjust to make it correctly predict the AND problem?',['biasweight', 'weight1', 'weight2'], 'biasweight')

mcqlist = [Q1,Q2,Q3,Q4,Q5,Q6,Q7]

def check_mcq(id:widgets.VBox)->int:
    if len (id.children)>=4 and len(id.children[3].outputs)>0:
        if 'Correct' in id.children[3].outputs[0]['text']:
            return 1
        else:
            return 0
    else:
        return -1 #not answered
    
    
def test_mcqs():
    mcqs= [Q1,Q2,Q3,Q4,Q5,Q6,Q7]
    correct = 0
    for q in range(len(mcqs)):
        res= check_mcq(mcqs[q])
        errmsg= "no answer submitted" if res== -1 else "incorrect answer"
        try:
            assert res==1, errmsg
            print (f' question {q}: answered correctly')
            correct += 1
        except AssertionError:
            print (f' question {q}: {errmsg}')
    print(f' Total: {correct} out of {len(mcqs)} questions answered correctly\n')