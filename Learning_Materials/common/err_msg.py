from sys import exc_info as EXC

import traceback

import re

# There are TWO functions here. One to process errors from the student submission that should not happen. i.e. the student's code is bugged. The other function is to process
# exceptions raised by the student code which we expected the student code to raise.


def processError(e,func = 'studentMethod'):

	# Called when the student code unexpectly raises an error.

	exceptionInfo = EXC();
	
	errTypeStr = format(exceptionInfo[0])
		
	#errTypeStr = errTypeStr.replace('<class ','')

	#errTypeStr = errTypeStr.replace('>','')
	#errTypeStr = errTypeStr.replace('\'','')
		
	errorMsg = f'{errTypeStr}\n:{e}'
	
	# errorMsg = "<div style='border:2px solid red;padding:10px'>"
	
	errList = traceback.format_exc().split('\n')		# contains the more detailed inform about the error
	
	outStr = ''
	
	useNext = False
	
	for x in errList:
		 
		# x = re.sub('/usr/lib/d/.*/work/','',x)

		outStr += (f'{x}\n')

		#if (useNext):
		#	x = x.replace('studentMethod',func)
		#	outStr += ('<b>'+x+'</b><br>')
		#	useNext = False
		#elif ('_marking.py' in x):
		#	x = x.replace('markThis','calling your supplied function')
		#	outStr += x+'<br>'
		#	useNext = True
		#elif ('student.py' in x):
		#	outStr += x+'<br>'
		#	useNext = True
	
	# outStr = outStr.replace('File "/usr/lib/d/data-code/catalogue/nobody/2022-uwe/ufmflv_30_1/CWK1','File "')
	
	errorMsg += (f'Partial Traceback:\n{outStr}\n')
	
	return errorMsg

#=============================================
	
def getExceptionDetails(e):

	# Used when we are expecting the student code to report an error (as required in the cwk spec) and we want to extract the error details to see if the
	# student's error reporting agrees with what we are expecting.

	exceptionInfo = EXC();
	
	errTypeStr = format(exceptionInfo[0])
	#errTypeStr = errTypeStr.replace('<class ','')
	#errTypeStr = errTypeStr.replace('>','')
	#errTypeStr = errTypeStr.replace('\'','')
		
	errorMsg = format(e)
	
	return errTypeStr, errorMsg	