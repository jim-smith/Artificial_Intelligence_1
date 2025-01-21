""" Test.py
tests for workbook 8
- reliability pltos for mLP on XOR
- workflow for kNN/DT,MLP on a. dataset
"""


from matplotlib import pyplot as plt
import numpy as np


def test_make_xor_reliability_plot(myfig,myaxs)->(int,str):
    """ test function for the method that assess impact of hidden layer width on learning"""
    
    score=0
    feedback="Feedback [marks earned]\n"
    ok = True
    ### right returned values
    if not isinstance(myfig,plt.Figure):
        ok=False
        feedback += "Failed to return a figure object as the first value.\n"
    if not isinstance(myaxs,np.ndarray):
        ok=False
        feedback +="failed to return an array as the second value.\n"
    if ok and  myaxs.shape[0] !=2:
        ok=False
        " second thing returned did not contain two objects.\n"
    for idx in [0,1]:
        if ok and not isinstance(myaxs[idx],plt.Axes):
            ok=False
            feedback += " object returned in array is not a pyplot axes.\n"
    if not ok:
        return 0, feedback
        
    #check titles etc - 10 marks
    if myaxs[0].get_title() == "Reliability":
        score += 2
        feedback += "Correct title for left hand plot [2].\n"
    else:
        feedback += "Missing or incorrect title for left hand plot.\n"
        
    if myaxs[1].get_title() == "Efficiency":
        score += 2
        feedback += "Correct title for right hand plot [2].\n"
    else:
        feedback += "Missing or incorrect title for right hand plot.\n"

    if myaxs[0].get_xlabel() == "Hidden Layer Width":
        score +=1
        feedback += "Correct x-axis label for left hand plot [1].\n"
    else:
        feedback += "Missing or incorrect x-axis label for left hand plot.\n"

    if myaxs[1].get_xlabel() == "Hidden Layer Width":
        score +=1
        feedback += "Correct x-axis label for right hand plot [1].\n"
    else:
        feedback += "Missing or incorrect x-axis label for right hand plot.\n"
        
        
    if myaxs[0].get_ylabel() == "Success Rate":
        score +=2
        feedback += "Correct y-axis label for left hand plot [2].\n"
    else:
        feedback += "Missing or incorrect y-axis label for left hand plot.\n"

    if myaxs[1].get_ylabel() == "Mean Epochs":
        score +=2    
        feedback += "Correct y-axis label for right hand plot [2].\n"
    else:
        feedback += "Missing or incorrect y-axis label for right hand plot.\n"
    #now are the lines right?
    correct_x= np.arange(1,11)

    try:
        x,y= myaxs[0].lines[0].get_data()
        feedback += f"For the left-hand plot (Effectiveness)\n"
        if x.shape[0]==10 and np.equal(x, correct_x ).all():
            score +=2
            feedback += "Correct x-axis values for left hand plot [2].\n"
        elif x.shape[0]==11 and np.equal(x[1:], correct_x ).all():
            score +=2
            feedback += "Correct x-axis values for left hand plot [2].\n"
        else:
            feedback += (f" Got the sequence {x} for the x-axis labels (hidden layer widths) "
                         "instead of the expected sequence of 1-10 or 0-10.\n"
                        )
        
        #now the actual results -success rates
        correct_SR = np.array([0,1,2,5,7,9,8,10,9,10],dtype=int)
        if y.shape[0]==10 and np.isclose(y, correct_SR).all():
            score += 3
            feedback += "Correct values for success rates [3].\n"
        elif y.shape[0]==11 and np.equal(y[1:], correct_SR).all():
            score += 3
            feedback += "Correct values for success rates [3].\n"
        else:
            feedback += (f"Got the success rates {y} instead of the expected ones:\n {correct_SR}\n"
                         " did you perhaps not use the value of repetition as the seed for the MLP?\n"
                        )   
            
    except NameError:
        ok=False 
        feedback += "left hand plot does not contain a line as it should.\n"
        
    # now mean solution times
    try:
        x,y= myaxs[1].lines[0].get_data()
        feedback += f"\nFor the right hand plot (Efficiency)\n"
        correct_x= np.arange(1,11)
        if x.shape[0]==10 and np.equal(x, correct_x).all():
            score +=2
            feedback += "Correct x-axis values for right hand plot [2].\n"
        elif x.shape[0]==11 and np.equal(x[1:], correct_x).all():
            score +=2
            feedback += "Correct x-axis values for right hand plot [2].\n"
        else:
            feedback += (f" Got the sequence {x} for the x-axis labels (hidden layer widths) "
                         "instead of the expected sequence of 1-10 or 0-10.\n"
                        )
        
        #now the actual results for mean. times
        correct_times=np.array([1000.0,192.0,281.5, 183.2,214.0, 204.8,  173.1,159.2,170.8,170.6])
        if y.shape[0]==10 and np.isclose(y, correct_times,atol=0.05).all():
            score += 3
            feedback += "Correct values for mean times [3].\n"
        elif y.shape[0]==11 and np.isclose(y[1:], correct_times,atol=0.05).all():
            score += 3
            feedback += "Correct values for mean times[3].\n"
        else:
            feedback += (f"Got the mean times {y} instead of the expected ones:\n {correct_times}]\n"
                         " did you perhaps not use the value of repetition as the seed for the MLP?\n"
                        )    
            
    except NameError:
        ok=False 
        feedback += "right hand plot does not contain a line as it should.\n"        
    return score, feedback 


from approvedimports import *


#dictionaries defining what the requirements said should be in the lists of stored models
names_and_types:dict = { "KNN":KNeighborsClassifier,
                        "DecisionTree":DecisionTreeClassifier,
                        "MLP":MLPClassifier
                       }
combinations_requested:dict = { "KNN":5,
                        "DecisionTree":27,
                        "MLP":18
                       }

#lovely bit of data structure
#for each type of model holds a directory with
# the names of the hyperparameters to change as keys
# how often each should occur as elements of a list
#(number of different value can be inferred from length of list)
hyperparams_and_counts:dict = {
    "KNN":{'n_neighbors':[1,1,1,1,1]},
    "DecisionTree": {'max_depth':[9,9,9],
                         'min_samples_split':[9,9,9],
                         'min_samples_leaf':[9,9,9]
                             },
    "MLP":{'hidden_layer_sizes':[2,2,2,2,2,2,2,2,2],
           'activation':[9,9]}
}
hyperparams_and_vals:dict = {
    "KNN":{'n_neighbors':['1','3','5','7','9']},
    "DecisionTree": {'max_depth':['1','3','5'],
                         'min_samples_split':['2','5','10'],
                         'min_samples_leaf':['1','5','10']
                             },
    "MLP":{'hidden_layer_sizes': ['(2,)','(5,)','(10,)','(2, 2)','(5, 2)','(10, 2)','(2, 5)','(5, 5)', '(10, 5)'] ,
           'activation':["logistic","relu"]}
}

def test_mlcomparisonworkflow(MLComparisonWorkflow,data_x,data_y):
    """ method to test the student's ML workflow class
    Parameters
    ----------
    MLComparisonWorkflow:  workflow class implementation
    data_x: 2-D numpy ndarray of r rows. and f features
    data_y: 1-D numpy array with r rows
    """
    # used for marking and feedback
    score = 0
    feedback  = ""
    ok = True
    
    
    #store details of "real" data and then write to file
    desired_shape_x = data_x.shape
    desired_shape_y = data_y.shape
    np.savetxt("data_x.csv", data_x, delimiter=",")
    np.savetxt("data_y.csv", data_y, delimiter=",")

    #create instance of student's class using these saved files
    # and check it has loaded the data correctly
    feedback += "==== Testing the constructor =====\n"
    mycomp = MLComparisonWorkflow(datafilename="data_x.csv", 
                                        labelfilename= "data_y.csv")

    #check data sizes after reading from file but before preprocessing
    #exit if data is not read correctly
    try:
        if mycomp.data_x.shape != desired_shape_x:
            feedback += ('Error reading data:\n'
                     f'X data size {mycomp.data_x.shape} '
                     f'should be {desired_shape_x}.\n'
                    )
            ok=False
    except AttributeError as e:
            feedback += (f'Constructor did not store data in specified variable.\n'
                         f'AttributeError:{e}\n'
                        )
            ok=False
    try:
        if  mycomp.data_y.shape != desired_shape_y:
            ok=False
            feedback += ( 'Error reading labels:'
                     f' y data size {mycomp.data_y.shape} '
                 f'should be {desired_shape_y}\n'
                    )
    except AttributeError as e:
            ok=False
            feedback += (f'Constructor did not store labels in specified variable.\n'
                         f'AttributeError:{e}\n'
                        )

    if not ok:
        feedback += ("Did you remember to set the delimiter to ','"
                     " in the call to np.genfromtxt(), "
                     "and use the attribute names data_x and data_y?\n"
                     "Not proceeding further with testing.\n"
                     "You score 0 at this stage\n")
        return 0, feedback
    else:
        feedback += "Constructor correctly loaded data. [10 marks]\n"     
        score = 10
                     
    ## run the workflow - we will test the functionality later  
    feedback += "\n ===Running preprocess(), and run_comparison()===\n"
    try:
        mycomp.preprocess()
        mycomp.run_comparison()
    except Exception as e:
        ok=False
        feedback += ("Exception encountered when running your code.\n"
                     "Use the feedback provided by the stack trace to debug your code.\n"
                     "To avoid wasting attempts  don't submit this work until you have fixed this error.\n"
                     f"{e}\n"
                    )
        return score , feedback
    except Error as e:
        ok=False
        feedback += ("Error encountered when running your code.\n"
             "Use the feedback provided by the stack trace to debug your code.\n"
             "To avoid wasting attempts  don't submit this work until you have fixed this error.\n"
             "Name Errors usualy come from having undefined variables in your code"
             f"{e}\n"
            )
    
    if not ok:
        return score, feedback
    
    else: 
        feedback += "\n==== That code all ran, now testing the stored models ====\n"
                     
    #Check 1: all the lists of saved models should be the right type and size
    
    for modelname, modeltype in names_and_types.items():
        storedlist= mycomp.stored_models[modelname]
        #size
        num_asked_for = combinations_requested[modelname]
        feedback += ( f"Looking at algorithm {modelname} "
                     f" you were asked to try {num_asked_for} "
                     "combinations of hyper-parameters.\n"
                     f"Your code stored {len(storedlist)} which is "
                    )
        if len(storedlist) == num_asked_for:
            feedback += "correct.\n"
        else:
            feedback += "incorrect.\n"
            ok= False
        
        #type
        for idx in range(len(storedlist)):
            model= storedlist[idx]
            if not isinstance(model,modeltype):
                ok=False
                feedback +=  ("There is a problem with the dictionary of stored models.\n"
                              f"Item {idx} in the list stored_models[{modelname}]"
                              f" should be of type {names_and_types[modelname]} "
                              f" but is of type {type(model)}.\n"
                             )
        # At last we know  we have the right things so we can check
        #if the correct combinations of parameter values were used
        if ok:
            hyperparams= {}
            for key in hyperparams_and_counts[modelname].keys():
                hyperparams[key] = []

            #see what is in the models
            for idx in range(len(storedlist)):
                model= storedlist[idx]
                for key in hyperparams.keys():
                    hyperparams[key].append( model.__dict__[key])

            #check if the values and counts are right
            alg_ok=True
            alg_feedback= '' 
            for key,val in hyperparams.items():
                string_list = [str(element) for element in val]
                values,counts = np.unique(string_list,return_counts=True)
                desired_vals = hyperparams_and_vals[modelname][key]
                desired_counts = hyperparams_and_counts[modelname][key]
                #print(f'key {key}, des_vals {desired_vals},'
                       #f'des_counts {desired_counts}, values {values} counts {counts} ')
                if ( len(counts) != len(desired_counts) or  
                     not np.equal(counts, desired_counts).all() or
                     len(values) != len(desired_vals) or  
                     set(values) != set(desired_vals)
                   ):
                    alg_feedback += (f'for hyper-parameter {key} we got these '
                                     f'incorrect values and counts {values}, {counts}\n'
                                     f' Expected: {desired_vals}, {desired_counts}.\n'
                                  )
                    alg_ok=False
            if alg_ok:
                feedback += (f'Algorithm {modelname} correctly tested with ' 
                             ' right combinations of values for hyper-parameters [10 marks].\n'
                                    )
                score += 10
            else:
                feedback += (f'Algorithm {modelname} tested right number of times. [5 marks]\n '
                                 'but not with right sets of hyper-parameters.\n'
                             f'{alg_feedback}.\n '
                            )
                score += 5

                
                

    if not ok:
        return score, feedback
    else: ## now go no to look at the preprocessing etc.
        knnlist= mycomp.stored_models['KNN']
        processed_data= knnlist[0]._fit_X
        processed_labels= knnlist[0]._y
        #get the ideal train/ test split data
        train_x,te_x,train_y,te_y = train_test_split(data_x,data_y,
                                               test_size=0.3,
                                               stratify= data_y,
                                               random_state=12345)
                                         
        # use data stored by KNN to see how data was preprocessed                                 
        feedback += ("\n===== Now testing preprocessing===\n"
                     "KNN stores the data - so we use that to examine "
                     "whether you have used a StandardScaler or a MinMax scaler\n"
                    )
        if processed_data.shape != train_x.shape:
            ok= False
            feedback += (f'data after preprocessing has shape {processed_data.shape}'
                         f'but it should be {train_x.shape} if you have '
                         'done a 70:30 train:test split and kept all the features\n'
                        )
        elif processed_labels.shape != train_y.shape:
            ok= False
            feedback += (f'labels after preprocessing have shape {processed_labels.shape}'
                         f'but it should be {train_y.shape} if you have '
                         'done a 70:30 train:test split and kept all the features\n'
                        )
        else:
            score += 5
            feedback += ('70% of data seems to have been correctly used for training.[5 marks]\n')                            
            nfeats= processed_data.shape[1]
            allones= np.ones(nfeats)
            allzeros = np.zeros(nfeats)
            minzero= np.isclose(np.min(processed_data,axis=0),allzeros).all()
            maxone = np.isclose(np.max(processed_data,axis=0),allones).all()
            meanzero = np.isclose(np.mean(processed_data,axis=0),allzeros).all()
            stdone = np.isclose(np.std(processed_data,axis=0),allones).all()
            
            if minzero and maxone:
                feedback += ( "MinMaxScaler has been correctly applied "
                             " to preprocess the x data [5 marks]\n"
                            )
                score += 5
            elif meanzero and stdone:
                feedback += ( "StandardScaler has been correctly applied "
                             " to preprocess the x data [5 marks]\n"
                            )
                score += 5
            else:
                feedback += ("data does not seem to have had preprocessing (scaling) "
                             " applied to every feature (column) independently.\n"
                             'Because the test data is supposed to be unseen '
                             'you should fit your scaler to the training data only, '
                             'but apply the same transformations to both train and test data.\n'
                            )
                                         
        # Now look at the labels provided to the stored models to look at the label encoder
        feedback += "\n==== Now looking at label encoding or knn vs MLP===\n"
        #knn uses raw labels
        if   np.array_equiv(processed_labels, train_y ):
            feedback += ' KNN were correctly trained with original labels. [5 marks]\n'
            score += 5
                                         
        mlplist = mycomp.stored_models['MLP']
        if mlplist[0]._label_binarizer.__dict__['y_type_']== 'multilabel-indicator':
            feedback += "MLP has been given one-hot encoded data. [5 marks]\n"
            score += 5
        else: 
            feedback += "MLP has not been given one-hot encoded data. [0 marks]\n"

    # now print findings from the workflow
    feedback += "\n=== testing results stored in summary dictionaries ===\n"
    best_idxes_ok = True
    if hasattr(mycomp, 'best_model_index') and isinstance( mycomp.best_model_index,dict):
        for alg in names_and_types.keys(): #loop over requested algorithms
            idx= mycomp.best_model_index.get(alg,'missing')
            if idx=='missing':
                feedback+= f'stored best index missing for {alg}'
                best_idxes_ok= False
            elif idx <0 or idx >= combinations_requested[alg]:
                feedback+= f'stored best index {idx} out of bounds for {alg}'
                best_idxes_ok= False 
            else:
                feedback += f'valid index of best model stored for {alg}.\n'
        if best_idxes_ok:
            score += 5
            feedback += 'Indexes of best model found for each algorithm stored ok. [5 marks].\n'
    else:
        feedback += ("Record of best index for each type of model not correctly stored "
                     "in dict as specified"
                    )
    best_accs_ok = True
    best_acc_found = -1
    best_alg_found = 'unk'
    if hasattr(mycomp, 'best_accuracy') and isinstance( mycomp.best_model_index,dict):
        #print(f'mycomp.best_accuracy {mycomp.best_accuracy}\n')
        for alg in names_and_types.keys(): #loop over requested algorithms
            acc= mycomp.best_accuracy.get(alg,'missing')
            if acc=='missing':
                feedback+= f'stored best accuracy missing for {alg}'
                best_accs_ok= False
            elif acc <0 or acc >100:
                feedback+= f'stored best accuracy {acc} out of bounds for {alg}'
                best_accs_ok= False 
            else:
                feedback += f'valid accuracy {acc} of best model stored for {alg}.\n'
                if acc > best_acc_found:
                    best_acc_found = acc
                    best_alg_found = alg
        if best_accs_ok:
            score += 5
            feedback += 'Accuracy of best model found for each algorithm stored ok. [5 marks].\n'
        #print(f'found {best_acc_found} for {best_alg_found}.\n')
    else:
        feedback += ("Record of best accuracy for each type of model not correctly stored "
                     "in dict as specified")
    
    # at very long last ... check the reporting
    reportok = True
    try:
        best_accuracy, best_algname, best_model = mycomp.report_best()
    except :
        feedback += 'report_best() method failed to run and threw exception or error.\n'
        reportok=False
    if reportok:
        if not np.isclose(best_accuracy, best_acc_found, 0.01):
            feedback += (
                f'Odd: your report_best() method said the best accuracy was {best_accuracy} '
                f'but inspecting your workflow object showed the best had accuracy {best_acc_found}.\n'
            )
        else:
            score += 3
            feedback += ( 'Your code returned the correct best accuracy found. '
                         f' ({100*best_accuracy}%) [3 marks].\n'
                        )
        if best_algname !=  best_alg_found:
            feedback += (
                f'Odd: your report_best() method said the best algorithm was {best_algname} '
                f'but inspecting your workflow object showed better results with {best_alg_found}.\n'
            )
        else:
            score += 3
            feedback += ( 'Your code returned the name of the best algorithm tested '
                         f'({best_algname})[3 marks].\n'
                        )
        righttype = names_and_types[best_alg_found]
        if not isinstance (best_model, righttype):
            feedback += 'Wierd: Best model  returned is not an instance of right model type'
        else:
            right_list = mycomp.stored_models[best_alg_found]
            right_index = mycomp.best_model_index.get(best_alg_found)
            right_model = right_list[right_index]
            if best_model == right_model:
                feedback += 'Best model correctly returned for use making predictions[4 marks]'
                score += 4

            feedback += '\nOut of interest, these are the best hyperparameters found:\n'
            for key in hyperparams_and_counts[best_alg_found].keys():
                val= best_model.__dict__.get(key,'missing')
                feedback += (f'{key} : {val}')
        feedback += (f'\n===Overall you score {score} / 75 ===\n')
    return score, feedback