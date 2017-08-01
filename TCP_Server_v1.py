from TCP_File_Server_v1 import list_o_files as list_o_files
import os, socket, pickle, sys, random

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1337
BYTES = 1024
SERVER_RECV_FILES = os.path.join(os.getcwd(), 'Server_Files', 'Receive')
SERVER_SEND_FILES = os.path.join(os.getcwd(), 'Server_Files', 'Send')
MENU = '\n' + \
    "WELCOME\n" + \
    "What would you like to do?\n" + \
    "1. Download files from server\n" + \
    "2. Upload files to server\n" + \
    "3. Reverse a word\n" + \
    "4. Reverse a sentence\n" + \
    "5. Echo a number\n"
SELECTION1 = [1,'1','1.','Download','Download files from server','1. Download files from server']
SELECTION2 = [2,'2','2.','Upload','Upload a file','Upload a file to the server','2. Upload a file to the server']
SELECTION3 = [3,'3','3.','Reverse word','Reverse a word','3. Reverse a word']
SELECTION4 = [4,'4','4.','Reverse sentence','Reverse a sentence','4. Reverse a sentence']
SELECTION5 = [5,'5','5.','Echo number','Echo a number','5. Echo a number']

# RAND_UPPER = sys.maxsize # Received overflow error:  "python int too long to convert to C unsigned long"
RAND_UPPER = 2147483647
# RAND_LOWER = -(sys.maxsize - 1) # The network byte ordering functions don't like negative values
RAND_LOWER = 0

if __name__ == "__main__":

    os.system('cls')

    ### VERIFY STATE OF FILES ###########################
    # 1. CHECK FOR FOLDERS
    if not os.path.exists(SERVER_SEND_FILES):
        try:
            os.makedirs(SERVER_SEND_FILES)
        except Exception as err:
            print("Send directory creation error:  {}".format(err))

    if not os.path.exists(SERVER_RECV_FILES):
        try:
            os.makedirs(SERVER_RECV_FILES)
        except Exception as err:
            print("Recv directory creation error:  {}".format(err))
    #####################################################

    ### LISTEN FOR CLIENTS ##############################
    # 1. CREATE THE SOCKET
    try:
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as err:
        print("SOCKET OPENING ERROR:  {}".format(err))
    else:
        print("SOCKET OPEN:  {}".format(serverSock.__str__()))

    # 2. BIND THE SOCKET
    try:
        serverSock.bind((HOST, PORT))
    except Exception as err:
        print("SOCKET BIND ERROR:  {}".format(err))
    else:
        print("SOCKET BOUND:\n\tHost:  {}\n\tPort:  {}".format(HOST, PORT))

    # 3. LISTEN FOR CLIENTS
    try:
        serverSock.listen(10)
    except Exception as err:
        print("SOCKET LISTEN ERROR:  {}".format(err))
    else:
        print("SOCKET NOW LISTENING...")

    # 4. ACCEPT CLIENTS
    try:
        clientSock, clientAddr = serverSock.accept()
    except Exception as err:
        print("SOCKET ACCEPT ERROR:  {}".format(err))
    else:
        print("SOCKET ACCEPTED CONNECTION FROM {}".format(clientAddr))

        with clientSock:
            while True:
                clientSock.sendall(MENU.encode())
                data = clientSock.recv(BYTES)
                
                if not data:
                    break
                else:
                    userInput = data.decode('utf-8')
                    print("Received:  {}".format(userInput))

                    # OPTION 1:  DOWNLOAD FILES FROM THE SERVER
                    if SELECTION1.count(userInput) == 1:
                        # Invoke list_o_files()
                        try:
                            serverFileDict = list_o_files(SERVER_SEND_FILES)
                        except Exception as err:
                            print("ERROR list_o_files():  {}".format(err))
                        else:
                            print("List of available files on server:\n{}".format(serverFileDict)) # DEBUGGING

                        # Pickle the dictionary
                        try:
                            if serverFileDict.__len__():
                                packedSFL = pickle.dumps(serverFileDict)
                            else:
                                packedSFL = pickle.dumps("No files to download")
                        except pickle.PickleError as err:
                            print("PICKLE PROBLEM:  {}".format(err))
                        except Exception as err:
                            print("FILE LIST DOWNLOAD ERROR:  {}".format(err))

                        # Send over the list
                        try:
                            clientSock.sendall(packedSFL)
                        except Exception as err:
                            print("PICKLED TRANSMIT PROBLEM:  {}".format(err))
                        else:
                            print("Pickled File List Sent to {}".format(clientAddr))

                        # What file to send?
                        data = clientSock.recv(BYTES)
                        userInput = data.decode('utf-8')

                        try:
                            fileToSend = open(os.path.join(SERVER_SEND_FILES, serverFileDict[userInput]), 'rb')
                        except KeyError as err:
                            print("KEY ERROR:  {}".format(err))
                        except Exception as err:
                            print("FILE NUMBER OPEN ERROR:  {}".format(err))
                        else:
                            print("SENDING FILE!") # Send over the file
                            filePart = fileToSend.read(BYTES)
                            partNo = 1

                            while filePart:
                                print("Sending Part #{}".format(partNo))
                                clientSock.send(filePart)
                                partNo += 1
                                filePart = fileToSend.read(BYTES)

                            # Done sending
                            print("Done Sending {} Parts".format(partNo))
                            clientSock.shutdown(socket.SHUT_WR)
                            break
                    # OPTION 2:  UPLOAD A FILE
                    elif SELECTION2.count(userInput) == 1:
                        # What file to upload?
                        try:
                            rawFileName = clientSock.recv(BYTES)
                            fileName = rawFileName.decode('utf-8')
                        except Exception as err:
                            print("ERROR RECEIVING INCOMING FILENAME:  {}".format(err))
                            sys.exit()
                        else:
                            print("Preparing to receive filename:  {}".format(fileName))

                        # Receive the file
                        partNo = 1
                        rawData = partNo
                        while rawData:
                            try:
                                # CURRENTLY IGNORES UPLOADED DATA
                                # SHOULD BE IMPLEMENTED LATER   
                                rawData = clientSock.recv(BYTES)
                            except Exception as err:
                                print("FILE UPLOAD ERROR:  {}".format(err))
                                sys.exit()
                            else:
                                print("Received Filename {} Part #{}".format(fileName, partNo))
                                partNo += 1                        

                    # OPTION 3:  REVERSE A STRING
                    elif SELECTION3.count(userInput) == 1:
                        # What string to reverse?
                        data = clientSock.recv(BYTES)
                        userInput = data.decode('utf-8')

                        reversedWord = userInput[::-1]

                        print("Reversed word is:\t{}".format(reversedWord))
                        clientSock.sendall(reversedWord.encode())

                    # OPTION 4:  REVERSE A SENTENCE
                    elif SELECTION4.count(userInput) == 1:
                        # What sentence to reverse?
                        data = clientSock.recv(BYTES)
                        userInput = data.decode('utf-8')

                        # Reverse the sentence
                        reversedSentence = ''
                        for word in userInput.split(' '):
                            reversedSentence = reversedSentence + word[::-1] + ' '
                        # Strip off the trailing space

                        print("Reversed sentence is:\t{}".format(reversedSentence))

                        clientSock.sendall(reversedSentence.encode())

                    # OPTION 5:  ECHO A NUMBER
                    elif SELECTION5.count(userInput) == 1:
                        # Randomize a number for the client to echo back
                        try:
                            randNum = random.randrange(RAND_LOWER, RAND_UPPER)
                        except Exception as err:
                            print("RANDOMIZATION ERROR:  {}".format(err))
                            sys.exit()
                        else:
                            print("Server randomized number:  {}".format(randNum))

                        # Send the number
                        try:
#                            clientSock.sendall(bytes(socket.htonl(randNum)))
                            clientSock.sendall(bytes(randNum))
                        except Exception as err:
#                            print("ERROR SENDING RANDOM NUMBER IN NETWORK BYTE ORDER:  {}".format(err))
                            print("ERROR SENDING RANDOM NUMBER:  {}".format(err))
                            sys.exit()
                        else:
#                            print("Successfully sent {} to client in network byte order".format(randNum))
                            print("Successfully sent {} to client".format(randNum))

                        # Receive the response
                        try:
                            data = clientSock.recv(BYTES)
                            userInput = data.decode('int')
                        except Exception as err:
                            print("ERROR RECEIVING RANDOM NUMBER ECHO FROM CLIENT:  {}".format(err))
                            sys.exit()
                        else:
                            print("Received random number echo from client:  {}".format(data))

                        # Convert response back to host byte ordering
                        # try:
                        #     userInput = socket.ntohl(data)
                        # except Exception as err:
                        #     print("ERROR CONVERTING RANDOM NUMBER ECHO FROM CLIENT INTO HOST BYTE ORDERING:  {}".format(err))
                        # else:
                        #     print("Successfully converted client response to:  {}".format(userInput))

                        # Check the response
                        if userInput is randNum:
                            print("Client successfully echoed back the random number.")
                        else:
                            print("FAIL!\nReceived:  {}\nExpected:  {}".format(userInput, randNum))

                    # BAD OPTION:  Fall through
                    else:
                        print("Why did they choose that?")
                        break                    


    # N. TEAR IT ALL DOWN
    try:
        serverSock.close()
    except Exception as err:
        print("SOCKET CLOSE ERROR?!  {}".format(err))
    else:
        print("SOCKET CLOSED")

    #####################################################