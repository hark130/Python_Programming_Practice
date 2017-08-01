import os

class Error(Exception):
    """Base error class"""
    pass

class lofError(Error):
    """Exception for list_o_files()

    Attributes:
        message - string formatted explanation
    """
    def __init__(self, message):
        self.message = message




'''
# Purpose: Return a numbered listing of files from dir as a dictionary
# Input: dir is a pathname
# Return: 
#       Success - A dictionary of numbered files starting at 1
#       Failure - Will raise a lofError exception
'''     
def list_o_files(dir):
    retVal = {}

    if isinstance(dir, str):
        if 0 < dir.__len__():
            if os.path.exists(dir) and os.path.isdir(dir):
                for i, file in enumerate(os.listdir(dir)):
                    if os.path.isfile(os.path.join(dir, file)):
                        retVal.update({str(retVal.__len__() + 1):file})
            else:
                retVal.update({-3:'FAIL: Bad dir'}) 
                if not os.path.exists(dir):
                    raise lofError('FAIL: This does not exist')
                elif not os.path.isdir(dir):
                    raise lofError('FAIL: This is not a directory')
                else:
                    raise lofError('FAIL: Bad dir')
        else:
            retVal.update({-2:'FAIL: Empty dirname'})
            raise lofError('FAIL: Empty dirname')
    else:
        retVal.update({-1:'FAIL: Not a string'})
        raise lofError('FAIL: Not a string')

    return retVal