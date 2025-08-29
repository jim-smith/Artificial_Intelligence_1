import importlib
import traceback




def check_code_syntax(package_name:str,directory:str="studentcode")-> tuple[bool,str]:
    """ Checks the syntax of code in a file wont prevent import
    Parameters:
    ------------
    package_name:str
        the name of the file, 
    directory:str
        ther name of where the code might be found assumed to be in the python interpreters path

       Returns:
    --------
    bool: was the code syntax ok so that the code could be imported
    str: more information and error messages
    """
    try:
        importlib.import_module(package_name,package=directory)
        return True,""
    except ModuleNotFoundError:
        return False, f'The  code file {package_name} does not seem to be present'
    except SyntaxError as e:
        message = ( f'Found a problem in your code of type {type(e)}\n'
                   f'Message: is {e}\n'
                   'Last item in traceback is:\n'
                   f'{traceback.format_exc(limit=0)}'
                  )
        return False, message
        



    
def test_for_presence(package_name:str, funcname:str, directory=".")-> tuple[bool,str]:
    """ Checks whether a function or class with a name is defined and callable in a code file 
    Parameters:
    ----------
    package_name:str
        The file of code. 
    funcname:str
       the name of the function or class that should be present
    directory: str
        Relative location of the package (default current directory)

    Returns:
    --------
    bool: was the object present and callable
    str: more information and error messages
    """
    try:
        themodule =importlib.import_module(package_name,package=directory)
    except ModuleNotFoundError:
        return False, f'The  code file {package_name} does not seem to be present'
    except ImportError as e:
        return False, e

    try:
        if not hasattr(themodule,funcname):
            return False, f'Code for {funcname} is missing from your file.'
        else:
            thefunc=getattr( themodule,funcname)
            if not callable (thefunc):
                return False, (f'{funcname} is present but not callable '
                            '- i.e. not an class or function'
                           )
                
            else:
                return True, f'function/class {funcname} is present and callable.\n'
    except:
        return False, 'Unexpected problems interrogating your code'



        