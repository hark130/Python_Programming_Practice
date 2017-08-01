:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
Layer 4 - Transport Layer Protocols
====================================

Layer 4 handles connections between two IP addresses. 

There are two types, UDP and TCP

#######################

====================================
Layer 4 Overview  
====================================

- Introduction to TCP

- TCP Flags

- Sequence and Acknowledgements

- TCP Handshake

- TCP Teardown

- TCP State

- Traffic Control

- TCP Header

- TCP Fields

- Introduction to UDP

- Protocols using UDP

- UDP Header

- UDP Fields

- Labs


====================================
TCP
====================================

TCP is a connection oriented protocol that provides error checking and reliability of communication

Most protocols commonly used on the internet use TCP, including HTTP, SMTP, and SSH

#######################

====================================
Intro to TCP
====================================

TCP connections open with a handshake, data is transmitted, and then the connection is closed with a teardown

TCP provides reliable transfer via:
  - Correctly ordering packets recieved in arbitrary order
  - Validating received packets were not corrupt
  - Re-requesting packets that were corrupt or not recieved at all 
  - Flow and congestion control 
  - Requires positive acknowledgement before next data transmission

#######################

====================================
TCP FLAGS
====================================

TCP uses a bit field to represent flags.

NS - Nonse Sum, used to counter an old method for an attacker attempting to "hide" traffic

CWR - Congestion Window Reduced, an acknolwedgement of congestion notification (ECE)

ECE - Explicit Congestion Notification, notifies sender of network congestion, or that the remote side is ENC capable (if sent along with SYN)

URG - Urgent field is valid in this transmission

ACK - Acknowledgement field is valid. Is on almost all tranmssions except for initial SYN

PSH - Requests data be pushed to application

RST - Resets the connection

SYN - Requests a Seq No sync, should always be set

FIN - No more data to send

#######################

====================================
Sequence and Acknowledgements
====================================

Sequence numbers indicate the most recent piece of data sent

Acknowledgement numbers indicate the next byte expected 

During the initial handshake:
  - Host A randomly generates a sequence number
  - Host B will acknowledge A's seq number, and generate a random seq no of it's own
  - Host A will acknowlege B's seq number and the connection is established


#######################

====================================
Sequence and Acknowledgements
====================================

With NO DATA transmitted (e.g. keep alive packet):
  - Sequence Numbers may be re-acked until other side actually sends the data

During normal data transmission
  - Sequence numbers mark the most recent data sent. It starts at the random number chosen during the handshake and is cumulative
  - Acknowledgement numbers = seq nummber + 1

Errors will result in the Acknolwedgement number being set to the last successfully recieved CONTIGUOUS block of data + 1
    - A sends a seq of 10, but B only recieves 1-7, the Ack number will be 8
    - A sends a seq of 10, but B only recieves 1 and 3-10, the Ack number will be 2

#######################


====================================
TCP Handshake
====================================

.. image:: img/tcp_handshake.png

#######################


====================================
TCP Teardown
====================================

.. image:: img/tcp_teardown.png

#######################



====================================
TCP state
====================================

TCP sockets have numerous states. Many of these can be seen in the output of a properly timed netstat command

Handshake states
  - LISTEN: Awaiting a SYN
  - SYN-Sent: A client has sent the SYN, and is awaiting the SYNACK
  - SYN-RECIEVED: A server has recieved and a SYN, sent a SYNACK, and is awaiting the ACK

Data states:
  - ESTABLISHED: Normal data transmission occuring
  - FIN-WAIT-1: Client FIN sent, awaiting acknowledgement from Server. May still recieve data
  - FIN-WAIT-2: Client FIN acknolwedged by Server (half closed), awaiting Server FIN. May still recieve data 

  - CLOSE_WAIT: Client FIN recieved and acknowleged by Server. Waiting for Server to send it's own FIN (This is the server view of FIN-WAIT-1 & 2)
  - LAST-ACK: Server sends FIN. Awaiting Client to acknowledge it for teardown
  - TIME-WAIT: There is a "cooldown" period before the socket can be closed for good 
  - CLOSED: No more connection



TIME-WAIT is why you occasionally get errors that a port is in use when rapdily re-running code that creates network socket. 
  - You can use socket options to solve this


#######################


====================================
RST and ICMP
====================================

Both RSTs and FINs (eventually) result in a teardown, but the previous state listing did not reference RST at all. 

A RST can be thought of as aborting the connection (i.e. ESTABLISHED directly to TIME-WAIT/CLOSED). 

For those with Linux experience, a good a analogy is how 'kill -9' terminates a process regardless of what the process is currently doing

In TCP, a RST usually takes the place of an ICMP Port Unreachable message for closed ports

#######################


====================================
Traffic Control
====================================

Window scaling is determined during the handshake and is determines how much data each TCP segment can contain. 

Flow control in TCP is accomplished using a sliding window. Receievers specify the amount of data that they are willing to recieve, and the sender will only send that much before waiting for an ACK. If the window is 0, transmission stops for a timeout to allow the reciever to ACK with a new window. 

Congestion is controlled by the TCP stack using timers and various algorithms to estimate round trip time, and will speed up or slow down data based upon that information. 


In depth analysis of these are out of the scope of this class


#######################

====================================
TCP Header
====================================

.. image:: img/tcp_header.png

#######################

====================================
TCP Fields
====================================

Source Port – sending port

Destination Port – Receiving port

Sequence Number – Initially random. Each new transmission adds the size of the data

Acknowledgment Number – The next byte expected to be received.

#######################

====================================
TCP Fields
====================================

Data offset - Size of TCP header in 32bit words

Reserved – 0's

Flags – Bit mask of all TCP flags

Window size – Max number of bytes reciever can handle


#######################

====================================
TCP Fields
====================================

Checksum – Checksum of header and data

Urgent Pointer – Only valid if URG flag set

Options – Allows for expanded uses

#######################

====================================
UDP
====================================

UDP is connectionless and best effort delivery. Error checking is limited to a UDP checksum.

Being connectionless minimizes overhead

Removing error checking, reordering, and other nice functionality from TCP increases speed since retransmissions do not occur and there is no need to wait for acknowledgements.

#######################

====================================
Protocols using UDP
====================================

UDP is particularly well suited to protocols where a single message is sent the repsonses are also single messages:
  - DNS, DHCP, SNMP, RIP

Protocols and applications designed to handle a high volume of traffic can often intenrally handle some packet loss:
  - VOIP, Streaming Media, Video Games


#######################

====================================
UDP Header
====================================

.. image:: img/udp_header.png

#######################

====================================
UDP Fields
====================================
Source Port – sending port

Destination Port – Receiving port

Length – Size in bytes of header + data

Checksum – Error checking

#######################


====================================
Labs - Special Note
====================================

The following labs are probably the most difficult ones of the class. I fully expect this to take a significant amount of time. 

There is no need to rush. 

#######################

====================================
Lab 4A - IPv6 Multicasting
====================================

We will be doing link-local scope multicasting using UDP sockets (not RAW). 

Create a terminal based chat program that uses UDP and IPv6 Multicast. Message strings should follow the following format
  
  Username;Text Goes Here

The recievera should display recieved chats in the following format

  Chatbot (IPv6 Addr): The quick brown fox jumps over the lazy dogs

HINTS:

Ref: http://man7.org/linux/man-pages/man7/ipv6.7.html

Using the reference set the following socket options, with a level of socket.IPPROTO_IPV6 

Receiver

    - Set the multicast hops to 5

Sender
    - Set the socket's multicast group (this is for the OS, it is _NOT_ IPv6 related)
    - The group is a value obtained by combining the following:

      - Packing the multicast IPv6 addr using socket.inet_pton()
      - Packing a 32 bit unsigned integer with the value 0, using struct.pack()

#######################


====================================
Lab 4B
====================================

Modify the 4A lab to include direct messaging, without breaking existing functionality

A message that begins with @username should then be sent directly to that user

#######################

====================================
Lab 4C - TCP Reset Lab
====================================

Note: This one must use RAW sockets and both netcats must be run on the same host (open two terminal windows)

Open wireshark and sniff the ens33 interface

    - Filter on port 8888

Set up a netcat listener and connector on port 8888 using IPv6

    - DON'T TYPE ANYTHING

Observe the latest packet in wireshark (TCP Handshake initially, data afterwards)

Using raw sockets, forge an ACK/RST packet from the server that kills the connector

    - You will know it worked when the connector returns to the terminal prompt. The listener will likely still be running

    - If both netcats are still running, type something on one end and verify it on the other side. Then try again using the latest packet in wireshark

Hints
    - You MUST have checksum. Use send_chksum() from the helper code
    - Seq nos and Ack nos are important!

#######################


====================================
Lab 4D - TCP Reset Lab v2
====================================

Repeat the TCP reset lab, except type send a bunch of messages from each netcat terminal before attempting to kill the connection.


#######################



====================================
Lab 4 BONUS
====================================

Recreate the lab using RAW sockets, but this time spoof your IPv6 address in creative ways. 

#######################

====================================
Layer 4 Overview  
====================================

TCP is connection oriented protocol with error handling and traffic control

TCP begins with a handshake and ends with a teardown

TCP Flags and Sequence/Acknowledgement numbers are key components

TCP's functionality adds overhead to all traffic

UDP is connectionless and best effory delivery, with no error handling

UDP is designed for minimal overhead and single message/response traffic 


