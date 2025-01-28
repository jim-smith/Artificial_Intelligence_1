
# # Notebook for developing code that marks a simple visualisation
# Jim Smith 2022


import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os.path



from tester.err_msg import processError, getExceptionDetails
#from err_msg import processError, getExceptionDetails
from typing import Any


# # Make data

num = 50
num_f = 4
feature_names= ("randchoice","f2","f1","rand_uniform")
vals = (0.0,0.2,0.4,0.6,0.8)
data = np.zeros((num,num_f),dtype=float)
for i in range (num):
    data[i][2] = (i%2) + 0.5 + np.random.normal(loc=0.25,scale=0.1)
    data[i][1] = np.random.normal(loc=1.0,scale=0.25)
    data[i][0] = vals [np.random.randint(5)]
    data[i][3] = np.random.uniform(0.0,1.0)
np.savetxt('visdata.csv',data,fmt="%.4f",delimiter=',')

perfect_clusters = np.zeros(num,dtype=int)
for i in range(num):
    if i%2:
        perfect_clusters[i] = 1


# # Functions to calculate different checks

def check_fig_type_ok(fig:Any)-> tuple :
    '''  checks that variable fig is a matplotlib figure
    Parameters
    -----------
    fig: the thing being tested
    
    Returns
    --------
    tuple[Bool,str]: is the type correct and what is the feedback
    '''

    
    right_types=False
    message = ""

    if  isinstance(fig, matplotlib.figure.Figure):
        message += ("Your code correctly returned first param of type Figure.\n")
        right_types=True
        
    #except in rare cases of scatter plot created directly by plt.scatter
    elif isinstance(fig,matplotlib.collections.PathCollection):
        message += ('The first thing returned by your code should be a figure, '
                    'but instead it is of type pathcollection. '
                    'This suggests that you called plt.scatter() directly,\n'
                   'instead of making a figure with subplots in it and then'
                   'writing scatter plots onto one of the axes as you were shown.\n'
                   'Please change your code to return fig,ax as specified and resubmit.\n'
                   'You score 0 for this attempt.\n' )
    else:
        message = ( "Error, your code does not return the right things.\n"
                    "The first thing returned should be of type matplotlib.figure.Figure, "
                   f"however your code return something of type {type(fig)}.\n"
                  )
    return   right_types,message




def check_ax_type(ax:Any,numfeatures=2)-> tuple :
    ''' checks that ax variables is either an axes subplot or an array of them
         Parameters:
         -----------
         ax:Any thing to check
         numfeatures: ideal size of matrix 

         Returns
         --------
         tuple [Bool,Bool,str]
             wrong types or count
             just one ax
             feedback
    
    '''
    wrong_count_or_types=False
    message = ""
    single_ax= False
    axtype = type(ax)
    
    #simple figure with one plot created using fig.subplots
    if issubclass(axtype, matplotlib.axes.SubplotBase):
        single_ax = True
        message += ("You have returned a figure with a single plot in it.\n"
                    "This is not enough to fully visualise this dataset.\n"
                   )

    
    elif isinstance (ax, np.ndarray):
        single_ax = False
        num_dimensions = len(ax.shape)

        # check organisation of array
        message += f'You have returned an array with {num_dimensions} dimensions, of sizes {ax.shape}, '

        if   num_dimensions != 2 or ax.shape[0]!=numfeatures or ax.shape[1] !=numfeatures:
            wrong_count_or_types=True
            message += ("but to compare combinations of features pairwise this should normally be "
                         f" a 2-D array of size {numfeatures}X{numfeatures}.\n"
                        "Please check that you have not hard-coded "
                        "the number of features (columns) in the dataset.\n"
                        "The workbook illustrates how to do this is an assumption-free way.\n")
            return wrong_count_or_types,single_ax,message 
        else:
            message += "which is the ideal arrangement.\n"

            
        #get contents of array
        if len(ax.shape)==1:
            contents_type= type(ax[0])
        else:
            contents_type= type(ax[0][0])    
        #check  type
        if  issubclass(contents_type, matplotlib.axes.SubplotBase):
            message += "Your ax array correctly contains objects of  type AxesSubplot.\n" 
        elif issubclass(contents_type, matplotlib.axes._axes.Axes):#later versions of matplot
            message += "Your ax array correctly contains objects of  type Axes.\n" 

        else:
            message += (f"Your array ax contains things of type {contents_type}."
                        "the standard  call `fig,ax = plt.subplots()` "
                        "makes ax an array with datatype  matplotlib.axes._subplots.AxesSubplot.\n"
                       )
            wrong_types=True
 
        
    else:
        message += ( "Error, your code does not return the right things.\n"
                    "The second thing returned should either be: \n"
                     " - one thing of type  matplotlib.axes._subplots.AxesSubplot, or \n"
                     " - a numpy.ndarray of things of type matplotlib.axes._subplots.AxesSubplot\n"
                     f"However your code returns something of type {type(ax)}"
                  )
        wrong_count_or_types = True
      
    return wrong_count_or_types,single_ax,message




def check_substring_in_title(fig:Any,ax:Any,single_ax:bool,substring:str)->tuple:
    title_quality=0
    quality_strings =('Your visualisation does not contain a title.\n',
                      'Your visualisation has a title, but it does not contain the details required.\n',
                      'Your visualisation has the details required in the title.\n'
            )
    the_title= ""
    
    
    if(single_ax):
        #try to get from figure first, 
        try:
            if ( ('_suptitle' not in fig.__dict__.keys()) or
                fig._suptitle is None
               ):
                the_title = fig._suptitle.get_text()
            # then ax if that hasnt worked
            if the_title=="" or the_title==None:
                the_title= ax.get_title()
        except AttributeError:
            title_quality = 0 #missing
            
        if the_title=="" or the_title==None:
            title_quality = 0 #missing
        elif substring in the_title:
            title_quality = 2 #good
        else :  
            title_quality = 1 #inadequate

    
    else:
        if ( ('_suptitle' not in fig.__dict__.keys()) or
            fig._suptitle is None
           ):
            title_quality = 0 #non-existent
        else:    
            the_title=fig._suptitle.get_text()
        
            if substring in the_title:
                title_quality = 2 #good
            else :  
                title_quality = 1 #inadequate

    return title_quality, quality_strings[title_quality]
    

    
def test_clusters (ax:Any, single_ax:bool) -> tuple:
    '''function to test whether the clustering given to an ax matches the ideal version
    parameters ax: either single axessubplot or a ndarray
    parameter single_ax: tells type of ax

    Returns
    ---------
    cluster quality :int
    feedback: str
    '''
    message = ""
    cluster_quality = 0 #non-existent

    #get all the things in an axis
    if (single_ax):
        A = getattr(ax._children[0],"_A","missing")
    else:
        A = getattr(ax[2,0]._children[0], "_A","missing")
    
    # artists were not present
    if ( isinstance(A,str) and A=="missing") or (type(A) ==type(None)):
        cluster_quality = 0 #non-existent 
        message = "Your plot does not appear to have any different colors for the markers.\n"
        
    elif( np.all(A == A[0])):
        cluster_quality = 0 #non-existent 
        message = "Your plot is given a set of colours to use, but they are all the same.\n"
    else:
        A = A.astype(int)
        if len(A) != len(perfect_clusters):
            message+=(f"Your plot contains {len(A)} points "
                     f"but the data contains {len(perfect_clusters)}\n"
                     " This is an error\n")
        else:
            #allow for cluster with inverse assignments
            neg_A = np.ones(len(A),dtype=int) - A
            if np.array_equal(A,perfect_clusters) or np.array_equal(neg_A, perfect_clusters):
                cluster_quality = 2 #perfect
                message += "Your plot colours match the ideal clustering for this data.\n"
            else:
                cluster_quality = 1 #present but not very good
                message += ("Your plot has different colours, "
                           "but they do not match the  clustering "
                           "this dataset was designed to contain.\n"
                          )
    return cluster_quality,message   



def check_axis_labels (ax:Any, single_ax:bool,feature_names) -> tuple:
    '''function to test whether there are axis labels
    parameters ax: either single axessubplot or a ndarray
    parameter single_ax: tells type of ax
    '''
    message = ""
    label_quality = 0 #non-existent
    
    if (single_ax):
        x_label = ax.get_xlabel()
        y_label=ax.get_ylabel()
        
        if x_label==None or x_label=="" or y_label==None or y_label=="" :
            label_quality=0
            message = "One or more axis labels are missing.\n"
            
        elif x_label in feature_names and y_label in feature_names :
            if x_label != y_label:
                label_quality=2
                message = "Axis labels show different valid feature names.\n"
            else:
                label_quality=1
                message= "Both Axis Labels are the same.\n"
        else:
            label_quality=0
            message = "One or both axis labels are not valid feature names.\n"
            
        
    else:
        names_used = {}
        for name in feature_names:
            names_used[name] = 0
        for row in range(ax.shape[0]):
            for col in range(ax.shape[1]):
                the_ax= ax[row][col]
                x_label = the_ax.get_xlabel()
                y_label=the_ax.get_ylabel() 
                #test values
                if (x_label != ""):
                    if  x_label not in feature_names :
                        label_quality=0
                        message = "One or more axis labels are not valid feature names.\n"
                        break
                    else:
                        #increment usage counters
                        val= names_used[x_label]
                        names_used[x_label] = val+1
                if(y_label != ""):
                    if  y_label not in feature_names:
                        label_quality=0
                        message = "One or more axis labels are not valid feature names.\n"
                        break
                    else:
                        val= names_used[y_label]
                        names_used[y_label] = val+1
        
        if testing:
            #for key, val in names_used.items():
            #    print(f'{key}:{val}\n')
            pass
        vals = list(names_used.values())
        
        if all(x==2 for x in vals):
            message= "Each label appears twice, as expected.\n"
            label_quality=3
        elif all(x==len(feature_names) for x in vals):
            message= ( f"Each label appears {len(feature_names)} times " 
                      " which is a little cluttered, but ok.\n"
                    )
            label_quality=2
        else:
            label_quality=1
            message = "All the axis labels provided are valid feature names.\n" 
            if any (x==0 for x in vals):
                message += ("However, some feature names do not appear as axis labels\n")
            else:
                message += ("However, the number of times each appears is unusual.\n")
            
            
    return label_quality,message   



def check_visualisation(func:Any,datafile:str,K:int,feature_names:Any,student_name:str= "j4-smith",testname:str="")->tuple:
    ''' Function that runs various tests on a visualisation 
    Parameters: func provided by student's code, student name, testname
    Returns: Score and message
    '''
    
    content_score = 0
    presentation_score = 0
    total_score=0
    done_marking = False
   
    title_quality= 0
    label_quality =0
    cluster_quality =0
    message = ""
    
    print('about to run your code')
    #EARLY EXIT if student's code won't run
    try:
        returned= func(datafile, K,feature_names )
        if len(returned)==2:
            fig,ax=returned[0], returned[1]
        else:
            return 0, "Your function runs but does not return two objects as required"

    except Exception as e:
        #print(str(e))
        message = f"your code failed to run and produced this error message:\n "
        message += processError(e,func=func)
        message += "So you score 0 for this attempt.\n"
        message += ("A common error is that people forget to return "
                    "both fig and ax from their function.\n"
                    "Otherwise trace through the  message printed above"
                    "to find the line in your code that is producing the error"
                   )
        return total_score, message
    
    #EARLY EXIT if  figure file has not been produced 
    if not os.path.isfile('myVisualisation.png') and  not os.path.isfile('myVisualisation.jpg'):
        message = "Your code ran but failed to create a file called either myVisualisation.png."
        message +="or myVisualisation.jpg.\nTherefore you score 0 for this attempt.\n"
        return total_score, message
    else:
        message = "Your code ran and made a file called myVisualisation with a .jpg or .png extension.\n"
        

    #EARLY EXIT  if  figure has incorrect return type
    # start by testing the return types
    right_types,message1 = check_fig_type_ok(fig)
    message += message1
    if  not right_types:
        return total_score, message   
      
    #EARLY EXIT if ax has wrong count or types
    wrong_count_or_types,single_ax,message2 = check_ax_type(ax,numfeatures=len(feature_names))
    message = message + message2
    if  wrong_count_or_types:
        return total_score, message             

  

    #ok to proceed with the checking the content ...
    #are the diagonals on a matrix histograms?
    diagonal_quality = 0
    if not single_ax:
        #print(ax.shape)
        try:
            if isinstance(ax[0][0]._children[0],matplotlib.patches.Rectangle):
                diagonal_quality = 1
                #get colours
                colours= [p.get_facecolor() for p in ax[0][0]._children]
                num_colours = len( set(colours))
                message += (
                    f'there are {num_colours} '
                    'different coloured bars in your histograms,'
                    )
                if num_colours==K :
                    diagonal_quality =2
                    message += " which matches K.\n"
                else:
                    message +=f" but there should be {K}.\n" 
        except IndexError:
            message += ("Your figure has empty plots on the diagonal,"
                        " which means it is not showing the distribution of values "
                        " for each variable taken on its own.\n"
                       )
                  
    #is there clustering 0 (none),1,2
    cluster_quality,message5= test_clusters (ax, single_ax)
    message +=message5
    
    #does the plot have the right number of points plotted in it?
    right_count=False if "but the data contains" in message5 else True
     
    
    #is there a correct title? 0,1,2
    title_quality,message3 = check_substring_in_title(fig,ax,single_ax,f' {K} ')
    message += message3
    
    #is correct data in the clusters 0,1,2
    #not currently implemented
    
    #are there axis labels? 0,1,2,3
    label_quality, message4 = check_axis_labels (ax, single_ax,feature_names) 
    message += message4
    
    
    #Calculate Marks
    message += "\n\n\n=== Overall: \n"
    #content mark
    if(single_ax):
        message += "You score 5/20 for the basic content having just one plot,\n"
        content_score = 5
        if right_count:
            content_score += 5
            message += "and 5/20 for plotting the right number of points.\n"
            message +=f"and {10*cluster_quality}/20 for the quality of your clustering.\n"
            content_score += 10*cluster_quality 
        else:
            message +="You plotted the wrong number of points we could not check the clustering.\n"
    else:
        message += "You score 10/20 for the basic content having an array of plots\n"
        content_score = 10
        if right_count:
            message += "and 10/20 for plotting the right number of points.\n"
            content_score += 10
            message +=f"and {10*cluster_quality}/20 for the quality of your clustering.\n"
            content_score += 10*cluster_quality 
            if(diagonal_quality>0):   
                message +="      and an extra 5 for having different plots on the diagonals\n"
                content_score += 5*diagonal_quality
            if (diagonal_quality ==2):
                message +="      and an extra five for showing the histogram for each class in a different colour.\n"
                
        else:
            message +="You plotted the wrong number of points we could not check the clustering.\n"             
    message +=f"Altogether, you score {content_score}/50 for the contents of your visualisation.\n\n"

       
    #presentation mark
    if(label_quality==0 and title_quality==0):
        presentation_score = 10
        message +="You do not have a title or labels so you score 10 for presentation"
    else:
        message+=f"You score {10*label_quality}/30 for the quality of your labelling,\n"
        message+=f"      and {10*title_quality}/20 for how well your title met the specs..\n"
        presentation_score= 10 * (label_quality + title_quality)
    message += f"Altogether, you score {presentation_score}/50 for presentation of  your visualisation.\n\n"
    
    message+=f"\nIn total you score {content_score+presentation_score}/100.\n"

    total_score= content_score+presentation_score
    return total_score, message
        
testing = False

def mark_visualisation(student_name):
    datafile= 'visdata.csv'
    K=2
    func= student
    score=0
    message = ""
    
    try:
        score, message= check_visualisation(func,datafile,K,feature_names,student_name)
    except Exception as e:
        message= processError(e, func=student) 
        
        
    return score, message
   



