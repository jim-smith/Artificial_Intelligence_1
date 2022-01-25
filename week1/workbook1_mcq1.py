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

Q1 = create_multipleChoice_widget('Does it make a difference whether you use upper or lower case?',['yes','no'],'no')
Q2 = create_multipleChoice_widget('Does it make a difference if you have a comma in the middle of your input?',['yes','no'],'yes')
Q3 = create_multipleChoice_widget('Does it make a difference if you put a full stop in the middle of your input?',['yes','no'],'yes')
Q4 = create_multipleChoice_widget('Does it make a difference if you you put a question mark in the middle of your input?',['yes','no'],'yes')
Q5 = create_multipleChoice_widget('Does it make a difference if you have a comma at the end of your input?',['yes','no'],'no')
Q6 = create_multipleChoice_widget('Does it make a difference if you put a full stop at the end of your input?',['yes','no'],'no')
Q7 = create_multipleChoice_widget('Does it make a difference if you you put a question mark at the end of your input?',['yes','no'],'no')
Q8 = create_multipleChoice_widget('What happens if you enclose some of your input in quotation marks?',['it makes no difference', 'it passes all the input to the chatbot','it still splits the input'],'it still splits the input')
Q9 =  create_multipleChoice_widget('What happens to contractions such as what\'s your name?',['the input is split  at the apostrophe','the apostrophe is removed', 'they are expanded into two words'],'they are expanded into two words')