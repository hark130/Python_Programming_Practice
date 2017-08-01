:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
Layer 3
====================================

Basics of Layer 3 and IP

#######################

====================================
Layer 3 Overview
====================================

- Introduction to IP

- IPv4 Addresses

- IPv4 Address Classes

- Subnet Masks

- CIDR

- Routers

- Routing Protocols

- Routing Basics

- Routing

- IPv4

- IPv4 Header Fields

- NAT and PAT

- IPv6

- IPv6 Addresses

- IPv6 Address Types

- IPv6 Global Unicast

- IPv6 Multicast

- IPv6 Anycast

- IPv6 Header Fields

- ICMP

- ICMP Types and Codes

- Ping

- Reasons for ICMP Error Messages

- MTU and Fragmentation

- ICMP Header

- NDP

- IPV6 Labs

#######################


====================================
Introduction to IP
====================================

Ethernet addressing is limited to networks sharing the same physical medium (i.e the broadcast domain). In order to connect multiple distinct networks, a new technology is needed.

The Internet Protocol (IP) is the Layer 3 protocol that we to address hosts and route traffic across networks.

There are two main types, IPv4 and IPv6

#######################


====================================
IPv4 Addresses
====================================
IPv4 Addresses are represented in “dotted decimal” notation

IPv4 addresses are 32 bits, so each number is represented by a single byte

    You can represent an IP using an unsigned 32 bit data type, e.g. uint32_t in C

There are 2^8 possible values for an octet ranging from 0-255

#######################

====================================
IPv4 Address Classes
====================================

Class A - first bit is 0 (First octet 1-127)

Class B - first TWO bits are 10 (First octet is 128-191)

Class C - first THREE bits are 110 (First octet is 192-223)

Class D - first FOUR are 1110 (First octet 224-239) Used only for multicasting and thus no network/host specified

Class E - The following IPs 240.0.0.0 to 255.255.255.254. Used for experimentation only. No network/host specified

#######################

====================================
Subnet masks
====================================

Subnet masks were introduced to identify the NETWORK and HOST bits of an IP

Subnet masks are a special kind of IPv4 address used in tandem with a normal IPv4 addresses to provide that context

They are used when configuring interfaces of network devices (PC's, Routers, etc). They are NOT transmitted with regular network traffic.

#######################

====================================
Subnet masks
====================================

Subnet masks are a contiguous block of 1's followed by any remaining bits set to contiguous 0's. The contiguous bits may span several octets.

Mixing 1's and 0's together is not allowed. This means that the only valid numbers in a subnet mask are: (0, 128, 192, 224, 240, 248, 252, 254, 255)

::

  255           .255          .248          .0
  11111111      .11111111     .11111000     .0


#######################

====================================
Subnet masks
====================================

All bits in the IP address that are masked with 1's determine the NETWORK, and all 0's are determine the HOST

If you bitwise AND an IP and a subnet mask, you will get the network IP.

::

  172.16.237.18
  255.255.248.0

  10101100      .00010000     .11101 | 101     .00010010
  11111111      .11111111     .11111 | 000     .00000000

  10101100      .00010000     .11101 | 000     .00000000

  172.16.232.0 is the network IP


#######################


====================================
CIDR
====================================

CIDR notation is a quick way of writing a subnet mask that allows for advanced networking

After the IP address put a slash followed by the number of network bits

::
  192.168.1.2 with a mask 255.255.224.0

  11111111      .11111111     .11100000     .00000000

  There are 19 contiguous 1's, so the CIDR notation is 192.168.1.2/19

#######################

====================================
Routers
====================================

Routers operate on Layer 3 address (IP)

They ignore Layer 2 addresses for decision making

Multiple Collision Domains

Multiple Broadcast Domains

#######################



====================================
Routing Protocols
====================================

Routing protocols allow neighboring routers to collaborate dynamically

There are two main types, distance-vector and link-state

Distance-vector protocols attempt to calculate the "distance" between networks. Usually this is the total number of hops, or the sum of all weights on a path.

Link-state protocols are more concerned with speed and current state of the connections. A longer path with a faster travel time will be prioritized over a path with less hops.

Hybrid protocols also exist

#######################

====================================
Routing Protocols
====================================

Routing protocols define the metric(s) used to calculate weights.

Weights are calculated individually on each router for each known network. The weight for the exact same network may be different on different routers.

Static routes may also be set, with arbitrary weights, by a network administrator

The “best” weight is used by a router to decide where send the packet. Weights are usually represented as an integer, and the lowest number is considered best.


#######################

====================================
Routing Protocols
====================================

Routers have routing tables that map a NETWORK, WEIGHT, and the NEXT HOP ADDRESS

Routing tables are populated by the information exchanges dictated by the specific routing protocol being used on that router and it's neighbors

      - Neighbors advertise what NETWORKS they know about, and their WEIGHTS

      - The NEXT HOP will either be the IP of the router that advertised the best path to a destination, OR it will be the locally connected network

#######################

====================================
Routing Basics
====================================

Packets are routed independently of each other, even if they are to the same destination

Traffic destined for a private IP address will not be routed onto the public internet without special configurations

Broadcast traffic will not be routed outside of that network

#######################

====================================
Routing
====================================

When a router receives a packet, the destination IP of a packet is compared to the networks in the routing table

  - If the network is directly connected, send the packet to that network

  - If the network is known, but not connected, send it to the NEXT HOP specified in the routing table with the 'best' weight

  - Otherwise send it to the DEFAULT GATEWAY

#######################


====================================
IPv4
====================================

IPv4 was adopted by IETF in 1981. IPv4 is the common version of IP we are used to dealing with

Initially, every device was to have it's own IPv4 address.

The explosion of the Internet dramatically increased the number of connected devices so IPv4 was modified slightly to curb address exhaustion.

These modifications included NAT, PAT, and subnetting

The supply of IPv4 has been exhausted (most recently North America in Sept 2015)

#######################

====================================
IPv4 Header
====================================

.. image:: img/ipv4_header.png

#######################


====================================
IPv4 Fields
====================================

Version - Set to 4 for IPv4

Header Length – Size of IP header

Differentiated Services Code Point (DSCP) – Formerly “Type of Service (TOS)”, it was redefined by RFC 2474. Used for new technologies that require real time data streamed over the network. We will not deal with this in this class

Explicit Congestion Notification – Formerly part of TOS, used to indicate network congestion. NOTE: This is not the same as TCP's congestion handling


#######################


====================================
IPv4 Fields
====================================

Total Length – Size of packet in bytes, including header and data

Identification – Identifies a group of IP fragments

Flags – Fragment flags
::
  Bit Indicator 	RFC 791 Definition
  0xx 	          Reserved
  x0x 	          May Fragment
  x1x 	          Do Not Fragment
  xx0 	          Last Fragment
  xx1 	          More Fragments

  from: http://www.wildpackets.com/resources/compendium/tcp_ip/ip_fragmentation

Fragment offset – offset of fragment from original packet

#######################


====================================
IPv4 Fields
====================================

Time to Live – Decremented first thing at each hop, packet is discarded when TTL is 0

Protocol – Protocol used in data portion

Header checksum – Error Checking

Source / Destination IP – Do not change during routing

#######################


====================================
IPv4 Fields
====================================

IPv4 has the ability for optional headers, but they are typically not used.

Seeing them in IPv4 is worth an investigation

#######################

====================================
NAT and PAT
====================================

NAT - Network Address Translation

  - Modifies an address inside your network, to a global IP (may be single address or from a pool)

  - NAT does not require private addresses


PAT - Port Address Translation

  - A mapping of inside IP/port to public IP/port is maintained by router

  - Return traffic will have the same Public IP/port which can be looked up and forwarded to the appropriate inside IP/port

#######################


====================================
IPv6
====================================

IPv6 is the latest version. It returns to the cleaner design of IP that IPv4 had before attempts to curb exhaustion happened.

Differences from IPv4

  - Back to single address per host, address translation is no longer needed
  - Multicasting, QoS, IPSec, and Encryption is built in
  - IPv6 can autoconfigure itself in a local network


See referenced for IPv6 RFC

#######################

====================================
IPv6 Addresses
====================================

IPv6 addresses are 128 bits long and represented by groups of 1-4 hex characters seperated by a : (aka a "hextet")
  - 2001:0db8:0000:0000:0000:ff00:0042:8329

Leading 0's in a grouping may be omitted

  - 2001:db8:0:0:0:ff00:42:8329

It may contain at MOST a single :: which represents the largest contiguous block (longer than than 16 bits) of 0's in the address

  - 2001:db8::ff00:42:8329 last


If multiple contiguous blocks are the same length, shorten the left most one

  - 2001:0:0:AAAA:0:0:B:CC becomes 2001::AAAA:0:0:B:CC

1 single 16 bit block of 0's should NOT be replaced with a  \::

  - A:0:B:CCC:0:22:0:44 should never be reduced with a \::


The Layer 2 (Ethernet) multicast address for IPv6 is 33:33:00:00:00:01

#######################

====================================
IPv6 Address Types
====================================

Generally there are three types of addresses
  - Unicast
  - Multicast
  - Anycast

There are also several scopes:

  - Global ("Public" in IPv4)
  - Site Local ("Private" in IPv4)
  - Link Local

There is no IPv6 broadcast address. Multicast addresses fulfill that role

#######################

====================================
IPv6 Address Types
====================================

The type of address is specified by the value of the first hextet



+---------------------+-------------------------------------+--------------------------------+
| IPv6                | Description                         | IPv4 Equivilent                |
+=====================+=====================================+================================+
| ::/128              | Unspecified/Default                 | 0.0.0.0                        |
+---------------------+-------------------------------------+--------------------------------+
| ::1/128             | Loopback                            | 127.0.0.1                      |
+---------------------+-------------------------------------+--------------------------------+
| fec0::/7            | Site local, not routed              | 10.0.0.0/8, 192.168.0.0/16     |
+---------------------+-------------------------------------+--------------------------------+
| fe80::/10           | Link Local, not routed              | 169.254.0.0/16                 |
+---------------------+-------------------------------------+--------------------------------+
| ff00::/8            | Multicast                           | Class D                        |
+---------------------+-------------------------------------+--------------------------------+
| 2001::/32           | Teredo, Allows IPv6 over IPv4       | n/a                            |
+---------------------+-------------------------------------+--------------------------------+
| 2002::/16           | 6to4, Allows IPv6 over IPv4         | n/a                            |
+---------------------+-------------------------------------+--------------------------------+

NOTE: This list is not exhaustive

http://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xhtml

#######################

====================================
IPv6 Global Unicast
====================================

A global unicast address can be broken down as follows:

.. image:: img/ipv6_global_unicast.png

from: https://mrncciew.com/2013/04/05/ipv6-basics/

#######################

====================================
IPv6 Multicast
====================================

A global multicast address can be broken down as follows:

.. image:: img/ipv6_multicast.png

From: https://mrncciew.com/2013/04/05/ipv6-basics/

From: http://www.txv6tf.org/wp-content/uploads/2013/07/Martin-IPv6-Multicast-TM-v3.pdf

#######################


====================================
IPv6 Multicast
====================================



+---------------+-----+-------------------------------------+--------------------------------+
| IPv6 Multicast Address       | Description                                                 |
+===============+=====+=====================================+================================+
| FF01:0:0:0:0:0:0:1           |  All Nodes (NL)                                             |
+---------------+-----+-------------------------------------+--------------------------------+
| FF02:0:0:0:0:0:0:1           |  All Nodes (LL)                                             |
+---------------+-----+-------------------------------------+--------------------------------+
| FF01:0:0:0:0:0:0:2           |  All Routers (NL)                                           |
+---------------+-----+-------------------------------------+--------------------------------+
| FF02:0:0:0:0:0:0:2           |  All Routers (LL)                                           |
+---------------+-----+-------------------------------------+--------------------------------+
| FF05:0:0:0:0:0:0:2           |  All Routers (LL OSPFv3)                                    |
+---------------+-----+-------------------------------------+--------------------------------+

NOTE: This link is not exhaustive

#######################

====================================
IPv6 Anycast
====================================

Anycast addressing does not operate like traditional addressing

Anycast addresses are in the global unicast range. The same global unicast address is assigned to multiple interfaces (perhaps on several different nodes)

Traffic destined to the anycast address will be delivered to the "nearest" host with that address. It's a trick to rely on a routing protocol which determines the "closest" host that was configured with the address

Don't use an anycast address as a source address

This seems strange. Why do it?

Some services are run on multiple servers (DNS or NTP for example). You would assign anycast addresses where multiple severs provide the same service but only one reply is required to use the service


#######################

====================================
IPv6 Header
====================================

.. image:: img/ipv6_header.png

#######################


====================================
IPv6 Fields
====================================

Version – Set 6 for IPv6

Traffic Class – Categorizes traffic for QoS purposes. ECN is last 3 bits

Flow Label – Request special handling by routers. May not be honored

Payload Length – Size of payload in OCTETS. Including any extension headers

#######################


====================================
IPv6 Fields
====================================

Next Header – Layer 4 header of payload. Uses same values as IPv4's protocol field

Hop Limit – Same as TTL

Source / Destination - Do not change during routing

#######################


====================================
IPv6 Headers
====================================

IPv6 Headers are identified by number. They are not required to be used, however they provide useful features that were absent or poorly implemented in IPv4.

0 = Hop-by-Hop Options - Options that need to be examined by all devices on the path.

60 = Destination Options (before routing header) - Options that need to be examined only by the destination of the packet.

43 = Routing - Methods to specify the route for a datagram (used with Mobile IPv6).

44 = Fragment - Contains parameters for fragmentation of datagrams.

51 = Authentication Header (AH) - Contains information used to verify the authenticity of most parts of the packet.

50 = Encapsulating Security Payload (ESP) - Carries encrypted data for secure communication.

135 = Mobility (currently without upper-layer header) - Parameters used with Mobile IPv6.

From wikipedia

#######################

====================================
ICMP
====================================

Internet Control Message Protocol

A "helper" protocol that supports IP and provides error reporting and relay queries

Many messages have been deprecated, reserved, or are obsolete

Each message has a Type, and each type may have several Codes

#######################


====================================
ICMP Types and Codes
====================================

See References page for bigger list

Type 0 Echo Reply
  - Ping

Type 3 Destination Unreachable
  - Code 0 Destination Network Unreachable
  - Code 1 Destination Host Unreachable
  - Code 3 Destination Port Unreachable (NOTE: See Layer 4 for slight modification regarding TCP)

Type 8 - Echo Request
  - Ping

Type 11 Time Exceeded
  - Code 0 TTL Exceeded
  - Code 1 Fragement Reassembly Time Exceeded

Type 30 Traceroute
  - Deprecated

#######################


====================================
Ping
====================================

Ping is ubiquitous. It shows the connectivity status between two hosts

Host A initiates request to Host B
  - ICMP Type 8

Host B receives it, and sends a response to A
  - ICMP Type 0


#######################


====================================
Reasons for ICMP error messages
====================================

If the packet cannot be delivered to a host, an ICMP message is generated by the last node that handled the packet, and returned to the sender. Below, I've captured some anecdotal reasons you will see some common ICMP errors. They are NOT absolutes, but just things to think about should you encounter them.

  - Network unavailable typically means there is no route to the network

  - Host unreachable is usually one of two reasons

    - Layer 1 is broken, host physically offline
    - A security feature is preventing access to the host (firewall, proxy, etc)

  - Port Unreachable is usually one of two reasons

    - A service is likely not running on that port*

    - A security feature is preventing access to that port (firewall, proxy, etc)

  - TTL Exceeded

    - Something is unusual about the route to the host that makes the path quite long

  - Reassembly Time Exceeded

    - I have never encountered this, however a severely degraded connection with multiple varying MTUs could theoretically cause this

#######################


====================================
MTU and Fragmentation
====================================

Maximum Transmission Unit is the maximum size of the payload on a given link-layer (Layer 2) protocol. (1500 bytes for Ethernet)

The max size of an IP packet is 65535 bytes (unless jumbogram extension header is used)

IP packets that are bigger than the link-layer protocol MTU are FRAGMENTED into several frames, and the recipient is responsible for reassembly

MTU can vary at each hop. This means it is possible for every node on the path to the destination to further fragment
  - Senders usually try to discover the smallest MTU on the path and shrink their own transmissions appropriately

Packets larger than MTU are dropped and ICMP message returned to sender indicating the packet is too big



#######################

====================================
ICMP Header
====================================

.. image:: img/icmp_header.png

From: https://notes.shichao.io/tcpv1/ch8/

#######################



====================================
NDP (Part of ICMPv6)
====================================

Neighbor Discovery Protocol is a collection ICMPv6 messages for auto configuration, discovery, and awareness. NDP has of the same functionality as regular routing protocol, however they are not the same thing.

Neighbor Solicitations - IPv6 message to map a known IPv6 address to a layer 2 address

Neighbor Advertisements - IPv6 message to broadcast your own layer 2 address to the network

Router Solicitation - Request a Router Advertisement, also performed during bootup

Router Advertisements - Here are all networks I know about

Redirect - A better route to a given host, causes updates among each host


#######################


====================================
References
====================================

RFC:

  NDP - https://tools.ietf.org/html/rfc4861

  ICMPv6 - https://tools.ietf.org/html/rfc4443

  ICMP - http://www.faqs.org/rfcs/rfc792.html


#######################


====================================
LAB 3
====================================

You will be implementing the NDP messages using the IPv6 raw socket helper code.

::

  from raw_socket_helper import RawSocket_IPv6

Hints:

  Read the RFC before starting. It tells you what values to put in fields

  Think about the scope of your IPv6 addresses

  What is the multicast MAC address for IPv6?

  The first 32 bits of the IPv6 header (Version, Traffic Class, Flow Label) should be '\x60\x00\x00\x00'

  All Checksums should be all 0's

  All Reserved should be all 0's

  The payload size in IPv6 header needs to be calculated by you

  If you see "Unable to checksum IP Proto 0x0a" verify you are using the IPv6 object


#######################

====================================
LAB 3A
====================================

Generate a valid IPv6 Neighbor Solicitation to your classmate, that elicts a neighbor advertisement.

Ensure both the solicitation and advertisement are viewable in Wireshark

Valid means it conforms the RFC, Wireshark confirms it is not malformed/displays no errors, and your request produces a reply

Depending on the setup of an OS, there MIGHT be a timeout on how many Neighbor Advertisements can be sent out in a period of time. If there is nothing else wrong with your code, wait 2-3 mins and try again.

(DOES the SOURCE LINK LAYER option avoid the timer?)

#######################

====================================
LAB 3B
====================================

Create a valid Neighbor Advertisement. You will only see the advertisement, there is no network reply.

Valid means it conforms the RFC, Wireshark confirms it is not malformed/displays no errors.

Validate with 'ip -6 neighbor show' on your classmate's system

#######################


====================================
LAB 3C
====================================

Generate a valid IPv6 Router Solicitation to the class server, that elicts a router advertisement.

Ensure both the solicitation and advertisement are viewable in Wireshark

Valid means it conforms the RFC, Wireshark confirms it is not malformed/displays no errors, and your request produces a reply

#######################


====================================
LAB 3D
====================================

Generate a valid IPv6 Router Advertisement to the class server. Use a timeout of 256.

You will see your link-local IPv6 address show up on screen as a "default" route

Ensure the advertisement is viewable in Wireshark

Valid means it conforms the RFC, Wireshark confirms it is not malformed/displays no errors, and your request produces a route on the server (will be displayed on screen)

Your RA will put your link-local address on the screen as 'default'


#######################



====================================
LAB 3E
====================================

Modify your Router Advertisement to actually advertise a network prefix instead of displaying your link-local IPv6 address as "default" on the server.

You may choose your own prefix, however it must NOT be for the a:c:7:9 network

Your RA will put your advertised prefix above the "default" ones

Hint: Flags




====================================
LAB 3F
====================================

Create a valid Redirect message that redirects traffic to b:c:7:9::100 through b:c:7:9::200

Valid means it conforms the RFC, and Wireshark confirms it is not malformed/displays no errors.


#######################



====================================
LAB 3G
====================================

Add an optional header to each of your Router Solicitation, Neighbor Solicitation, and Redirect message

#######################


====================================
LAB 3 BONUS
====================================

Create a raw socket that can handle ICMP traffic

Generate a ping packet and send it.

Validate you can recieve the response on your initial socket.

Use struct to unpack the values into the ICMPv6 header. Print the name of each field, it's width, and the value

#######################

====================================
References
====================================

RFC:

    IPv4 - https://tools.ietf.org/html/rfc791

    IPv6 - https://www.ietf.org//html/rfc2460

    NDP - https://tools.ietf.org/html/rfc4861

    ICMPv6 - https://tools.ietf.org/html/rfc4443

    ICMP - http://www.faqs.org/rfcs/rfc792.html




Values for IPv4 Protocol Field/ IPv6 Next Header Field:
    http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

ICMP Messages:

    https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol

IPv6 Address Multicast Addresses

    http://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xhtml

#######################


====================================
Layer 3 Overview
====================================

IPv4

IPv6

CIDR notation

ICMP

Routing

NDP/ICMPv6
