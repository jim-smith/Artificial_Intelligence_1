#=====================================================    
def Evaluate(soln: candidateSolution ):
    location = [0,0,0,0]
    global reason
    reason = ""
    boat=3
    grain=2
    chicken=1
    fox=0
    for move in soln.variableValues:
        valid = True
        if(move==0): 
            if(location[boat]!=0):
                valid = False
                reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=1
        elif(move==1):
            if( location[boat]!=0 or location[grain]!=0):
                valid = False
                reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 1
        elif(move==2):
            if( location[boat]!=0 or location[chicken !=0]):
                valid = False
                reason = "boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 1
        elif(move==3):
            if( location[boat]!=0 or location[fox]!=0):
                valid = False
                reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 1                
        elif(move==4): 
            if(location[boat]!=1):
                valid = False
                reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=0
        elif(move==5):
            if( location[boat]!=1 or location[grain]!=1):
                valid = False
                reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 0
        elif(move==6):
            if( location[boat]!=1 or location[chicken !=1]):
                valid = False
                reason = " boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 0
        elif(move==7):
            if( location[boat]!=1 or location[fox]!=1):
                valid = False
                reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 0                         
 
        else:
            print('error- unknown move encountered: ' +str(move))
            
        # check for infeasible partial solutions
        if( location[boat] != location[chicken]):
            if( location[chicken]==location[fox]):
                reason = 'fox eats chicken'
                soln.quality=-1
                break
            if(location[chicken]==location[grain]):
                reason = 'chicken eats grain'
                soln.quality=-1
                break
        #check for goal
        if (location == [1,1,1,1]):
            soln.quality=1
            print('goal reached')
            break
    return reason
            
#=================================================================
def to_display(soln:candidateSolution):
    nummoves= len(soln.variableValues)
    movelist = ""
    for move in soln.variableValues:
        #movelist = movelist + " -> " + moveNames [move] 
        movelist = movelist + "->" + moveNames [move] 
    return movelist

#======================================================        
#python 3 lets us define the types of parameters if we want to
def IsAtGoal(soln:candidateSolution): 
    if(soln.quality==1):
        return True
    else:
        return False
    
    
#======================================================
