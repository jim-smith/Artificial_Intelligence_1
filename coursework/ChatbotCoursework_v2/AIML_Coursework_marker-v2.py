#!/usr/bin/env python
# coding: utf-8

# # AIML Coursework marker
# 
# <div class="alert alert-block alert-danger"> <b>REMEMBER:</b> You need to make sure you are running this code within the virtual environment you created using 'AIenv'.<br> In Jupyter click on the kernel menu then change-kernel. In VSCode use the kernel selector in the top-right hand corner </div>
# 
# 
# # Run the next code cell to do some imports

# In[ ]:


import re
import aiml
import random
import sys
from os.path import exists

def preprocessSingleInput(bot,theInput):
    # run the input through the 'normal' subber- only wortks for a single sentence
    subbed1 = bot._subbers['normal'].sub(theInput).upper()
    subbed2 = re.sub(bot._brain._puncStripRE, " ", subbed1)
    return(subbed2)


def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
    


# 
# # Next cell sets up variables and checks your file exists
# - You can change the amount of debugging information printed to screen by setting debug=True
# - you can change the name of your input file to something other than "student.aiml" if you want.
# - **Dont change anything else**

# In[ ]:


debug = False
debug2 = False
theAIMLfile = 'student.aiml'




if not exists(theAIMLfile):
        print(f"====> ERROR - there is no file in this directory " 
              f"with the name {theAIMLfile} as set in the second code cell.\n"
             "=====> Fix this problem before you continue.\n"
             )


# # Run the next three cells to set up the questions
# ## make sure that they report they have not found errors

# In[ ]:


try:
    responsesFileName = theAIMLfile[:-5] +"-responses.txt"
    feedbackFileName = theAIMLfile[:-5] +"-feedback.txt"
except NameError as err:
    print('ERROR: Got error {} - that suggests you have not run the cell above?\n')


# In[ ]:


theQuestionsFileName = "coursework-questions-and-responses-v2.txt"
if not exists (theQuestionsFileName):
    print(f'ERROR: the question file called {theQuestionsFileName} is missing from this directory.\n'
           'You need to fix this problem before you can continue.\n'
         )
NUMQS =45
NUMCONTEXTQS=3
contextQuestions = [35,42,44]


# In[ ]:


#declare arrays to hold the questions and answers
questions = []
responses = []
thisQ = 0

#read the questions
if exists (theQuestionsFileName):
    # read the questions and answers in
    # Using readline() 
    qFile = open(theQuestionsFileName, 'r') 


    while True: 
        # Get next line from file 
        line = qFile.readline() 
        if not line: 
            print("unexpected end of file")
            break
        # should be a question
        elif (line[0] != 'Q' ):
            print("didn't get expected question marker Q")
            break;
        elif ( int(line[1:3]) != thisQ):
            print("question had wrong number")
            break
        else:
            questions.append( line[5:-1])
            if(debug2):
                print("question {} is: {}".format(thisQ,questions[thisQ]))        

        line = qFile.readline() # next line should be the corresponding answer
        if not line: 
            print("unexpected end of file")
            break
        elif (line[0] != 'A' ):
            print("didn't get expected answer marker A")
            break;
        elif ( int(line[1:3]) != thisQ):
            print("answer had wrong number")
            break
        else:
            responses.append(line[5:-1])
            if(debug2):
                print("response {} is: {}".format(thisQ,responses[thisQ]))

        thisQ += 1
        # then read the empty line separating QnA paits
        line = qFile.readline()

        # if line is empty 
        # end of file is reached 
        if not line: 
            break
        if(debug2):
            print("")

    qFile.close() 

#make a shuffled order to ask them in
if (thisQ>0):

    # shuffle the order of the questions except the **three** context-dependent ones
    CQ1 = contextQuestions[0]
    CQ2 = contextQuestions[1]
    CQ3 = contextQuestions[2]
    toremove= [(CQ1 - 1),CQ1,(CQ2 - 1),CQ2,(CQ3 - 1),CQ3]
    #print(toremove)
    # make a shuffled list with the numbers 1...NUMQs except the ones above in
    order = []
    for i in range (NUMQS):
        if i not in toremove:
            order.append(i)
    random.shuffle(order)

    #put the context dependent Qs and precursors back in
    order.insert(10,(CQ1 -1))
    order.insert(11,CQ1)
    order.insert(20,(CQ2-1))
    order.insert(21,CQ2)
    order.insert(30, (CQ3-1))
    order.insert(31,CQ3)
    #print(order)
    #print ( len(order))
    for i in range (NUMQS):
        if i not in order:
            print("{} is missing".format(i))

# check that there are the right number
if (thisQ <NUMQS ):
    print("ERROR, only {} question-answer pairs read".format(thisQ))
elif (len(questions) < NUMQS or len(responses)<NUMQS):
    print("ERROR, somehow the questions or responses have not all be saved")
    if(debug):
        print(" {} questions and {}responses read, thisQ = {}".format(len(questions),len(responses),thisQ))
else: 
    print('{} question-response pairs read for testing your bot'.format(thisQ))


# # Run the next cell to  create the chatbot

# In[ ]:


# Create Chatbot and read the candidate AIML file
checkBot = aiml.Kernel()
checkBot.verbose(True)


# ##  Now run this cell to  clear any old categories, and  load your AIML file
# ### If you have edited your .aiml file, you can restart from here 
# ### rather than restarting the kernel  and re-running the whole notebook

# In[ ]:




if exists(theAIMLfile):
    checkBot.resetBrain()
    checkBot.learn(theAIMLfile)

    load_failed=False
    # How many categories were correctly read
    numCategories = checkBot.numCategories()
    print( "After reading your file the bot has {} categories".format(numCategories))

    if(numCategories==0):
        load_failed=True
        with open(feedbackFileName,'w') as feedback_file:
            feedback_file.write('<SCORE>0</SCORE>\n')

            feedback = ("<MESSAGE>" 
                        "The chatbot could not load your .aiml file.\n"
                        "To debug, run it through the notebook provided.\n"
                        "That will report the line and character number of the error."
                        "</MESSAGE>\n"
                       )
            feedback_file.write(feedback)
        if not isnotebook():
            sys.exit()
        else:
            print("====> Do not continue - your aiml has failed to load.\n"
                 "=====> Fix this problem before you continue.\n"
                 "=====> The error message contains the line number "
                  " and the character within that line,   of the problem.\n")

    else:
        print( "Remember that the bot will overwrite categories with the same pattern, that and topic. "
               "This number should help you fix misformed categories if needed\n"
             )
else:
    print("ERROR: the system cannot find your aiml file.\n"
          "Check the cells above to make sure you have specified it")


# # Run the next four code cells to test your aiml

# In[ ]:


### See how frequently different language constructs have been used
studentlines  = []
if exists (theAIMLfile):
    ## open the student.aiml file and read it line by line looking for <srai> <set> <star/> and <that>
    file2 = open(theAIMLfile,'r')
    srai_count = 0
    set_count = 0
    wildcard_count=0
    starslash_count=0
    that_count = 0
    condition_count= 0


    #read through line by line counting use of AIML constructs
    while(True):
        line = file2.readline()
        if not line:
            break
        if "<srai" in line:
            srai_count += 1
        if "<set" in line: # just use start - they ar hopefullty defining a name for their variable
            set_count += 1
        if ("*" in line) or ("_" in line) or ("^" in line) or ("#" in line):
            wildcard_count +=1
        if "<star" in line: #just look for start of tag in case they used indexing
            starslash_count += 1
        if "<that" in line: #just look for start of tag in case they used indexing
            that_count +=1
        if "<condition" in line: #just look for start of tag in case they used indexing
            condition_count +=1
        studentlines.append( line)
    file2.close()       
        
else:
    print("ERROR: the system cannot find your aiml file.\n"
          "Check the cells above to make sure you have specified it")


# In[ ]:


### See if users have duplicated information
if len(studentlines)>0:
    repeats = [0]*NUMQS
    numlines = len(studentlines)
    for q in range(NUMQS):
        answer = responses[q]
        for theline in range(numlines):
            if answer in studentlines[theline]:
                repeats[q] = repeats[q]+1
    #print(repeats)

    unnecessary_duplicates = False
    contextQuestions = [35,42,44]
    otherDuplicates = [11,28]
    for i in range(NUMQS):
        if repeats[i]==0:
            pass #print(f' answer --{responses[i]}-- is not present')
        elif repeats[i]==1:
            pass
        elif i+1 in contextQuestions or i in otherDuplicates:
            pass
        else:
            unnecessary_duplicates = True
        
else:
    print("ERROR: could not continue becuase the system could not read your aiml")
    unnecessary_duplicates = False


# In[ ]:



### Ask the questions, check and store the responses

# initialise score
numCorrect = 0
numContextQsCorrect=0
numNoMatch=0
responsesFile = open(responsesFileName,'w')

for q in range (NUMQS):
    thisQ = order[q]
    #get bot's response to question
    botResponse = checkBot.respond(questions[thisQ])
    if(botResponse==""):
        numNoMatch +=1
    responsesFile.write('Q{:2d}: {}\n'.format(thisQ, questions[thisQ]))
    responsesFile.write('Expected response: {}\n'.format(responses[thisQ]))
    responsesFile.write('Your bot response: {}\n'.format(botResponse))
    # check if it matches the required input
    if botResponse == responses[thisQ] :
        #print('question {} answered correctly'.format(thisQ))
        responsesFile.write('*** Question answered correctly\n\n')
        numCorrect +=1
        if thisQ in contextQuestions:
            numContextQsCorrect +=1
    else:
        responsesFile.write('Question answered incorrectly\n\n')
        if(debug):
            theInput = questions[thisQ]
            print('Q{} {}\n gets preprocessed as:{}'.format(thisQ,theInput,preprocessSingleInput(checkBot,theInput)))
            print(' expected :' +responses[thisQ])
            print(' got      :' +botResponse)
            lastThat = checkBot.getPredicate("_outputHistory")

# write final line to log file and exit
responsesFile.write(' In total you got {} questions correct'.format(numCorrect))
responsesFile.close()


# In[ ]:


### Calculate final score and feedback
if not load_failed:

    feedbackFile = open(feedbackFileName,'w')


    # calculate final score
    finalScore= numCorrect 
    # if all questions correct then we start rewarding go solutions
    if (numCorrect==NUMQS):
        if (numCategories <10):
            finalScore = 100
        else:
            finalScore = 90 - numCategories
        if unnecessary_duplicates==True:
            finalScore = min (finalScore,65)

    # provide output for DEWIS
    feedbackFile.write('<SCORE>{}</SCORE>\n'.format(finalScore))

    fstart=  "<MESSAGE>"
    fend = "</MESSAGE>\n"

    feedback = fstart + "After removing repeated categories, your bot used " + str(numCategories) + " categories" +fend
    feedbackFile.write(feedback)

    # what did the submission get wrong and why?
    if(numCorrect< NUMQS):
        feedback = fstart+ "Your bot answered one or more questions incorrectly." +fend 
        feedbackFile.write(feedback)
        feedback = fstart + "File " + responsesFileName + " has more details of your bots responses." +fend
        feedbackFile.write(feedback)
        feedback = fstart + "Common mistakes are typos or extra spaces" +fend
        feedbackFile.write(feedback)

        if(numNoMatch>0):
            feedback = fstart + "For " + str(numNoMatch) +" questions your bot did not have a matching category." +fend
            feedbackFile.write(feedback)
        contextErrors = NUMCONTEXTQS - numContextQsCorrect
        if( contextErrors >0 ):
            feedback= fstart +"Your bot answered incorrectly for " + str(contextErrors) + " questions that require a sense of context." +fend
            feedbackFile.write(feedback)

    else: #
        feedback = fstart +"Your bot answered every question correctly using " + str(numCategories) + " categories" +fend
        feedbackFile.write(feedback)
        if ( srai_count==0  or wildcard_count ==0 or starslash_count==0):
            feedback = fstart+ "You can improve your score by generalising using srai and wildcards." + fend
            feedbackFile.write(feedback)
        if (set_count==0 or that_count==0):
            feedback = fstart + "You can improve your score by remembering context and what the conversation is talking about." +fend
            feedbackFile.write(feedback)
        if(condition_count==0):
            feedback = fstart + "You can use <condition> to change behaviour within a category." +fend
            feedbackFile.write(feedback)

        if unnecessary_duplicates==True:
            feedback = fstart + "Your knowledge base duplicated information so you mark is restricted to a maximum of 65." +fend
            feedbackFile.write(feedback)


        if(numCategories ==10):
            feedback = fstart + "Congratulations, you have matched Jim's score!" +fend
            feedbackFile.write(feedback)
            
        if(numCategories <10):
            feedback = fstart + "Congratulations, you have beaten Jim's score!" +fend
            feedbackFile.write(feedback)    


    feedbackFile.close()


# # Run next cell to show your results and feedback

# In[ ]:


if isnotebook():
    print(f'The score is {finalScore}')
    print(f'The feedback is in {feedbackFileName} '
       'and here it is for quick reference:\n')
    with open(feedbackFileName) as f: 
        for line in f:
            print (line)


# # Uncomment the cell below if you want to run your bot interactively

# In[ ]:


# keepgoing= True
# while(keepgoing):
#     nextInput = input("Enter your message >> ")
#     if (nextInput=='bye'):
#         keepgoing= False
#     else:
#         print (checkBot.respond(nextInput))


# In[ ]:


# print (finalScore)

