""" bannedkeywords.py
Helper code for self-checker notebooks that screen student code for issues
Author: Jim Smith 2025
"""

blacklist= ['system', 'open','import']
whitelist = ["from approvedimports import *","openlist"]

def check_for_banned_words(filename:str)->str:
    '''Checks for presence of banned words in a file.
    Allows for whitelisted lines
    '''

    retval= []
    with open(filename, 'r',encoding='utf8') as thefile:
        thelines= thefile.readlines()

    for num,line in enumerate(thelines):
        #drop the newline
        line = line[0:-1] if len(line)>0 else line

        whitelisted,blacklisted =False, False

        linestr= f'testing line number {num}: "{line}"'
        for allowed in whitelist:
            if line == allowed:
                whitelisted=True
        if whitelisted:
            linestr+= f'  : whitelist matched:"{allowed}"'

        else:
            for banned in blacklist:
                if banned in line.split(" "):
                    blacklisted=True
                    newret = (
                        f'banned keyword {banned} '
                        f'present on line {num}: {line}\n'
                        )
                    retval.append(newret)
                    linestr += f" : banned word {banned} found."
        if not blacklisted:
            linestr+= 'line ok'

        #print(linestr)
    retval= ["no banned keywords found"] if len(retval)==0 else retval
    return retval

def add_to_file(filename:str, what:str):
    '''appends a str to a file as a new line'''
    with open(filename, 'a',encoding='utf8') as f:
        f.write(what+"\n")

def get_file_lines(filename:str)->int:
    '''gets number if lines in file'''
    with open(filename, 'r',encoding='utf8') as thefile:
        thelines= thefile.readlines()
    return len(thelines)

def test_check_for_banned_words():
    '''' tests correct operation of banned words check'''
    myfile:str= "delete-me.py"
    oklines= []

    oklines.append(whitelist)
    oklines.append("blahsystem")
    oklines.append("this is a line about openlists")
    oklines.append("foopen")

    for line in whitelist:
        add_to_file(myfile,line)
    for banned in blacklist:
        add_to_file(myfile, "prefix"+banned)
        add_to_file(myfile, banned + "suffix")

    with open(myfile,'r',encoding='utf8') as safefile:
        content= safefile.readlines()
        safe_linecount= len(content)
        print('File with safe contents is:\n',*content)

    testval= check_for_banned_words(myfile)
    errstr= f"error-this file should have been ok: {testval}"
    assert len(testval)==1 and testval[0] == "no banned keywords found", errstr

    print("Safe version of file recognised as ok.\nNow appending various unsafe lines")


    for num,banned in enumerate(blacklist):
        testline= "prefix "+banned+" suffix"
        add_to_file(myfile, testline)
        try:
            retval= check_for_banned_words(myfile)
        except AssertionError:
            pass
        if len(retval)!= num+1:
            errstr= "Error: failed to detect: "+testline
            assert False,errstr
        else:
            linenum=get_file_lines(myfile)
            checkstr = f"banned keyword {banned} present on line {linenum -1}"
            errstr= (
                f'error msg "{checkstr}" not present '
                f'in line "{retval[-1]}" '
                f'retval is "{retval}"'
            )
            assert checkstr == retval[-1].split(':',maxsplit=1)[0],  errstr



    with open(myfile,'r',encoding='utf8') as unsafefile:
        content= unsafefile.readlines()
        print('File now has these unsafe contents:\n',*content[safe_linecount:])

    print('tests for banned words passed')

if __name__ == '__main__':
    # runs test for banned keyword checker
    import os
    test_check_for_banned_words()

    if os.path.exists("delete-me.py"):
        os.remove("delete-me.py")
    else:
        print("Error: file `delete-me.py` does not exist")
    