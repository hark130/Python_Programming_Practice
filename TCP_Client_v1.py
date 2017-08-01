import os, socket, sys, pickle

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1337
BYTES = 1024
CLIENT_RECV_FILES = os.path.join(os.getcwd(), 'Client_Files', 'Receive')
CLIENT_SEND_FILES = os.path.join(os.getcwd(), 'Client_Files', 'Send')
SELECTION1 = [1,'1','1.','Download','Download files from server','1. Download files from server']
SELECTION2 = [2,'2','2.','Upload','Upload a file','Upload a file to the server','2. Upload a file to the server']
SELECTION3 = [3,'3','3.','Reverse word','Reverse a word','3. Reverse a word']
SELECTION4 = [4,'4','4.','Reverse sentence','Reverse a sentence','4. Reverse a sentence']
SELECTION5 = [5,'5','5.','Echo number','Echo a number','5. Echo a number']

if __name__ == "__main__":

    os.system('cls')

    ### VERIFY STATE OF FILES ###########################
    # 1. CHECK FOR FOLDERS
    if not os.path.exists(CLIENT_SEND_FILES):
        try:
            os.makedirs(CLIENT_SEND_FILES)
        except Exception as err:
            print("Send directory creation error:  {}".format(err))

    if not os.path.exists(CLIENT_RECV_FILES):
        try:
            os.makedirs(CLIENT_RECV_FILES)
        except Exception as err:
            print("Recv directory creation error:  {}".format(err))
    #####################################################

    ### CONNECT TO THE SERVER ###########################
    # 1. CREATE THE SOCKET 
    try:
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as err:
        print("SOCKET OPENING ERROR:  {}".format(err))
        sys.exit()
    else:
        print("SOCKET OPEN:  {}".format(clientSock.__str__()))

    # 2. CONNECT TO SERVER
    try:
        clientSock.connect((HOST, PORT))
    except Exception as err:
        print("SOCKET CONNECTION ERRROR:  {}".format(err))
        sys.exit()
    else:
        print("CONNECTED TO {} on port {}".format(HOST, PORT))

    while True:
#        print("Receiving from server") # DEBUGGING
        incomingData = clientSock.recv(BYTES)
        print("Server Menu:\n{}".format(incomingData.decode('utf-8')))

        try:
            outgoingData = input("What is your response?\n'CLOSE' to quit.\n")
        except Exception as err:
            print("USER INPUT ERRROR:  {}".format(err))
            clientSock.close()
            sys.exit()
        else:
            if -1 < outgoingData.find('CLOSE'):
                clientSock.close()
                break
            else:
                if SELECTION1.count(outgoingData) == 1:
                    # Answer 1
                    ## Step A - Answer the server
                    clientSock.sendall(outgoingData.encode())            
                    ## Step B - Receive list of files
                    rawList = clientSock.recv(BYTES)

                    try:
                        fileList = pickle.loads(rawList)
                        formattedFileList = ''
                    except pickle.PickleError as err:
                        print("PICKLE PROBLEM:  {}".format(err))
                    except Exception as err:
                        print("FILE LIST DOWNLOAD ERROR:  {}".format(err))
                    else:
                        for fileNum in fileList.keys():
                            formattedFileList = formattedFileList + str(fileNum) + ' ' + str(fileList[fileNum]) + '\n'
                        print("Raw File List:\n\t{}".format(fileList)) # DEBUGGING
                        print("Formatted File List:\n{}".format(formattedFileList))
    #                    print(formattedFileList)
                        fileNo = input("Which file do you want to download?  ")
                        clientSock.sendall(fileNo.encode())
                        incomingFileName = os.path.join(CLIENT_RECV_FILES, fileList[fileNo])
                        incomingFile = open(incomingFileName, 'wb')
                        incomingFilePart = clientSock.recv(BYTES)
                        partNo = 1

                        while incomingFilePart:
                            print("Receiving Part #{}".format(partNo))
                            incomingFile.write(incomingFilePart)
                            partNo += 1
                            incomingFilePart = clientSock.recv(BYTES)

                        print("Done Receiving {} Parts".format(partNo-1))
                        incomingFile.close()
                        break

                elif SELECTION2.count(outgoingData) == 1:
                    print("Not yet implemented.")
                    clientSock.close()
                    break   

                elif SELECTION3.count(outgoingData) == 1:
                    # Answer 3
                    ## Step A - Answer the server
                    clientSock.sendall(outgoingData.encode())   

                    ## Step B - Read a word from user
                    try:
                        userString = input("Enter a word for the server to reverse:\n")
                    except Exception as err:
                        print("ERROR READING WORD: {}".format(err))
                    else:
                        print("Read string:\t{}".format(userString))

                    ## Step C - Send a word
                    try:
                        clientSock.send(userString.encode())
                    except Exception as err:
                        print("ERROR SENDING WORD: {}".format(err))

                    ## Step D - Receive the reversed word
                    try:
                        reversedString = clientSock.recv(BYTES)
                    except Exception as err:
                        print("ERROR RECEIVING REVERSED WORD: {}".format(err))

                    print("Server returned the following word:\n{}\n".format(reversedString.decode('utf-8')))

                elif SELECTION4.count(outgoingData) == 1:
                    # Answer 4
                    ## Step A - Answer the server
                    clientSock.sendall(outgoingData.encode())   

                    ## Step B - Read a sentence from user
                    try:
                        userSentence = input("Enter a sentence for the server to reverse:\n")
                    except Exception as err:
                        print("ERROR READING SENTENCE: {}".format(err))
                    else:
                        print("Read sentence:\t{}".format(userSentence))

                    ## Step C - Send a sentence
                    try:
                        clientSock.send(userSentence.encode())
                    except Exception as err:
                        print("ERROR SENDING SENTENCE: {}".format(err))

                    ## Step D - Receive the reversed sentence
                    try:
                        reversedSentence = clientSock.recv(BYTES)
                    except Exception as err:
                        print("ERROR RECEIVING REVERSED SENTENCE: {}".format(err))

                    print("Server returned the following word:\n{}\n".format(reversedSentence.decode('utf-8')))

                elif SELECTION5.count(outgoingData) == 1:
                    # Answer 5
                    ## Step A - Answer the server
                    try:
                        clientSock.sendall(outgoingData.encode())   
                    except Exception as err:
                        print("ERROR SENDING MENU SELECTION TO SERVER:  {}".format(err))
                        sys.exit()
                    else:
                        print("Sent menu choice to server")

                    ## Step B - Read the random number from the server
                    try:
                        data = clientSock.recv(BYTES)   
                    except Exception as err:
                        print("ERROR RECEIVING RANDOM NUMBER FROM SERVER:  {}".format(err))
                        sys.exit()
                    else:
                        print("Received data from server:  {}".format(data))

                    ## Step C - Convert the input from network to host byte ordering
                    try:
#                        serverNum = ntohl(data)
                        serverNum = bytes(data)
                    except Exception as err:
#                        print("ERROR CONVERTING INPUT FROM SERVER FROM NETWORK BYTE ORDERING TO HOST BYTE ORDERING:  {}".format(err))
                        print("ERROR CONVERTING INPUT FROM SERVER:  {}".format(err))
                        sys.exit()
                    else:
                        print("Converted {} into {}".format(data, serverNum))

                    ## Step D - Get input from user
                    print("Server sent {}".format(serverNum))             
                    userInput = input("Type that number to send it back to the server")

                    ## Step E - Convert the input to an int
                    try:
                        userAnswer = int(userInput)
                    except Exception as err:
                        print("ERROR CONVERTING USER INPUT STRING TO INTEGER:  {}".format(err))
                        sys.exit()
                    else:
                        print("Successfully converted {}({}) into {}({})"\
                            .format(userInput, type(userInput), userAnswer, type(userAnswer)))      

                    ## Step F - Convert the int into network byte ordering
                    try:
#                        userResponse = htonl(bytes(userAnswer))
                        userResponse = bytes(userAnswer)
                    except Exception as err:
#                        print("ERROR CONVERTING USER INPUT FROM HOST BYTE ORDERING TO NETWORK BYTE ORDERING:  {}".format(err))
                        print("ERROR CONVERTING USER INPUT:  {}".format(err))
                        sys.exit()
                    else:
                        print("Converted {} into {}".format(userAnswer, userResponse))      

                    ## Step G - Send user response back to server
                    try:
                        clientSock.sendall(userResponse)
                    except Exception as err:
                        print("ERROR SENDING CONVERTED USER RESPONSE TO SERVER:  {}".format(err))
                        sys.exit()
                    else:
                        print("Successfully sent user response back to server")      

                else:
                    print("Invalid selection.")
                    clientSock.close()
                    break                    


    # N. TEAR IT ALL DOWN
    try:
        clientSock.close()
    except Exception as err:
        print("SOCKET CLOSE ERROR?!  {}".format(err))
    else:
        print("SOCKET CLOSED")

    ### Just testing
    # while True:
    #     try:
    #         data = input("Send data.  'CLOSE' to quit.\n")
    #     except Exception as err:
    #         print("USER INPUT ERRROR:  {}".format(err))
    #         clientSock.close()
    #         break
    #     else:
    #         if -1 < data.find('CLOSE'):
    #             clientSock.close()
    #             break
    #         else:
    #             clientSock.sendall(data.encode())
    #####################################################
