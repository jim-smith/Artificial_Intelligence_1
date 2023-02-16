
# THIS IS AIMED TO BE QUESTION INDEPENDENT

import resource as RESRC

#========================================================================

# Do a general loading test first of all

def main():
    try:

        import student

    except Exception as e:

        from loading_error import LoadingError

        outStr = LoadingError(e)

        errMsg = '<b>Please note</b>: We encounterd a loading error in doing an \'import\' on your code. The result is that we cannot mark any of your submission. More detail is given below:<p></p>'

        PublishMarksFeedback(0,(errMsg+outStr))

        sys.exit(0)

	#========================================================================

    import the_marking as Marking		

    # Each mark function has the following: numRuns, markThis

    # ============================================
    # Memory limiter
    
    import platform
    if platform.system() != 'Darwin':
        MAX_MEM = 3

        RESRC.setrlimit(RESRC.RLIMIT_AS, (MAX_MEM, MAX_MEM)) 
        RESRC.setrlimit(RESRC.RLIMIT_DATA, (MAX_MEM, MAX_MEM)) 
        RESRC.setrlimit(RESRC.RLIMIT_STACK, (MAX_MEM, MAX_MEM)) 


    #===============================================================================================

    totalMarks, overallFeedback = Marking.MarkingFunction()
    #import numpy as np
    #reps=10
    #scores=np.zeros(reps)
    #for i in range (reps):
    #    scores[i],_ = Marking.MarkingFunction()
    #print(f' on {reps} runs there were {len(np.unique(scores))}different results')

    overallFeedback += "<p></p>You scored "+repr(totalMarks)+" marks for your submission.</div>"

    #=============================================================================================

    PublishMarksFeedback(totalMarks,overallFeedback)

#=============================================================================================

def PublishMarksFeedback(scored,feedbackStr):

    print("<MESSAGE>\n")
    print(feedbackStr)
    print("</MESSAGE>\n")
    print("<SCORE>"+repr(scored)+"</SCORE>\n")
    
#=============================================================================================
	
if __name__ == "__main__":
    main()
