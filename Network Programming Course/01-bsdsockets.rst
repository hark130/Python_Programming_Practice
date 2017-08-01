:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
Concepts Overview  
====================================

- Sockets

- BSD Socket API

- TCP Client Call Sequence

- TCP Server Call Sequence

- TCP and sockets

- UDP Client Call Sequence

- UDP Server Call Sequence

- UDP and sockets


#######################

====================================
Sockets Overview
====================================

Sockets allow for Inter-Process Communication (IPC) 

We will be using the BSD Socket API for networking

Knowing BSD sockets will provide a foundation to do networking in almost any language/environment

  - Even Windows' Winsock library still follows the call pattern, even if Microsoft makes their function calls take a dozen more parameters

#######################

====================================
BSD Sockets
====================================

In order to connect to another host, you need to make a socket. To do so, you need to know 2 things: 

  - What type of address should I use?
  - How is the data being transmitted?

The Address family
  - AF_INET
  - AF_INET6

The socket type
  - DATAGRAM
  - STREAM
  - RAW (Used for raw access to the wire)


DATAGRAM and STREAM sockets handle layers 1-4 for you. You simply supply the data on top (typically layer 7 data)

RAW sockets give you raw access to the wire. You are responsible for correctly structuring all layers
 

#######################


====================================
Ports
====================================

Ports are how processes get access to the network.

Port numbers < 1024 are considered "privleged" ports
  
  - Processes must have root/admin privileges to bind to these ports

  - They are typically reserved for servers. IANA maintains the list of well known ports (see references)

Ports >= 1024 can be used by anyone

If you do not bind to a port as a TCP client/UDP sender, you will get a random high number port automatically assigned to your process. This is called an "ephemeral port" 

#######################



====================================
TCP Client call sequence
====================================

socket() – Get a socket descriptor

bind() – Specify SOURCE port (Optional) 

connect() – Connect to destination IP/PORT

send()/recv() – Data transfer

close() – Close the socket 

#######################

====================================
TCP Server call sequence
====================================

socket() – Get a socket descriptor

bind() – Specify SOURCE port to listen on 

listen() – Wait for a client to connect on the port

accept() – Returns a NEW socket to communicate with a single client (more on this on the next slide)

send/recv() – Data Transfer

close() – Close the socket

#######################

====================================
Tale of two sockets
====================================

TCP Server code will deal with TWO (or more) sockets

  - The first socket is created by socket() and is used to LISTEN
  - The other sockets are returned by accept() after a client connects to the listening socket. This new socket is used for data transfer to that specific client
  - Accept() returns two values, the socket, and the IP of the other side.

Keep in mind

  - Calls to accept() will NOT alter the LISTENING socket
  - By default, accept() will block until a connection is received

#######################

====================================
Connections
====================================

A CONNECTION is a unique combination of
  - Client IP
  - Client Port
  - Server IP
  - Server Port

If any one of these changes, it must be a different connection

A connection is established between a TCP client and TCP server when the client uses connect() to establish a connection to a TCP server listening. The result of that connection is the socket returned by accept()


#######################

====================================
UDP Call Sequence
====================================

socket() – Get a socket descriptor

bind() – Specify SOURCE port (Optional) 

sendto()/recvfrom() – Data transfer*

close() – Close the socket


#######################

====================================
UDP: Client vs Server
====================================

There is ONE socket and UDP is connectionless 
  - sendto() and recvfrom() share the socket
  - The source of received data must be tracked manually
  - There is no concept of a connection

The concept of client and server gets muddied. 

It's usually easier to think of them as "Senders" and "Recievers"
  - If you want to recieve traffic, you need bind to a port. 

#######################

====================================
sendto() and recvfrom()
====================================

recvfrom() returns TWO values, A tuple of clients ip/port and the data.

sendto() takes TWO arguments, dest ip/port and data

Use the clientIP from recvfrom() in the call to sendto() to return data to that host

#######################


====================================
setsockopt() and getsockopt()
====================================

Using socket options gives you some advanced options for sockets to do interesting things.

Options have a LEVEL, OPTION NAME, and a VALUE
  
  - LEVEL can be the entire socket (socket.SOL_SOCKET) or a specific protocol (socket.IPPROTO_IPV6) 

  - The LEVEL specified determines what OPTION NAME's are available to be set
  
  - VALUES are assigned to the specified OPTION NAME

Unfortunately, options are scattered all over the place in documentation. Man pages are currently the best source.

Example:

To prevent the "Address is use" errors when restarting labs, set the following option:

  mysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  SOL_ means 'Socket Option Level'


#######################


====================================
Struct Module
====================================

Struct allows you to pack values into specified data types/sizes and endianess. Packed data is represented by a string of hex bytes. 

Struct will also unpack data from the hex string string and provide you a tuple of the values.

Packing is used to prepare structured binary data such as a protocol header or a message format. This data can then be referenced like a struct in C, or sent across the wire. 

It uses a format string and variable arguments (like print or printf in C) 


::

  >>> from struct import *
  >>> pack('hhl', 1, 2, 3)
  '\x00\x01\x00\x02\x00\x00\x00\x03'
  >>> unpack('hhl', '\x00\x01\x00\x02\x00\x00\x00\x03')
  (1, 2, 3)

#######################


====================================
JSON Module
====================================

JSON = JavaScript Object Notation. It's a series of key-value pairs. The key-value pairs may be nested.

json.dumps() creates a JSON string from the data passed in. It looks like a Python dictionary with quotes around it

::

  >>> import json
  >>> data = {'foo':1, 'bar':'qwerty'}
  >>> json.dumps(data)
  '{"foo": 1, "bar": "qwerty"}'
  >>> data
  {'foo': 1, 'bar': 'qwerty'}
  >>> 


json.loads() takes a JSON String and  makes it onto a dictionary

::

  >>> jsonstr = json.dumps(data)
  >>> type(json.loads(jsonstr))
  <type 'dict'>

#######################

====================================
Debugging
====================================

Wireshark is your networking debugger. If your code does not work, the first thing you should do is identify the traffic in Wireshark. 

Wireshark will indicate if your packet is malformed, incorrectly sized, has bogus headers, and other things. Look at the Info column in the traffic window, and the individual layers in the pakcet window. 

Walk through each byte of each header and compare it to what you THINK you put there. If your code is messy, this can be a chore to isolate. 

Common errors include:

  Incorrect length fields
  Transposed bytes
  Data in fields are of incorrect widths

Invalid checksums can be caused by almost any error, including the ones above. 

#######################


====================================
References
====================================

PyDocs: 

  https://docs.python.org/2/library/socket.html

  https://docs.python.org/2.7/library/json.html

  https://docs.python.org/2/library/struct.html


Man Pages:

  http://man7.org/linux/man-pages/man7/socket.7.html

  http://man7.org/linux/man-pages/man7/ip.7.html

  http://man7.org/linux/man-pages/man7/ipv6.7.html


Other:

  http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml


#######################

====================================
LABS
====================================

The following slides contain several labs for you to do. If you finish early, move on to the bonus labs.

Each lab is to be in it's own file, even if it builds on a previous lab. This applies to all labs in this class@

You may arbitrarily choose the port numbers for the below labs

Write your code neatly and with comments


#######################



====================================
LAB 1A
====================================

Write a TCP server that recieves a string, reverses order of the words, and sends it back to the client. 

Write a TCP client to connect to and print the response


#######################

====================================
LAB 1B
====================================

Write a UDP sender that takes a dictionary, turns it into a JSON string, and sends it to a listener. 

Write the UDP listener to recieve the JSON string and turns it back into a dictionary.

#######################


====================================
LAB 1C
====================================

Write a UDP reciever that recieves a string, orders the words from longest to shortest in a new string, and sends that new string it to the source port + 1 

Write a UDP client that sends the initial string

Write a second UDP client to recieve the reordered string and print it to the terminal


#######################


====================================
LAB 1D
====================================

NOTE: This lab has a Q&A aspect to it. 

You will be using struct.pack() to simulate a binary protocol.

Pack the values (1, 2, -3, -4) as the following data types (unsigned short, unsigned int, signed short, signed int)

::  

  1 as an unsigned short 
  2 as an unsigned int
  -3 as a signed short 
  -4 as a signed int


Write a TCP client that packs those values, sends the packed string to a server.

Write a TCP server that recieves the string, unpacks it using little endian and prints it, then unpacks it again using big endian and prints it.

Q1) Which unpacked are the same? 

Q2) Why are they the same? Does it matter what Endianess your system is using?

Q3) Assume I repeat this lab with a client on a little-endian architecture, and the server on a big-endian architechture. How will the files change? Why?

Q4) How can I be sure that the data I send is properly recieved on any endian machine?


#######################


====================================
LAB 1E
====================================

Use: https://en.wikipedia.org/wiki/Action_Message_Format

Implement a TCP client and server that will pack and unpack an ACTION MESSAGE header-type-structure. 

Create a struct.pack/unpack string using the header description

You may choose arbitrary values, but they must be of the correct type (UTF-8 is a string, integers are numeric)

The type field in the header contains a mnemonic:

  uimsbg = Unsigned Integer, transmitted Most Significant Bit First
  simsbg = Signed Integer, transmitted Most Significant Bit First



#######################




====================================
LAB 1 BONUS
====================================

Make a raw socket that recieves the responses from a 'ping' or 'ping6' command

  Hint: socket.socket() takes an optional 3rd parameter. Pings are ICMP and ICMPv6 protocols riding on IPv4/IPv6 traffic


#######################

====================================
Concepts Review  
====================================

Sockets allow for IPC

BSD Socket API is used for networking

Function calls to make a TCP Server
  - Socket, Bind, Listen, Accept, Send/Recv, Close

Function calls to make a TCP Client
  - Socket, Connect, Send/Recv, Close

Function calls to make a UDP Server are identical to UDP Clients
  - Socket, Bind, SendTo/RecvFrom, Close

Byte order matters, NETWORK byte order is big endian, use struct module

JSON is string based. Python dictionaries convineitly can be used to store the data


====================================
Homework: ARP RFC
====================================

Let's look at RFC 826 for an example of ARP.
  -  https://tools.ietf.org/html/rfc826

Read the following sections

  - Motivations
  - Definitions
  - Packet Format
  - Packet Generation
  - Packet reception

Identify the ethernet header fields and their widths

Identify the ethernet payload (This ancient RFC calls it "packet data") fields and their widths

Why does ARP allow for certain fields to be variable width? How can you tell how long that field is?

Identify the values that should be in each of those fields you have identified

Explain which values change on between an ARP request and an ARP reply, and why they change.
  - It is more than just "fill in the address"

#######################