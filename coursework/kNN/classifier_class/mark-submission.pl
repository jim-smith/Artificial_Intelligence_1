
use strict;

#================================================================
#
# In this example we will use just one performance indicator: $f1
#
# $f1 = -1	There was a problem with the submitted file (see $x4 for string explanation)
#
# $f1 >= 0   The submission was received and this flag now contains the marks awarded
#
# The parameter $feedback will be the feedback string (for now we will make it in html format - can be different)
#

our ($codeSubmission_WorkFolder,$codeSubmission_StoreFolder);

#=====================================================

our $MarkFile_outputFileName = 'main.txt';		# The filename of the file we will analyse as part of the marking.

our $MarkFile_errorFileName = 'compiler.wri';

#=====================================================

our $SandboxTimeLimit = 20;

our $SandboxProject = 'classifier';  # lower case string with no spaces

#=====================================================

# Following is the actual executable

our $UseCurl = 1;  # THIS IS NOT TO BE ALTERED

our $MarkFile_ExecutionBlock = "REMOTE";

#====================================================================================================

sub FileInputs_markContents
{
	# This is the assessment specific part of the marking. The Python's output is contained in '@$contents_'.
	
	# In this assessment, we don't actually do much analysing here since the Python has done most of the work, including obtaining a mark for the assessment.
	
	my $contents_ = shift();			# The contents outputted by Python

	#================================
	
	# Here we analyse the output from the Python file and respond accoringly. This is a bespoke part of the code.
	
	my ($feedback,$markScored) = ('',-1);
	
	my $readStage = 0;
	
	foreach my $line (@{$contents_})
	{
		$line =~ s/\s+$//;	# a crop
	
		if (($line =~ m/^<MESSAGE>$/) && ($readStage == 0))
		{
			$readStage = 1;
			next;
		}
		elsif ($readStage == 1)
		{
			if ($line =~ m/^<\/MESSAGE>$/)
			{
				$readStage = 2;
				next;
			}
			else
			{
				$feedback .= "$line\n";
			}
		}
		elsif ($readStage == 2)
		{
			if ($line =~ m/^<SCORE>(\d+)<\/SCORE>$/)
			{
				$markScored = $1;
			}
		}
	}
	
	if ($markScored == -1)
	{
		$feedback =  "<b>There was a process error here due to an error in the code that the system could not capture. Please contact the person responsible for this assessment for an explanation of what happened. @{$contents_}\n\n";
		
		$markScored = 0;
	}
	
	FileInputs_constructFeedback($feedback,$markScored);
	
	# Two ways to populate the mark ... not sure which one is implemented but, anyway.
	
	my $mark = shift();
	${$mark} = $markScored;
	
	return $markScored;			# This routine needs to return the mark scored.
}

#====================================================================================================

sub FileInputs_compilerErrorReportOld
{
	# If this is called then we know there is a compiler error and it is contained in @{$contents_}.
	
	# We need to just write it to the output file in the same format as a standard Python output we use.

	my $contents_ = shift();

	for (@{$contents_})
	{
		s/\".+\/work\/student.py\"/"<span style=\'color:red\'>student.py<\/span>"/;
		
		s/</&lt;/g;
		s/>/&gt;/g;
	}
	
	# This is the compiler error we will send to the student's output screen - we will use the same format as for the Python output
	
	my $outputReport = qq £

<MESSAGE>	
<span style='color:red;font-weight:bold;'>Compiler Error Detected</span>:
<p></p>
An error was reported in running the Python code using your input file which we named 'student.py'.
<p></p>
Please have a look at the following error report to deduce what is wrong with the code:
<p></p>
<pre style='font-weight:bold;color:darkred;font-size:120%'>
@{$contents_}
</pre>
</MESSAGE>

# Compiler error gets zero score.
<SCORE>0</SCORE>
£;
		
	FileInputs_writeToOutputFile($outputReport);			# the second parameter is the mark scored by the student
	
	return $outputReport;
}

#====================================================================================================



1;
