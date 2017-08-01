import os, socket, json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 7412                    # TALK if K == 1< == 2

if __name__ == "__main__":

    # 1. CREATE A SOCKET
    try:
        udpClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as err:
        print("FAILED TO CREATE A SOCK: {}".format(err))
    else:
        print("Created a socket: {}".format(udpClientSock.__str__()))

    # 2. CONNECT TO SERVER
    try:
        udpClientSock.connect((HOST, PORT))
    except:
        print("FAILED TO CONNECT TO SERVER: {}".format(err))
    else:
        print("Connected to IP {} on Port {}".format(HOST, PORT))

    # 3. COMMUNICATE WITH SERVER
    while True:
        thingsToSend = [1337, '31337', ['this','is','a','list'], tuple(('a','tuple')), {1:'1',2:'4',3:'6',4:'8',8:'otso otso',42:'Dictionary'}]
        menuChoice = input("What do you want to send to the server?\n1. Text\n2. JSON Strings\n'CLOSE' to shutdown\n")

        ## 3.1. TEXT
        if menuChoice == '1' or menuChoice == '1.' or menuChoice.upper() == 'ONE' or menuChoice == 1:
            userData = input("What text do you want to send to the server?\n")

            try:
                udpClientSock.sendto('1'.encode(), (HOST, PORT))
                udpClientSock.sendto(userData.encode(), (HOST, PORT))
            except Exception as err:
                print("FAILED TO SEND USER DATA TO SERVER: {}".format(err))
            else:
                print("Successfuly sent {} to server.".format(userData))

        ## 3.2. JSON STRING
        elif menuChoice == '2' or menuChoice == '2.' or menuChoice.upper() == 'TWO' or menuChoice == 2:
            print("What would you like to send?\n")

            for num, thing in enumerate(thingsToSend):
                print("{}:\t{}".format(num, thing))

            jsonMenuChoice = input("Which of these would you like to send? ")

            # Create the JSON string
            try:
                jsonThingToSend = json.dumps(thingsToSend[int(jsonMenuChoice)])
            except:
                print("Invalid selection")
            else:
#                print("Sending JSON string?") # PLACEHOLDER

                # Send the JSON string
                try:
#                    print("Sending a '2'") # DEBUGGING
                    udpClientSock.sendto('2'.encode(), (HOST, PORT))
#                    print("Sending the JSON string") # DEBUGGING
                    udpClientSock.sendto(jsonThingToSend.encode(), (HOST, PORT))
#                    print("JSON string sent") # DEBUGGING
                except Exception as err:
                    print("FAILED TO SEND JSON STRING TO SERVER: {}".format(err))
                else:
                    print('Successfully transmitted JSON string to server.')


        ## 3.N. CLOSE... "CLOSE", empty, or merely a carriage return
        elif (0 < menuChoice.count('CLOSE') or 0 == menuChoice.__len__() or menuChoice == '\n'):
            print("Received shutdown command. Sending shutdown command to server.")
            udpClientSock.sendto('CLOSE'.encode(), (HOST, PORT))
            break

        ## 3.DEFAULT.
        else:
            print("Invalid selection. Try again.")
            

    # 4. SHUTDOWN CONNECTION
    try:
        udpClientSock.close()
    except Exception as err:
        print("FAILED TO CLOSE UDP CLIENT SOCKET?! {}".format(err))
    else:
        print("Closed socket {}".format(udpClientSock.__str__()))

