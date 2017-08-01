:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
Layer 2 
====================================

Basics of Layer 2 and Ethernet

#######################

====================================
Layer 2 Overview  
====================================

- Introduction to Ethernet

- Layer 1 Network Devices

- Layer 2 Network Devices

- MAC Addresses

- Switching

- Ethernet Header

- Ethernet Header Fields

- ARP and RFC 826

- ARP header fields

- LAB

#######################

====================================
Introduction to Ethernet
====================================

Ethernet is a family of technologies used to connect LANs and WANs. It has used several different physical mediums over time from coaxial, to twisted pair, and now fiber. 

The Ethernet protocol is the foundation of sending and receiving traffic and is lowest level of network communication we will discuss in class. 


#######################

====================================
Layer 1 Devices
====================================

Sole-purpose layer 1 devices are mostly extinct in today's environments. As technology advanced, the functionality became obsolete or was rolled into layer 2 devices. 

Repeater - Has 2 ports. Takes recieved data from one side and retransmits it on the other. It allows the physical transmission medium to be extended.

Hub - A multi-port repeater. Data is recieved on one port, and retransmitted out ALL other ports (except port it was recieved on)

Single Collision Domain

Single Broadcast Domain

#######################

====================================
Layer 2 Devices
====================================

Bridges have two ports and connect two independent PHYSICAL networks. These days, you are most likely to encounter a bridge in virtualization software or a system's network interfaces. (e.g. bridging vs NAT mode for VMs, or combining two interfaces in Linux )

Switches are multiport bridges and are still prelevant in networks today. Switches are typically the lowest level device that makes decisions on where to send traffic. The MAC (Media Access Control) address is what switches use to make those decisions.

Multiple Collision Domain
  - Each physical connection to a switch port is a collision domain

Single Broadcast Domain 

#######################

====================================
MAC Addresses
====================================

48 bits long, usually represented as 6 groups of hex (e.g. aa:bb:cc:dd:ee:ff)

Manufacturers 'burn in' a MAC address to each port on a device, however most modern equipment allows the MAC to be changed in software as well

Organizational Unique Identifier - (OUI) First 3 bytes
 - OUIs specific to each manufacturer (VMWare OUI 00:50:56, Intel OUIs 00:02:B3, 00:03:47, 00:04:23)
 - Majority of the time OUIs are enforced. The MAC address of a device will be unique within the network
 - LSBit in 1st byte in OUI determines if address is unicast (0) or muilticast (1)
 - 2nd LSBit in 1st byte in OUI determines if the mac is globally unique (0), or locally administered (1)

Host ID - Last 3 bytes
 - Randomly decided by manufacturer
 - Ideally there are no collisions within a physical network

Special MAC Addresses

  - The Layer 2 BROADCAST address for IPv4 and ARP is FF:FF:FF:FF:FF:FF
  - The Layer 2 MULTICAST address for IPv6 is 33:33:00:00:00:01

#######################


====================================
Switching
====================================

Switches operate using MAC addresses found in the Ethernet header of the traffic. 

Switches have CAM (Content Addressable Memory) tables that map a physical port to MAC addresses
  - Switches populate a CAM table by looking at the Ethernet header and determining the SOURCE address of traffic arriving on that port
  - It is possible the table maps multiple MAC Addresses to the same physical port (e.g. Switch port is connected to a hub with multiple hosts)

Switches check the DESTINATION MAC address against the MAC table
  - If the address is mapped to a port, forward it out that port
  - If no mapping, forward it out ALL ports EXCEPT the one it was received on 
    - Traffic usually gets a response, and the MAC table will be updated normally when that traffic is seen

If the DESTINATION MAC is a broadcast address, then forward it out ALL ports EXCEPT the one it was received on 


#######################

====================================
Ethernet header
====================================

.. image:: img/ethernet_header.png

#######################

====================================
Ethernet Header Fields
====================================

Source MAC Address -  Originator of the traffic

Destination MAC Address - The Ethernet address of the intended recipient. Must be in the same broadcast domain, and may be a broadcast address

Ethernet Type (aka EtherType)- What is being transmitted in the Ethernet payload? 
  - ARP, IPv4, IPv6, etc...
  - See references page


#######################

====================================
ARP Header
====================================
.. image:: img/ethernet_arp_request.png


#######################

====================================
ARP Header fields
====================================

Hardware Type - The physical medium of transmission. 1 for Ethernet, 6 for 802.11 (wifi)

Protocol Type - Uses same constants as EtherType. Identifies the Layer 3 address that needs to be mapped to an Ethernet address

Hardware Address Length - Size of Layer 2 address defined in Hardware type

Protocol Address Length - Size of Layer 3 address defined in Protocol Type


#######################

====================================
ARP Header fields
====================================

Op Code - 1 for Request, 2 for Reply. Other codes exist for protocols that make use of an Arp Header

Sender Hardware Address, Sender Protocol Address - The sender's addresses

Target Hardware Address, Target Protocol Address - The target's addresses, The hardware address is filled in upon receipt of ARP Request

#######################

====================================
Helper Code
====================================

How to use helper code. This code sends a frame to yourself:

::

  from raw_socket_helper import RawSocket

  ...

  interfaceName = "ens33"   # from ifconfig
  raw_socket = RawSocket(interfaceName)

  raw_socket.send(frame)          # Layer 2 has no checksums
  raw_socket.send_chksum(frame)   # Most higher layer protocols require checksums to be computed

#######################


====================================
Coding Suggestions
====================================

Your raw socket code in the class builds on itself. It is also a chore to debug if your code is disorganized and poorly structured. I recommend three things

1) Organize your code into sections, where each section deals with a specific header

2) One variable with a descriptive name, per field. Don't combine fields unless you have too (ie smaller than a byte, bit flags, etc) 

3) Comment your variables so you know what the values are and what they mean


#######################


====================================
Coding Suggestions
====================================

Look at the example below for a skeleton that allows extension into layer 3 and above. 

::

  from raw_socket_helper import RawSocket

  # Constants
  mymac = "\x00\x0c\x29\xc9\x78\x14"
  myip = ...


  # Layer 3 Header
  l3Field1 = ... 
  l3Field2 = myip
  l3hdr = l3Field1 + l3Field2 + ...

  # Layer 2 Header
  dst = mymac       # Destination MAC
  src = mymac       # Source MAC
  typ = '\x00\x00'  # Ether Type, 0x0800 = IPv4  
  etherhdr = dst + src + typ
  
  # Make the complete frame and send it
  frame = etherhdr + l3hdr + ...     

  interfaceName = "ens33"   # from ifconfig
  raw_socket = RawSocket(interfaceName)
  
  # Makes it easy to find in wireshark
  for i in range(5):
      raw_socket.send(frame)          # Layer 2 has no checksums
      #raw_socket.send_chksum(frame)  # Most higher layer protocols require checksums to be computed


#######################


====================================
Debugging
====================================

Wireshark shows you all data, from Layer 2 onward using the collapsible trees in the packet window

Highlighting a field will show it's hex value highlighted

Wireshark will tell you if a packet is malformed, a protocol is malformed, there is an incorrect size, or there is a bad checksum, etc

If you have a checksum issue:
  
  - Make sure you use send_chksum() from the helper code
  - Make sure any size fields are calculated correctly. Check with the RFC
  - Are your checksums and reserved fields set to 0?


If you have a malformed packet/protocol

  - Ensure your fields are the proper width. Check with the RFC
  - Make sure any size fields are calculated correctly. Check with the RFC


A correctly formatted packet may still have bad data, If your code doesn't work, and wireshark shows it as a valid packet, your actual values are likely incorrect



#######################


====================================
LAB
====================================

In this lab you will be manually generating raw frames and transmitting them over the network.

Use the helper code provided to you (put the .py or .pyc files in the same diectory as your code)

Use Wireshark to identify the traffic on the wire. This will also help you troubleshoot.

1) A frame to your Windows machine or a coworker's machine (may need to use ipconfig/ifconfig)

2) ARP Request

What will happen if you send a complete ARP Reply to a host that did not send an ARP Request?
  - What vulnerability does this introduce?

#######################

====================================
LAB 2A
====================================

Generate a frame to your neighbor. They will have to tell you their MAC Address. 

Ensure that you see both your frame and your neighbor's frame on Wireshark. 
 

#######################

====================================
LAB 2B
====================================

Generate a valid ARP Request to your neighbor. Valid means it conforms the RFC, Wireshark confirms it is not malformed/displays no errors, and your request produces a reply.

Ensure that you see both your frame and your neighbor's frame on Wireshark. 

Ensure that you see the ARP Reply triggered by your ARP request in Wireshark. If you do not, your frame is incorrect.


#######################


====================================
References
====================================

RFC: 

  ARP - https://tools.ietf.org/html/rfc826

EtherType: 
  
  http://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml


#######################

====================================
Layer 2 Overview  
====================================

Layer 1 and 2 Network devices
  - Switches are most prevelant

Layer 2 addresses are MAC addresses

Switching allows networking via Layer 2

Ethernet Header and ARP traffic
