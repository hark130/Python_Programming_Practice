import struct
import sys


if __name__ != "__main__":
    
    def pack_a_string(someString):

        # Input validation
        if isinstance(someString, str):

            ## Build the format string
            ### Determine string length
            strlen = someString.__len__()

            ### Determine endianness
            if sys.byteorder == 'little':
                character = '<'
            elif sys.byteorder == 'big':
                character = '>'
            else:
                print("byte order is {}".format(sys.byteorder))
                raise Exception('sys.byteorder is weird')

            ### Complete the format string
            if 0 < strlen:
#                print(type(someString)) # DEBUGGING
                
                formatString = character + str(strlen) + 's'
                byteString = someString.encode()
                
                try:
                    retVal = (formatString, struct.pack(formatString, byteString))
                except struct.error as err:
                    print("Packing error:\t{}".format(err))
            else:
                retVal = ("Fail", "String is empty".encode())   
        else:
            retVal = ("Fail", "Object is not a string".encode())        
        
        return retVal                  

