import numpy as np
import load_datasets as ld


from correct_simple_KNN import simple_KNN as Correct
from student import simple_KNN as Student
from simple_1NN import simple_1NN 


from err_msg import processError, getExceptionDetails

# MARK-A: THE PURPOSE
#
# Runs the student's code on three different datasets
#


##======================================
## def TestAlgorithm on Dataset
# runs a provided model on aprovided dataset:
# this gets called 3 models (correct, student,rule induction) x 3 datasets times
def TestAlgorithmOnDataset(theModel,X_train, y_train,X_test,y_test,verbose=False):

    debug = verbose #controls level of detail printed during run
    constantPred= False
    theModel.fit(X_train,y_train)
    if(debug):
        pass

    ypred = theModel.predict(X_test)
    
    # arrays to check no invalid predictions
    classesPresent = np.unique(y_train)
    numClasses = len(classesPresent)
    invalidPreds = []
              
              
    confusionMatrix = np.zeros((numClasses,numClasses+1),np.uint)
    accuracy = 0.0
 
    for i in range(len(y_test)):
        actual = int(y_test[i])
        predicted = int(ypred[i])
        #put all the erroneous predictyions into an extra column in the confusion matrix and store them for feedback
        if(predicted not in classesPresent):
            if(debug):
                print("Classifier wrongly predicted a label {} which does not exist in the training set".format(predicted))
            invalidPreds.append(predicted)
            predicted=numClasses
 
        confusionMatrix[actual][predicted] += 1
        if(actual==predicted):
            accuracy += 1.0
    accuracy = accuracy*100/len(y_test)
    if (len(invalidPreds) >0):
          accuracy = -1
    
    if(debug):
        print("\tTest accuracy on this dataset is {}%, and the confusion matrix is:".format(accuracy))
        header= "\tPredicted|"
        for label in range(numClasses):
            header = header + "  " + str(int(classesPresent[label])) + " "
        header = header + " Invalid"
        print(header)
        for row in range(numClasses):
            rowString= "\tActual   |"
            for column in range(numClasses+1):
                rowString = rowString + "  " + str(confusionMatrix[row][column] )
            print(rowString)
 
    if len(np.unique(ypred)) == 1:
        constantPred= True
    
    return accuracy, invalidPreds,constantPred





##==================================================
##
### This is the main marking function
##
##
def MarkClassifier(): 

    
    kValues = (1,3,5,9)
    numK=len(kValues)
    
    datasets = [ ld.load_dataset2(),  ld.load_dataset4(),ld.load_dataset5()]
    numSets=len(datasets)

    setDesc = (#"a simple 2-class problem with one predictive variable, all others are zero",
               "a three class problem defined by values for 2 variables, all others are noise",
               #"a simple 2 class problem with  one predictive variable, all others are noise",
               " a two class problem with a curved decision boundary defined by  two randomly chosen features",
                " a two class problem with a curved decision boundary defined by three randomly chosen features"
              )
    correctDeltas = np.zeros(numSets*numK)
    oneNNDeltas = np.zeros(numSets*numK)
    madeInvalid = 0
    numConstantPreds = 0
    
    message = "\n"
    
    
    for k in range (numK):
        K= kValues[k]
        message = message + f"With K = {K}.\n"
        for setNum in range(len(datasets)):
            index = setNum*numK +k
            
            #get data
            train_X,train_y,test_X,test_y = datasets[setNum]
             
            #results for correct, knn and student classifiers
            
            correctModel = Correct(K=K,verbose=False)   
            correctTestScore,_,_ = TestAlgorithmOnDataset (correctModel,train_X,train_y,test_X,test_y,verbose=False)
            oneNNModel = simple_1NN(K=K,verbose=False) 
            oneNNTestScore,_,_  = TestAlgorithmOnDataset (oneNNModel,train_X,train_y,test_X,test_y,verbose=False)
    
            #ca nstudetn code successfully create a model
            try:
                studentModel = Student(K=K,verbose=False) 
            except Exception as e:
                #print(str(e))
                message = f"your code failed to creater a  model instance and produced this error message:\n "
                message += processError(e,func=Student)
                message += ("So you score 0 for this attempt.\n"
                            "Otherwise trace through the  message printed above "
                            "to find the line in your code that is producing the error.\n"
                           )
                return 0, message
            
            try:
                studentTestScore, studentInvalids,allsame = TestAlgorithmOnDataset(studentModel, train_X,train_y, 
                                                                                   test_X,test_y, verbose=False)
            except Exception as e:
                #print(str(e))
                message = ( "Your code createrd a model isntance ok, "
                           "but then failed to run when asked to fit and predict a dataset. \n"
                            "It produced this error message:\n "
                            f"{processError(e,func=Student)}"
                            "So you score 0 for this attempt.\n"
                            "Otherwise trace through the  message printed above"
                            "to find the line in your code that is producing the error.\n"
                           )
                return 0, message
            
            
            
            
                
                
            correctDeltas[index] = np.abs(correctTestScore - studentTestScore)
            oneNNDeltas[index] = np.abs(oneNNTestScore - studentTestScore)
    
            message = message + (
                f"On dataset {setNum}, {setDesc[setNum]}.\n"
                f"\tYour method got a test accuracy of {studentTestScore}\n"
                f"\tThe target for this dataset was {correctTestScore} "
                f" so on this dataset the difference was {correctDeltas[index]}\n"
            )

            if allsame:
                numConstantPreds += 1
                message += "In this case your algorithm always made the same prediction.\n"

            if(len(studentInvalids)>0):
                message += "\tCrucially,  your algorithm predicted labels not in the training set.\n"
                madeInvalid += 1
            message += "\n"

 
    # Finally print summary message and score
    message = message+"Overall:\n"
    
    if (numConstantPreds >0):
        message += (f"To help you improve your code, note that in {numConstantPreds} runs "
                    "your algorithm always made the same prediction.\n"
                   )
    finalScore = 0
    if (madeInvalid>0):
        message = message + "Your algorithm made some invalid predictions, therefore you score 0"
        finalScore = 0
    else:
        
        #check for differencde ot 1NN and use this to provide feedback
        wrongAlg = False
        if(np.mean(oneNNDeltas) < 2):
            message = message + (
                "The results are very close to what a 1-NN classifier gets."
                "Did you implement this by mistake?\n"
            )
            wrongAlg=True

        
        #base score on difference in accuracy to correct code
        meanDiff= np.mean(correctDeltas)
        maxDiff = np.max(correctDeltas)
        message  += ("Your algorithm makes valid predictions.\n"
                     "Over all the datasets and values of K, "
                     "the mean and maximum difference in test accuracy "
                     f"to the correct code is {meanDiff:.3}% and {maxDiff:.3}%\n"
                    )

        if(maxDiff>10):
            message += ( "As the test accuracy is more than 10% away from the target"
                           "on one or more datasets, you score 10\n"
            )
            finalScore = 10
            
        elif ( meanDiff <10 and meanDiff>5):
            message += ("The mean difference to the target test accuracy "
                        "is between 5% and 10% so you score 40.\n"
            )
            finalScore=40
            
        elif ( (meanDiff <= 5.0)and (meanDiff >=2.5)):
            message  += "The mean difference to the target accuracy is between 2.5 and 5 percent."
            if  (maxDiff >= 5):
                message += " However, the difference is greater than 5 for one or more datasets so you score 50.\n"
                finalScore = 50
            else :
                message += "The difference is less than 5 for all datasets so you score 60.\n"
                finalScore = 60
        elif(meanDiff >= 1.0 and meanDiff<2.5):
            message += ("On average your  test accuracy is within 1 and 2.5 percent" 
                        " of the target accuracy so you score 70.\n"
            )
            finalScore = 70
        elif(meanDiff < 1.0):
            message += ("The mean test accuracy is less than 1 percent away from target."
                                 " You score 100 for this run.\n"
            )
            finalScore = 100
        
        
    return finalScore,message       
#======================