import os, sys, socket, json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 7412					# TALK if K == 1< == 2
clientList = []

if __name__ == "__main__":

	# 1. CREATE A SOCKET
	try:
		udpServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except Exception as err:
		print("FAILED TO CREATE A SOCK: {}".format(err))
		sys.exit()
	else:
		print("Created a socket: {}".format(udpServerSock.__str__()))

	# 2. BIND THE SOCKET
	try:
		udpServerSock.bind((HOST, PORT))
	except Exception as err:
		print("FAILED TO BIND TO A PORT: {}".format(err))
		sys.exit()
	else:
		print("Bound to Port {} on IP {}".format(PORT, HOST))

	# 3. LISTEN FOR client 			# UDP DOESN'T LISTEN FOR CLIENTS LIKE TCP DOES
	# try:
	# 	udpServerSock.listen(0)
	# except Exception as err:
	# 	print("FAILED TO PUT SOCKET INTO LISTEN MODE: {}".format(err))
	# 	sys.exit()
	# else:
	# 	print("Listening for clients on Port {}".format(PORT))

	# 4. COMMUNICATE WITH CLIENT
	while True:
		clientData, clientIP = udpServerSock.recvfrom(1024) # Contains user selection
		
		# Add new clients to the list
		if 0 == clientList.count(clientIP):
			clientList.append(clientIP)
			print("Accepted connection from new client: {}".format(clientIP))

		# Decode the bytes object received from the server socket
		try:
			incomingData = clientData.decode('utf-8')
		except Exception as err:
			print("ERROR DECODING INCOMING MENU SELECTION: {}".format(err))
		else:
			# Close on empty data
			if not incomingData:
				print("Incoming data blank. Shutting down server.")
				break

			# Close on 'CLOSE' message from client
			if 0 < incomingData.count('CLOSE'):
				print("Received shutdown command from client. Shutting down server.")
				break

			# DEBUGGING
			print("Received Menu Selection of {} from {}".format(incomingData, clientIP))

			# Switch on client intention
			## '1' == Send text
			if incomingData == '1':
				clientData, clientIP2 = udpServerSock.recvfrom(1024) # Contains user text

				if clientIP == clientIP2:
					try:
						incomingData = clientData.decode('utf-8')
					except Exception as err:
						print("ERROR DECODING INCOMING TEXT: {}".format(err))
					else:
						print("Received data from {}: {}".format(clientIP, incomingData))
				else:
					print("Communication interrupted by another client.\nExpecting: {}\nReceived: {}".format(clientIP, clientIP2))

			## '2' == Send JSON string
			elif incomingData == '2':
				print("Receiving JSON string?") # PLACEHOLDER
				clientData, clientIP2 = udpServerSock.recvfrom(1024) # Contains JSON string
				print("Got some data from {}".format(clientIP2)) # DEBUGGING

				if clientIP == clientIP2:
					try:
#						print("Attempting to decode incoming JSON string...") # DEBUGGING
						incomingData = json.loads(clientData.decode('utf-8'))
#						print("Received data from {}: {}!!!!!".format(clientIP, incomingData)) # DEBUGGING
					except Exception as err:
						print("ERROR DECODING INCOMING JSON STRING: {}".format(err))
					else:
						print("Received data from {}: {} (Type: {})".format(clientIP, incomingData, type(incomingData)))
				else:
					print("Communication interrupted by another client.\nExpecting: {}\nReceived: {}".format(clientIP, clientIP2))


	# 5. CLOSE SOCKET
	try:
		udpServerSock.close()
	except Exception as err:
		print("FAILED TO CLOSE UDP SERVER SOCKET?! {}".format(err))
	else:
		print("Closed socket {}".format(udpServerSock.__str__()))



