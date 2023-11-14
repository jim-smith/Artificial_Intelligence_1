# General 
- [ ] Be consistent about the use (or not) of 'notes' slides becuase they appear in the notebooks.REMOVE THEM

# Re-ordering
- nothing in the search weeks that relies on previous knowledge,
  - but it could be good to say 'we'll see. this later' sometimes.
- perceptron: copy the 'learning binary problems' example from the notebook to the lectures
- for ANN do a walk-through of an actual example.
  - maybe move the iris data to the lecture and do with the full three class
  - use scatter plots to show decision surface ?
  
- then 

- add new search week on estimating local gradients without explicit need to sample neighbourhood points

- old week 9 (MLP) has an intro which has cell "Perceptrons - The basis of Artificial Neural Networks" - copy and paste that to end of old week 8 as summary





# Python skills


# Testing MCQs
```
def check_mcq(id:widgets.VBox)->int:
    if len (id.children)>=4 and len(id.children[3].outputs)>0:
        if 'Correct' in id.children[3].outputs[0]['text']:
            return 1
        else:
            return 0
    else:
        return -1 #not answered
    
    
def test_mcqs():
    mcqs= [Q1,Q2,Q3,Q4,Q5,Q6,Q7]
    correct = 0
    for q in range(len(mcqs)):
        res= check_mcq(mcqs[q])
        errmsg= "no answer submitted" if res== -1 else "incorrect answer"
        try:
            assert res==1, errmsg
            print (f' question {q}: answered correctly')
            correct += 1
        except AssertionError:
            print (f' question {q}: {errmsg}')
    print(f' Total: {correct} out of {len(mcqs)} questions answered correctly\n')
```