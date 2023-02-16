import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import plotchecker

from ideal_visualiser import cluster_and_visualise as ideal
from cluster_and_visualise_one_ax import cluster_and_visualise as one_ax
from cluster_and_visualise_onefig import cluster_and_visualise as one_fig
#from student import cluster_and_visualise as student


from err_msg import processError, getExceptionDetails
from typing import Any

def check_fig_type(fig:Any)-> tuple[bool,bool,str] :
    ''' function that checks that variable fig is a matplotlib figure'''

    manual_marking= False
    wrong_types=False
    message = ""

    if  isinstance(fig, matplotlib.figure.Figure):
        message += ("Your code correctly returned first param of type Figure.\n")
        
    #except in rate cases of scatter plotd created directly by plt.scatter
    elif isinstance(fig,matplotlib.collections.PathCollection):
        manual_marking=True
        message += ('Your code returned a first param of type pathcollection, '
                    'which is unusual, and will need manual marking.\n')
    else:
        message = ( "Error, your code does not return the right things.\n"
                    "The first thing returned should be of type matplotlib.figure.Figure, "
                   f"however your code return something of type {type(fig)}.\n"
                  )
        wrong_types = True
    return  manual_marking, wrong_types,message




def check_ax_type(ax:Any,numfeatures=2)-> tuple[bool,bool,bool,str] :
    ''' function that checks that ax variables is either an axes subplot or an array of them'''
    wrong_types=False
    message = ""
    single_ax= False
    manual_marking= False
        
 
    axtype = type(ax)
    
    #simple figure with one plot created using fig.subplots
    if issubclass(axtype, matplotlib.axes.SubplotBase):
        single_ax = True
        message += "You have returned a figure with a single plot in it.\n"

    
    elif isinstance (ax, np.ndarray):
        single_ax = False
        num_dimensions = len(ax.shape)

        # check organisation of array
        message += f'You have returned an array with {num_dimensions} dimensions, of sizes {ax.shape}, '

        if   num_dimensions != 2 or ax.shape[0]!=numfeatures or ax.shape[1] !=numfeatures:
            message += ("but to compare combinations of features pairwise this should normally be "
                         f" a 2-D array of size {numfeatures}X{numfeatures}.\n"
                       )
            message += "this will require manual marking.\n"
            manual_marking = True
        else:
            message += "which is the ideal arrangement.\n"
            
        #check contentys of array
        if len(ax.shape)==1:
            contents_type= type(ax[0])
        else:
            contents_type= type(ax[0][0])                
        if not issubclass(contents_type, matplotlib.axes.SubplotBase):
                message += (f"Your array ax contains things of type {contents_type}."
                        "the standard  call `fig,ax = plt.subplots()` "
                        "makes ax an array with datatype  matplotlib.axes._subplots.AxesSubplot.\n"
                       )
                wrong_types=True
        else:
            message += "Your ax array correctly contains objects of  type AxesSubplot" 
        
    else:
        message += ( "Error, your code does not return the right things.\n"
                    "The second thing returned should either be: \n"
                     " - one thing of type  matplotlib.axes._subplots.AxesSubplot, or \n"
                     " - a numpy.ndarray of things of type matplotlib.axes._subplots.AxesSubplot\n"
                     f"However your code return something of type {type(ax)}"
                  )
        wrong_types = True
      
    return manual_marking, wrong_types,single_ax,message


debug = True
if debug:
    studentName= "j4-smith"

content_score = 0
presentation_score = 0

featurenames= ( 'mean_red', 'mean_green', 'mean_blue','width', 'height', 'weight')
datafile= 'data/fruit_values.csv'
numfeatures= len(featurenames)

typesdict = {"ideal":ideal, "oneax":one_ax, "oneFig":one_fig}

#this tests that the identification of the type of charts works
for name,func in typesdict.items():
    
    print("*****testing.   " + name + " *****\n")

    # start by testing the return types
    fig,ax = func(datafile, 3,featurenames )
    print(f' type of fig  is: {type(fig)}\n  type of ax is {type(ax)}\n\n')
    manual_marking,wrong_types,message = check_fig_type(fig)
    print (f"Checking fig, needs manual_marking= {manual_marking}, "
           f"wrongtype = {wrong_types}\nmessage= {message}\n"
          ) 
    
    if not manual_marking:
        manual_marking2,wrong_types2,single_ax2,message2 = check_ax_type(ax,numfeatures=numfeatures)
        print (f"checking ax, manual_marking= {manual_marking2}, " 
           f"wrongtype = {wrong_types2}, single_ax= {single_ax2}\nmessage= {message2}\n"
          )     
    

#Check chart has a title that contains the user name
fig,ax = ideal(datafile,3,featurenames)




if('_suptitle' in fig.__dict__.keys()):
    has_title = True
    the_Title=fig._suptitle.get_text()
    print(f'the_title= {the_title}')
    if studentName in the_Title:
        name_in_title = True
        message += 'Your figure has your user name in the title'
    else :  
        message += 'Your figure does not contain a label with your user name in as required.\n'
else:
    has_title = False
    message += 'Your figure does not contain a title'
    #TODO if ther is a single qaxius there could be an axis title
    
print(message)
pc = plotchecker.PlotChecker(ax)
#pc.assert_title_exists()
#print(pc.title)

    
    
    
    
    
        
#get marks
        
        

#for key,value in fig.__dict__.items():
#    print(f'{key}:{value}')
    
#print(f'type of ax is {type(ax)} with shape {ax.shape}')

#for row in range (ax.shape[0]):
#    for col in range (ax.shape[1]):
#        print(f'subplot in row {row} col {col}  has '
#              f'x label {ax[row][col].get_xlabel()}, ylabel {ax[row][col].get_ylabel()}'
#        )
        
#for item in ax[0][0].__dict__.items():
#    #print (item)
#    if item[0]=='_children':
#        pathcollection = item[1] 
#        print(f' pathcollection is type {type(pathcollection)} with contents {pathcollection[0].__dict__}')
##print(ax[0][0].__dict__.items()['children'])






##==================================================
##
### This is the main marking function
##
##
# def MarkVisualiser(): 

#     datasets = [ld.load_dataset1(), ld.load_dataset2(), ld.load_dataset3()]

#     setDesc = ("a simple 2-class problem with one predictive variable, all others are zero",
#            "a three class problem defined by values for 2 variables, rest are noise",
#           "a simple 2 class proble, defined by one variable, rest are noise")
#     correctDeltas = np.zeros(len(datasets))
#     knnDeltas = np.zeros(len(datasets))
#     madeInvalid = 0
#     madeNoRules = 0
#     message = ""
#     for setNum in range(len(datasets)):

#         #get data
#         train_X,train_y,test_X,test_y = datasets[setNum]
 
#         #results for correct, knn and s tudent classifiers
#         correctModel = Correct(maxRules=5,increments=100)   
#         currectNumRules, correctTestScore,_ = TestAlgorithmOnDataset (correctModel,train_X,train_y,test_X,test_y,verbose=False)
#         knnModel = KNN(maxRules=5,increments=100) 
#         _, KNNTestScore,_  = TestAlgorithmOnDataset (knnModel,train_X,train_y,test_X,test_y,verbose=False)
    
#         studentModel = Student(maxRules=5,increments=100) 
#         studentNumRules, studentTestScore, studentInvalids = TestAlgorithmOnDataset (studentModel,train_X,train_y,test_X,test_y)
    
#         correctDeltas[setNum] = np.abs(correctTestScore - studentTestScore)
#         knnDeltas[setNum] = np.abs(KNNTestScore - studentTestScore)
    
#         message = message + "On dataset {}, {}, your method got a test accuracy of {}\n".format(setNum,setDesc[setNum],studentTestScore)
#         message = message +"\tThe target for this dataset was {} so on this dataset the difference was {}\n".format(correctTestScore,correctDeltas[setNum])

#         # feedback about their predict() method from testing the student's learned model with my code
#         if(studentNumRules>0):
#             message = message + "\tTesting the set of {} rules learned by your code using a different implementation of predict()\n".format(studentNumRules)
#             studentRuleSet = studentModel.GetRuleSet()
#             corr_ypred = getCorrectPredictionsForStudentRuleSet(studentRuleSet,studentNumRules,correctModel, test_X)
#             st_ypred = studentModel.predict(test_X)
#             if(np.array_equal(st_ypred, corr_ypred)):
#                 message = message + "\tThis gave the same results, indicating that  your predict() method is probably correct.\n"
#             else:
#                  message = message + "\tThis gave a different results indicating that your predict() method is not correct.\n"
#         else:# (studentNumRules==0)
#             madeNoRules += 1
#             message = message + "\tHowever, your algorithm had a value of 0 for self.numRules, and getRuleSet() returned an empty array.\n"
#             message = message + "\tSo we could not test your predict() method for this dataset.\n"

        
#         if(len(studentInvalids)>0):
#             message = message +"\tCrucially, you algorithm predicted labels that were not present in the training set. This should be impossible.\n"
#             madeInvalid +=1
#         message = message + "\n"

 
#     # Finally print summary message and score
#     message = message+"Overall:\n"
#     finalScore = 0
#     if (madeInvalid>0):
#         message = message + "Your algorithm made some invalid predictions, therefore you score 0"
#         finalScore = 0
#     else:
#         wrongAlg = False
#         if(madeNoRules >0 and madeNoRules < len(datasets)):
#             message = message + "Your algorithm made  rules on some datasets but not on {}. ".format(madeNoRules)
#             message = message + "That indicates you are not generating all possible rules- check your loop conditions."
            
#         if(madeNoRules ==len(datasets)):
#             message = message + "Your algorithm made no rules for any datasets."
#             message = message + " This  suggests you have implemented a different algorithm or not used the super class correctly.\n"
#             wrongAlg = True
#         if(np.mean(knnDeltas) < 2):
#             message = message + "The results are very close to what a 1-NN classifier gets. Did you implement this by mistake?\n"

#         meanDiff= np.mean(correctDeltas)
#         maxDiff = np.max(correctDeltas)
#         message = message + "Your algorithm makes valid predictions."
#         if(maxDiff>=10):
#             message = message + " However,  the test accuracy more than 10 percent away from the target on one or more datasets, so you score 20\n"
#             finalScore = 20
#         elif ( meanDiff <10 and meanDiff>5):
#             message = message + "The mean difference to the target test accuracy is between 5 and 10 percent, so you score 40.\n"
#             finalScore=40
#         elif ( (meanDiff <= 5.0)and (meanDiff >2.5) and (maxdiff >= 5)):
#             message = message + "The mean difference to the target accuracy is between 2.5 and 5 percent."
#             message = message + " However, the differnce is greater than 5 for one or more datasets so you score 50.\n"
#             finalScore = 50
#         elif ( (meanDiff <= 5.0)and (meanDiff >2.5) and (maxdiff <5)):
#             message = message + "On average your  test accuracy is between 2.5 and 5 percent away from the target."
#             message = message + " The differnce is less than 5 for all datasets so you score 60.\n"
#             finalScore = 60
#         elif(meanDiff >= 1.0 and meandDiff<2.5):
#             message =message + "On average your  test accuracy is within 1 and 2.5 percent of the target accuracy so you score 70.\n"
#             finalScore = 70
#         elif(meanDiff < 1.0):
#             message = message + "The mean test accuracy is less than 1 percent away from target. You score 100 for this run.\n"
#         finalScore = 100
        
        
#     return finalScore,message       
# #======================