# commented out by jim
use strict;

# In V4, unlike V3, here we assume that the student submits a Python .py file and that we do not do anything to extract the code to be marked. i.e. it is the whole code that will
# be imported, with maybe minor alterations.

# (In V3, on the other hand, a JupyterLab ipynb notebook file was submitted and Dewis would extract the code cells containing the definition of the relevant functions to be tested.)

our ($codeSubmission_WorkFolder,$codeSubmission_StoreFolder);

#============================================

my $maxFileSize = 20*1024;

our $SubmittedFileName = 'student.py';          # the name we will allocate to the submitted file

# Be carefull with the @OverrideBannedList ... if you allow just 'import numpy' without the end of line then you are also allowing 'import numpy, sys' which is dangerous.

our @OverrideBannedList = (
        #'^from\s+LearnedRuleModel\s+import\s+LearnedRuleModel\s*$',
'^import\s+numpy(\s+as\s+\w+)?\s*$',
'^import\s+math(\s+as\s+\w+)?\s*$',
'^import\s+numpy\s+as\s+np(\s+as\s+\w+)?\s*$',

);      

#============================================


#============================================

sub checkAcceptableFile
{
	# Check in here for any banned content in the file.
	
	# In the return DO NOT INCLUDE a pound sign as that is used as a string delimitter.
	
	our $StudentOriginalFileLoc;
	
	my $location = $StudentOriginalFileLoc;		# location of the student's original (unaltered) submission
	
	#================
	
	my @stats = stat $location;
	
	if ($stats[7] > $maxFileSize)
	{
		return 'File too big';
	}
		
	#================
	
	open(FILIN,"< $location") or die "Cannot open file";
	my @contents = <FILIN>;
	close(FILIN);
	
	# Project-bespoke analyse file .... can analyse the contents here... the input file contents are held in '@contents'.
	
	# Return empty-string if ok but return error string if not.
	
	#==============

	# It is a condition of use of Dewis that this function is called. It absolutely must be called with absolutely no exceptions!

	my $errorReport = PERFORM_STD_CHECK(\@contents);
	
	if ($errorReport)
	{
		return $errorReport;
	}
	
	#==============
	
	# Here's an example of code that can be implemented if you want to put in a bespoke checker of things in here.
	
	#	$problemMessage = exampleReject(\@contents);
	#
	#	if ($problemMessage)
	#	{
	#		return $problemMessage;
	#	}

	#=================
		
	return '';		# all is ok
}

#=======================

sub editOriginalForRun
{
	# If this function exists then it is auto-called in the on-submission.pl file for general python submissions

	our $StudentOriginalFileLoc;
	
	my $location = $StudentOriginalFileLoc;		# location of the student's original (unaltered) submission
	
	open(FILIN,"< $location") or die "Cannot open file";
	my @contents = <FILIN>;
	close(FILIN);

	#====

	BespokeModifier(\@contents);	

	#====

	# This is done instead of just outputing the @contents since, for some reason, a space was put before every entry in @contents
	
	my $contentsString = getContentString(\@contents);

	#====

		
	$location =~ s/\-orig\./-altered\./;
	
	open(FILIN,"> $location") or die "Cannot open file";
	print FILIN "$contentsString";
	close(FILIN);
	
	return $location;
}

#==========================

sub BespokeModifier
{
	return '';		# does nothin in this assessment
}

1;
