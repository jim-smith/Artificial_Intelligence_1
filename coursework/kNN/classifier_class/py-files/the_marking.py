
from mark_knn_classifier import MarkClassifier

#======================

def MarkingFunction():

    runNum=1

    overallFeedback = ''

    totalMarks, text = MarkClassifier()# returns an int and fedback text
    
    headerStr = "<p></p><div style='border:2px solid darkred;padding:5px'><b>Run "+repr(runNum)+"</b><p></p>"

    overallFeedback += (headerStr+text+"</div>")

    return totalMarks, overallFeedback

