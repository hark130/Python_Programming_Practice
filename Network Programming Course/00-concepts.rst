:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
MQT Basic Developer Training
====================================
Network Programming
------------------------------------
 
::

	Authors:
	Eric Ortega 	eric.ortega@us.af.mil
	Chris Plummer 	christopher.plummer.4@us.af.mil

	Version:
	v2 2 DEC 2016 

#######################



====================================
Scary slide first
====================================

After this class you will be expected to perform on a team. You will be tasked to do things you are unfamiliar with. 

Independently solving problems using technical resources is a requirement in this line of work. 

The slides will NOT cover everything in detail. I will cover the topics at a high level, provide you references for the implementation, and assist you in learning tools to debug your code.  

I expect you to use those resources and make an effort to figure it out yourself. 

#######################


====================================
Class Structure
====================================

"Try it" - I encourage experimentation (we can ALWAYS reboot), but do NOT interfere with your classmates learning

Make mistakes! Ask questions! This is how we all learn.

Lectures will be brief. This course is primarily labs.

Protip: It might be very beneficial to have working lab code by the end of the course


#######################


====================================
Environment
====================================

The majority of labs will be IPv6 and using raw sockets. 

We will be using Linux for this class because Windows does not properly support raw sockets.

If you need assistance with Linux, let us know during the lab portions. 

#######################

====================================
Concepts Overview  
====================================

- Numbering Systems

- Endianness

- RFCs

- Wireshark

- Netcat

- OSI Model

- Broadcast vs Collision Domains

#######################

====================================
Numbering Systems
====================================

bit  	= 1 or 0

nibble 	= 4 bits, half a byte

octet 	= 8 bits 

A byte on most computers is the same as an octet, but other architectures exist with differing sizes

#######################

====================================
Numbering Systems
====================================

Hexadecimal - base 16

	- Counting: 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,10,11,12, ....

	- A single hex digit = 4 bits/half a byte

Octal - base 8

	- Counting: 0,1,2,3,4,5,6,7,10,11,12, ...

#######################

====================================
Numbering Systems
====================================

Place value is the key. 

In decimal our BASE is 10: 

  - BASE ^ 0 = 10^0 = 1, "ones"
  - BASE ^ 1 = 10^1 = 10, "tens"
  - BASE ^ 2 = 10^2 = 100, "hundreds"

A number like 25 is broken down:

		- (2*10) + (5*1) = 20+5 = 25

#######################

====================================
Numbering Systems
====================================

In hexadecimal the "tens" place is actually "sixteens", and the "ones" stays the same but now consists of 15 numbers, 0 to F.  

BASE is 16: 

  - BASE ^ 0 = 16^0 = 1, "ones"
  - BASE ^ 1 = 16^1 = 16, "sixteens"
  - BASE ^ 2 = 16^2 = 256, "256ths"

Convert 2A into decimal	

		- (2*16) + (A*1) = (2*16) + (10*1) = 32+10 = 42

#######################
	
====================================
Endianness
====================================

A number is represented by a sequence of bytes. A 32 bit integer is 4 bytes. 

  - Least Significant Byte (LSB)- The byte representing the smallest part of a number (e.g. the "ones")

  - Most Significant Byte (MSB) The place representing the largest part of a number 

Endianness tells us how to read a grouping of bytes. 

  - Big Endian - MSB is first

  - Little Endian - LSB is first



#######################

====================================
Endianness
====================================

0xDEADBEEF (4 bytes)

  - Little Endian - 0xEF, 0xBE, 0xAD, 0xDE
  - Big Endian - 0xDE, 0xAD, 0xBE, 0xEF

#######################

====================================
Endianness
====================================

Network byte order is Big Endian

x86/x86_64 are Little Endian

Know what endian your data is in or you will have problems with binary data


#######################

====================================
RFC -  Request for Comments
====================================

Originally (in the ARPANET days) a semi-formal document of ideas shared to get comments from peers.  Now they are issued by the Internet Engineering Task Force (IETF) to formally define an accepted specification

RFCs describe and define the history, implementation, formats, and use of protocols. They are the authoritative source of information regarding protocols. 

#######################

====================================
RFC -  Request for Comments
====================================

You should not 100% rely on vendor implementations or internet posts if you have questions about a protocol. 

Microsoft intentionally implemented parts of the HTML/web protocols incorrectly around the era of Internet Explorer 5 and 6.  

Posters on forums, even Stack Overflow, can say something that sounds correct/interpreted as correct, even if the RFC specifies otherwise.

Stack Overflow is still a highly useful site, just use it to supplement/validate your understanding of the RFC.

#######################


====================================
Pydocs
====================================

Python documentation can be accessed online

Each module has it's own page describing the functions, function parameters, constants, and example usage. These will be linked in the references slide in each slide deck.

The search function on Pydocs will let you search for a specific function to see it's parameters and return values. It does require you to know the module.

  e.g.  accept() can be found by searching socket.accept()



#######################

====================================
Man pages
====================================

The BSD socket API is POSIX compliant and is the standard on Linux machines. There are man pages that describe each system call. 

The man pages can be accessed via a terminal in Linux, or via Google.

Man pages have different numbers for different sections. I typically link to man 7 pages which in turn link to the man 2 pages for specific calls. 

  7 describes the higher level operations

  2 describes the system calls for C (which are reused in Python)

e.g. 

  man 7 socket describes sockets and the associated function calls. 

  man 2 <function name> would provide details of a specific call for sockets

#######################

====================================
Wireshark
====================================

Wireshark is a GUI based protocol analyzer. It works on live traffic and PCAP files.

There are three windows in Wireshark:

	1. The traffic window which shows the packets in order of receipt

	2. The packet window which shows the packet (and frame) breakdowns of the selected packet from the traffic window

	3. The hexdump window which shows the raw bytes of the highlighted section highlighted in the packet window

#######################

====================================
Wireshark
====================================
.. image:: img/wireshark-example2.png

#######################

====================================
Wireshark 
====================================

Wireshark requires you to select an interface to sniff traffic

The 'lo' interface is the loopback. Any traffic that is both to and from a single host (A VM and Host OS are different hosts) will show up on this interface. Typically this traffic will never touch the wire

The 'ens33' interface should be the one you have bridged in VMWare. If you have traffic from different hosts, it will show up here.

The 'any' interface should show you all traffic on all interfaces and is the noisiest. We have had issues with this interface in the past. Do not use for these labs.


#######################

=============================================
Wireshark - Quick and Dirty Intro to Filters
=============================================

Click the expression button to the right of the Filter bar

OR type it in yourself:

  eth.addr == aa:bb:cc:dd:ee:ff

	ip.addr == 127.0.0.1

	ip.src == 127.0.0.2

	ipv6.dst == ::1

	tcp.port == 1337

	tcp.sport == 80

	udp.dport == 53

You can also filter on protocol

    arp

    icmpv6


#######################

====================================
Netcat
====================================

Netcat is the "swiss army knife" of networking. It is a simple networking program that can be used as a client or server. 

Any data that is recieved is printed to the terminal (or file if using file redirection)

Netcat supports both IPv4/IPv6 and TCP/UDP

You can use netcat to recieve traffic you are sending, or to simulate a client accessing a server.

#######################

====================================
Netcat - Linux
====================================

Most linux distros have netcat built in. It can be executed with 'nc' command. 

Useful netcat switches

    -6: IPv6  

    -l: listen 

    -p: Source port to listen on

    -u: UDP mode

#######################

====================================
Netcat - Windows
====================================

Some people have compiled the netcat source for Windows and posted the binaries online. There is one binary for IPv4 and one for IPv6, however they have the exact same functionality.

nc.exe is for IPv4

nc6.exe is for IPv6

Useful netcat switches

    -l: listen 

    -L: listen harder (Windows only, automatically listens again after connection terminates)

    -p: Source port to listen on

    -u: UDP mode

#######################

====================================
Using netcat
====================================
Netcat listener ("server")

	- nc -lp 1337 (-p is only for listeners)

Netcat connector ("client")

	- nc 192.168.1.1 1337 

File redirection
	
	- netcat supports file redirection. Files piped into netcat will send be sent over the wire. Output from netcat may be piped to a file

Loops can be used as a ghetto server

	- nc -Lp 80 < index.html 

	- while true; do sudo nc -lp 80 < index.html; done (Equivalent to -L in Windows)



#######################

====================================
OSI Model
====================================

.. image:: img/osimodel.png

From: https://infosys.beckhoff.com/content/1033/tf6310_tc3_tcpip/Images/png/84433547__Web.png

#######################

====================================
TCP/IP Model
====================================

.. image:: img/tcpmodel.jpeg

From: http://lemoncisco.blogspot.com/2014/06/internetworking-with-tcpip-notes_18.html

#######################


====================================
Models
====================================

The OSI model is primarily a theory model

The TCP/IP Model is more practical oriented. 

Both are useful at different times. We are primarily concerned with OSI layers 2,3,4,7 in this class

#######################

====================================
Broadcast vs Collision Domains
====================================

Collision Domain – A grouping of networked devices on a shared medium (Coax ethernet, wifi, etc) that can cause a collision when two device transmit simultaneously
  - Extended by: repeaters, hubs
  - Divided by: switches 


Broadcast Domain – A grouping of networked device that can all be reached by a layer 2 broadcast
  - Extended by: repeaters, hubs, switches
  - Divided by: routers

#######################



====================================
LAB 0
====================================

The following slides contain several labs for you to do. 

I expect you to be able to use Wireshark for debugging. Make sure you understand how to find Ethernet addresses, IP addresses, 


#######################


====================================
LAB 0A
====================================

Almost all class labs are to be done in IPv6. Give yourself a global IPv6 address starting with a:c:7:9::X. If you have issues, let us know.

0) Execute 'ifconfig' and find your interface name (mine is ens33)

1) Become root

2) As root, edit /etc/networking/interfaces. Any editor will work, as long as you run execute it as root from the terminal

  Edit the file to look similar to what is below. Do not alter the 'lo' interface

::

    # interfaces(5) file used by ifup(8) and ifdown(8)
    auto lo
    iface lo inet loopback

    auto ens33
    iface ens33 inet dhcp

    iface ens33 inet6 static            
        address a:c:7:9::QQ/64  #Replace QQ with your assigned number

3) As root execute 'service networking restart'. If this does not work, you will need to reboot your VM.

4) Execute 'ifconfig' and validate your address is there


#######################


====================================
LAB 0B
====================================

Run nc and nc6 listeners and connectors. Ensure you can connect to yourself and send data via the following IP addresses:

    - 127.0.0.1
    - ::1
    - Your IPv4 address
    - Your IPv6 a:c:7:9::X address
    - Your IPv6 address beginning with "fe80"


#######################


====================================
LAB 0C
====================================

Open wireshark.

In preferences, uncheck the box for "Relative Sequence Numbers" in TCP options

Practice filtering traffic 

    - By IP/IPv6
    - BY MAC Address
    - by port
    - By protocol
    - A combination of the above


Use 'ping' and 'ping6' to test connectivity to your classmates

Use netcat to send traffic back and forth using IPv4 and IPv6


====================================
Questions and Debugging
====================================

Which IPs are visible on the loopback/lo interface?

Which IPs are visible on the normal enterface ('ens33', 'eth0' or something similar)?

How do you see into Ethernet, IP, TCP/UDP, and data information of a packet?

What are some of the fields in those layers?

How do you see the specific bytes of a field? How can you highlight them?


#######################



====================================
Concepts Summary  
====================================

Numbering Systems
    - Converting to hex will be crucial for raw sockets

Endianness
    - Know your endianess when dealing with binary

RFCs are the authority for protocols

Wireshark is your network debugger

Netcat can be used for many networking tasks.

OSI Model is the theory model. In practice, it becomes the TCP/IP model

Broadcast vs Collision Domains