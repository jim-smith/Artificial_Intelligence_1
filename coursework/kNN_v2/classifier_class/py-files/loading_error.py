from sys import exc_info as EXC

import traceback

import re

def LoadingError(e):

	exceptionInfo = EXC();
	
	errTypeStr = format(exceptionInfo[0])
		
	errTypeStr = errTypeStr.replace('<class ','')

	errTypeStr = errTypeStr.replace('>','')
	errTypeStr = errTypeStr.replace('\'','')
		
	errorMsg = "<div style='border:2px solid red;padding:10px'><b>Error Type</b>: "+errTypeStr+"<p></p><b>Message</b>: "+format(e)+" "
	
	errList = traceback.format_exc().split('\n')		# contains the more detailed inform about the error
	
	outStr = ''
	
	useNext = False
	
	for x in errList:
		 
		x = re.sub('/usr/lib/d/.*/work/','',x)

		if ('Traceback (most' in x):
			continue

		outStr += x+'<br>'
	
	# outStr = outStr.replace('File "/usr/lib/d/data-code/catalogue/nobody/2022-uwe/ufmflv_30_1/CWK1','File "')
	
	errorMsg += ('<p></p><b>Partial Traceback</b>:<div style="background-color:grey;color:white;border:grey 1px solid;padding:10px">'+outStr+"</div></div>")
	
	return errorMsg