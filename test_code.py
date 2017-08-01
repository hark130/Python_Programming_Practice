from TCP_File_Server_v1 import list_o_files as list_o_files
from TCP_File_Server_v1 import lofError as lofError
import os

returnValue = []

if __name__ == "__main__":

	# Test #1
	path1 = os.getcwd()
	try:
		returnValue = list_o_files(path1)
	except lofError as err:
		print("TEST #1:\tFailed... {}".format(err.message))
	else:
		print("TEST #1:\tPass")
#		print("Return Value {} == {}".format(path1, returnValue))


	# Test #2
	path2 = os.path.join('C:\\', 'Temp', 'Filewalk Practice')
	try:
		returnValue = list_o_files(path2)
	except lofError as err:
		print("TEST #2:\tFailed... {}".format(err.message))
	else:
		print("TEST #2:\tPass")
#		print("Return Value {} == {}".format(path2, returnValue))

	# Test #3
	path3 = 'C:\\Not_There'
	try:
		returnValue = list_o_files(path3)
	except lofError as err:
		print("TEST #2:\tFailed... {}".format(err.message))
	else:
		print("TEST #2:\tPass")
#		print("Return Value {} == {}".format(path3, returnValue))

	# Test #4
	path4 = os.path.join('C:\\', 'Temp', 'Filewalk Practice', 'File0_2.zip')
	try:
		returnValue = list_o_files(path4)
	except lofError as err:
		print("TEST #4:\tFailed... {}".format(err.message))
	else:
		print("TEST #4:\tPass")
#		print("Return Value {} == {}".format(path4, returnValue))

	# Test #5
	path5 = os.path.join('C:\\', 'Temp', 'Filewalk Practice', 'EmptyDir')
	try:
		returnValue = list_o_files(path5)
	except lofError as err:
		print("TEST #5:\tFailed... {}".format(err.message))
	else:
		print("TEST #5:\tPass")
#		print("Return Value {} == {}".format(path5, returnValue))

	# Test #6
	path6 = os.path.join('')
	try:
		returnValue = list_o_files(path6)
	except lofError as err:
		print("TEST #6:\tFailed... {}".format(err.message))
	else:
		print("TEST #6:\tPass")
#		print("Return Value {} == {}".format(path6, returnValue))

	# Test #7
	myList = [1,2,3]
	path7 = myList
	try:
		returnValue = list_o_files(path7)
	except lofError as err:
		print("TEST #7:\tFailed... {}".format(err.message))
	else:
		print("TEST #7:\tPass")
#		print("Return Value {} == {}".format(path7, returnValue))