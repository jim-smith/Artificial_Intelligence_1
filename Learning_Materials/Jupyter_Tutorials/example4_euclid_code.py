# This file contains the definition of the Euclid function.
# This function takes in two inputs which we label m and n.
# The function calculates the highest common divisor of m and n and then outputs this value to the code that calls the function.
# It is the 'return' command that sends the output of the function back to the calling code.
# At this stage, do not concern yourself unduly about the actual code in the function. Just recognise that the inputs
# are labelled m and n and that it is the 'return' command that sends the value back out.
#
# For example, in the main code in the Jupyter notebook, if one executed the code 'Euclid(90,72)' then the function call
# would return the value 18.
# 
# Please note that there are some flaws to the following code; e.g. we have not checked for the instance of negative numbers.
#

def Euclid(m,n):
    while (m != n): 
        if (m > n):
            m = m - n
        else:
            n = n - m
    return m

