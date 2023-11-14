from candidatesolution import CandidateSolution
       
#python 3 lets us define the types of parameters if we want to
def is_at_goal(soln:CandidateSolution): 
    if(soln.quality==1):
        return True
    else:
        return False
    
    
#======================================================

# define the encoding we will use for moves 
possible_moves= [0,1,2,3,4,5,6,7]
move_names = ["empty_0to1","Grain_0to1","Chicken_0to1","Fox_0to1","empty_1to0","Grain_1to0", "Chicken_1to0", "Fox_1to0"]    
    
#moveNames = ["b01","G01","C01","F01","b10","G10", "C10", "F10"]    
    
    
    
#=====================================================    
def evaluate(soln: CandidateSolution ):
    location = [0,0,0,0]
    boat=3
    grain=2
    chicken=1
    fox=0
    #set initial values for solution
    soln.quality=0 #valid but incomplete
    soln.reason = ""
    soln.breaks_constraints = False
    #valid is whether boats and cargo are in right place
    #different to constr
    valid = True
    for next_move in soln.variable_values:
        if(valid and next_move==0): 
            if(location[boat]!=0):
                valid = False
                soln.breaks_constraints= True
                soln.reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=1
        elif(valid and next_move==1):
            if( location[boat]!=0 or location[grain]!=0):
                valid = False
                soln.breaks_constraints= True
                soln.reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 1
        elif(valid and next_move==2):
            if( location[boat]!=0 or location[chicken !=0]):
                valid = False
                soln.breaks_constraints= True
                soln.reason = "boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 1
        elif(valid and next_move==3):
            if( location[boat]!=0 or location[fox]!=0):
                valid = False
                soln.breaks_constraints= True
                soln.reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 1                
        elif(valid and next_move==4): 
            if(location[boat]!=1):
                valid = False
                soln.breaks_constraints= True
                soln.reason = "boat is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat]=0
        elif(valid and next_move==5):
            if( location[boat]!=1 or location[grain]!=1):
                valid = False
                soln.breaks_constraints= True
                soln.reason = "boat and/or grain is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[grain] = 0
        elif(valid and next_move==6):
            if( location[boat]!=1 or location[chicken !=1]):
                valid = False
                soln.breaks_constraints= True
                soln.reason = " boat and/or chicken is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[chicken] = 0
        elif(valid and next_move==7):
            if( location[boat]!=1 or location[fox]!=1):
                valid = False
                soln.breaks_constraints= True
                soln.reason = " boat and/or fox is in wrong place"
                soln.quality=-1
                break
            else:
                location[boat] = location[fox] = 0                         
 
        else:
            reason= 'error- unknown move encountered: ' +str(move)
            soln.breaks_constraints= True
            soln.reason= reason
            soln.quality=-1
            
        # does valid partial solution break the constraints?
        if( valid and location[boat] != location[chicken]):
            if( location[chicken]==location[fox]):
                soln.reason = 'fox eats chicken'
                soln.breaks_constraints= True
                soln.quality=-1
                break
            if(location[chicken]==location[grain]):
                soln.reason = 'chicken eats grain'
                soln.breaks_constraints= True
                soln.quality=-1
                break
        #check for goal
        if (valid and location == [1,1,1,1]):
            soln.quality=1
            soln.breaks_constraints= False
            print('goal reached')
            break
    
    
            
#==================================================================            
def display(soln:CandidateSolution):
    nummoves= len(soln.variable_values)
    movelist = ""
    for move in soln.variable_values:
        #movelist = movelist + " -> " + moveNames [move] 
        movelist = movelist + "->" + move_names [move] 
    print( movelist)
