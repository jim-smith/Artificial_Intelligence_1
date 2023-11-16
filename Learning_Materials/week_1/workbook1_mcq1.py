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

Q1 = create_multipleChoice_widget('Q1: If there are four digits each from {0,1,...,9}, how many attempts will your algorithm try ON AVERAGE',['1','4','9','1000','5000','10000'],'5000')
Q2 = create_multipleChoice_widget('Q2:If there are four digits each from {0,1,...,9}, how many attempts will your algorithm try IN THE BEST CASE',['1','4','9','1000','5000','10000'],'1')
Q3 = create_multipleChoice_widget('Q3: If there are four digits each from {0,1,...,9}, how many attempts will your algorithm try IN THE WORST CASE',['1','4','9','1000','5000','10000'],'10000')

Q4 = create_multipleChoice_widget('Q4: If there are four digits each from {0,1,...,4}, how many attempts will your algorithm try ON AVERAGE',['1','5','100','500','312.5','625','1000'],'312.5')
Q5 = create_multipleChoice_widget('Q5: If there are five digits each from {0,1,...,9}, how many attempts will your algorithm try ON AVERAGE',['1000','5000','10000','50000'],'50000')
Q6 = create_multipleChoice_widget('Q6: If there are four digits each from {0,1,...,20}, how many attempts will your algorithm try ON AVERAGE',['1000','5000','10000','80000'],'80000')

Q7 = create_multipleChoice_widget('Q7:As you increase their values, which parameter makes the number of possible answers grow fastest',["don't know",'the number of digits','the number of options for each digit'],'the number of options for each digit')

def check_submitted_answers(answer_dict):
    global answer1,answer2,answer3,answer4,answer5,answer6,answer7
    try:
        assert answer_dict['Q1'] == 5000, "numerical value wrong"
        assert answer_dict['Q2'] == 1 , "numerical value wrong"
        assert answer_dict['Q3'] == 10000, "numerical value wrong"
        assert answer_dict['Q4'] == 312.5, "numerical value wrong"
        assert answer_dict['Q5'] == 50000, "numerical value wrong"
        assert answer_dict['Q6'] == 80000, "numerical value wrong"
        assert answer_dict['Q7'] == "the number of options for each digit","Did you get the spelling and spacing right?"
        print('These answers are all correctly stored and ready to submit')
    except AssertionError:
        print('some of these answers are not correct')