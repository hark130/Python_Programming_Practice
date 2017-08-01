from Pack_Module import pack_a_string as pack_a_string
import struct

if __name__ == "__main__":
    
    # TEST 1 - Normal input
    inputString1 = "This is a normal string"
    tempFrmtStr, tempPckData = pack_a_string(inputString1)
    expectStr1 = b'This is a normal string'
    expectFrmtStr1 = "<" + str(expectStr1.__len__()) + "s"
    decodedString1 = 'default'
    
    try:
        assert(tempFrmtStr == expectFrmtStr1)
    except:
        print("FAILED TEST 1a\n{} is not equivalent to {}".format(tempFrmtStr, expectFrmtStr1))
    else:
        print("Passed Test 1a")

    try:
        assert(tempPckData == expectStr1)
    except:
        print("FAILED TEST 1b\n{} is not equivalent to {}".format(tempPckData, expectStr1))
    else:
        print("Passed Test 1b")

    # UNPACK THE RETURN VALUE
    try:  
        decodedString1 = struct.unpack(tempFrmtStr,tempPckData)
    except Exception as err:
        print("FAILED UNPACKING RETURN TUPLE:\t{}".format(err))
    else:
        print("Original string:\t{} (Type: {})".format(inputString1, type(inputString1)))
        print("Decoded return value:\t{} (Type: {})".format(decodedString1, type(decodedString1)))

    # TEST 2 - Empty string
    inputString2 = ""
    tempFrmtStr, tempPckData = pack_a_string(inputString2)
    expectStr2 = b'String is empty'
    expectFrmtStr2 = "Fail"
    decodedString2 = 'default'
    
    try:
        assert(tempFrmtStr == expectFrmtStr2)
    except:
        print("FAILED TEST 2a\n{} is not equivalent to {}".format(tempFrmtStr, expectFrmtStr2))
    else:
        print("Passed Test 2a")

    try:
        assert(tempPckData == expectStr2)
    except:
        print("FAILED TEST 2b\n{} is not equivalent to {}".format(tempPckData, expectStr2))
    else:
        print("Passed Test 2b")

    # UNPACK THE RETURN VALUE
    try:  
        decodedString2 = struct.unpack(tempFrmtStr,tempPckData)
    except Exception as err:
        print("FAILED UNPACKING RETURN TUPLE:\t{}".format(err))
    else:
        print("Original string:\t{} (Type: {})".format(inputString2, type(inputString2)))
        print("Decoded return value:\t{} (Type: {})".format(decodedString2, type(decodedString2)))


    pass

