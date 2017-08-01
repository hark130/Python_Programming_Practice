:title: Introduction to Network Programming
:data-transition-duration: 1500
:css: networking.css

====================================
Higher Level Protocols
====================================

Basics of Layer 7 and other useful functionality

#######################

====================================
Layer 7 Overview  
====================================

- Introduction to DNS

- FQDNs

- DNS Record Format

- SOA Records

- A/AAAA Records

- CNAME Records

- MX Records

- SRV Records

- DNS Tiers

- DNS Resolution

- Introduction to HTTP

- HTTP Requests

- HTTP Response

- HTTP Status Codes


#######################

====================================
DNS
====================================

Domain names are for the benefit of humans. 

IPs are difficult to remember, and if they change it is almost impossible to fully advertise the new IP to everyone.

DNS maps domain names to IPs, and can advertise the services each domain offers (HTTP, MAIL, etc)

Operates on UDP port 53

#######################

====================================
FQDN
====================================
FQDN - Fully Qualified Domain Name, the complete domain name of a host, which combines the network domain with the host's name

    mail3.example.com

A typical domain name used to access a website is NOT a FQDN because that domain does not reference a not specific host, but one of several that can serve webpages for that domain.

    www.example.com may ultimately resolve to webserver.example.com or www2.example.com

A technically correct a FQDN ends with a . as a reference to the root domain
    - While it is the best kind of correct, this isn't always reflected in reality

#######################


====================================
DNS Records - Format
====================================
Owner - Name of domain

TTL - TTL in seconds

Class - Protocol family to use, almost always IN

Type - Type of record being returned

RDATA - Data of the record



#######################



====================================
DNS - SOA Records
====================================

Start of Authority records identify information about the domain,

This also serves as the authoritatve copy that keeps secondary DNS servers up to date


In addition to the DNS record fields, it contains more information

    Authoritative server - Primary DNS for the zone

    Respsonible person - Email address of admin, with @ replaced by .

    Serial Number - Current "version number", used by secondary DNS to determine whether they should update

    Refresh - Number of second between each secondary DNS checks for updates

    Retry- Number of seconds to wait for secondary DNS to re-try a zone transfer

    Expire - TTL of zone transfer for secondary DNS

    Minimum TTL - The minimum TTL for all records in the zone

#######################


====================================
DNS - A and AAAA Records
====================================

Map domain name to IP

Sometimes the IPv6 one will be called a "quad-A"

::

    noamdc1 IN A 172.16.48.1

    noamdc1 IN AAAA 2001:db8::ff00:42:8329


#######################


====================================
DNS - PTR Records
====================================

Maps IP to FQDN

::

    1.48.16.172.in-addr.arpa. IN PTR noamdc1.noam.reskit.com.

    9.2.3.8.2.4.0.0.0.0.f.f.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. 1h IN PTR host1.example.com.

There are several things of note:
  - The IP is backwards
  - The string 'in-addr.arpa.' is appended to the reversed IP
  - 'in-addr.arpa.' ends with a .
  - The IPv6 address is not in a traditional format (http://rdns6.com/hostRecord)

#######################


====================================
DNS - CNAME
====================================
Canonical Name, an alias for a specific FQDN.

::
    
    ftp.noam.reskit.com. IN CNAME ftp1.noam.reskit.com.

According to RFC 2181, there must be only one canonical name per alias.


#######################


====================================
DNS - MX Records
====================================

Provides the mailservers for the FQDN. There can be multiple listings

::

    *.noam.reskit.com. IN MX 0 mailserver1.noam.reskit.com.

    *.noam.reskit.com. IN MX 10 mailserver2.noam.reskit.com.

    *.noam.reskit.com. IN MX 10 mailserver3.noam.reskit.com. 

#######################


====================================
DNS - SRV records
====================================

These allow domains to identfy the services offered and the hosts responsible for providing the services 

Service - name of the service (http, telnet, etc)

Proto - Usually the Layer 4 protocol

Domain - Domain this applies to

TTL/Class - Same as other DNS records

Priorty - Lower number =  higher priority. Higher priortity hosts get contacted first

Weight - Used to load balance hosts with identical Priorities

Port - Port of servce

Target - FQDN for service host

::

    _http._tcp.reskit.com. IN SRV 0 0 80 webserver1.noam.reskit.com.

    _http._tcp.reskit.com. IN SRV 10 0 80 webserver2.noam.reskit.com. 

#######################



====================================
DNS Resolution
====================================

Resolving addresses are performed with DNS Request messages. 

DNS requests may be iterative or recursive. At almost every step, the cache of the current system is checked before attempting another query to reduce the load on higher servers. 

Recursive requests allow the recipient of a DNS query to make it's own DNS query. That recipient can make it's own query if needed. This is the typical method.

Iterative requests mean the host expects the DNS server to reply immediately, without asking any other DNS servers. The reply will either be from the cache, or a referral to another name server. Iterative requests may then be made by the initial host if needed.




#######################


====================================
DNS Tiers
====================================

There are several tiers of name servers in DNS

The root servers (there are 13 A-M) are the masters. Their purpose to to point at the TLD servers

Top Level Domain servers handle the .com, .net, .io, etc. They will point you to the specific name server

Domain nameserver (e.g microsoft.com, code.io) handles the resolution for the whole domain. There may be other tiers beneath this for specific subdomains



#######################


====================================
Dig, replacement for nslookup
====================================

dig [+short] [@nameserver to query] host type, [host type]

ex. 
dig +short google.com A google.com AAAA
dig google.com SOA

[user@localhost Desktop]$ dig google.com A google.com AAAA

; <<>> DiG 9.10.4-P4-RedHat-9.10.4-2.P4.fc24 <<>> google.com A google.com AAAA
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30293
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.            IN  A

;; ANSWER SECTION:
google.com.     118 IN  A   216.58.194.78

;; Query time: 37 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Dec 01 23:08:46 CST 2016
;; MSG SIZE  rcvd: 55

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 22402
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.            IN  AAAA

;; ANSWER SECTION:
google.com.     299 IN  AAAA    2607:f8b0:4000:802::200e

;; Query time: 36 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Dec 01 23:08:46 CST 2016
;; MSG SIZE  rcvd: 67

[user@localhost Desktop]$ dig +short google.com A google.com AAAA
216.58.218.206
2607:f8b0:4000:802::200e

====================================
Introduction to HTTP
====================================

HTTP is a string based protocol. 

HTTP Requests are sent with several broad categories of information
    - The resource requested and it's location (index.html at example.com)
    - Information about the expected result (type of data, language, etc)
    - Any supplemental data needed to process the request (form data, parameters, etc)


HTTP Responses usually containt
    - The result of the transaction (status codes)
    - Metadeta about the transaction (date, webserver, content length and type)
    - The data

#######################


====================================
HTTP Line Breaks
====================================

An HTTP line break is a carriage return followed by a newline (\\r\\n)

A blank line with a single \\r\\n signifies the end of a header
     - This ends a request, and seperates the data from the header in a response

#######################



====================================
HTTP Requests
====================================

The only MANDATORY parts of an HTTP Request are the verb, the URL, HTTP version, and the host (and any data you need to send if POSTING)

We will only discuss the verbs GET and POST because they are almost exclusively what you will encounter, however others do exist. 

Example 1

::

    GET /hello.htm HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.example.com
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive

Example 2

::

    POST /cgi-bin/process.cgi HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: www.tutorialspoint.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: length
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive

    licenseID=string&content=string&/paramsXML=string

Example 3

::

    BREW /pot-4 HTCPCP/1.0
    Host: 120.0.0.1
    Content-Type: message/coffeepot
    Accept-Additions: cream;1,whisky;3,rum;5



#######################


====================================
HTTP Responses
====================================

HTTP Responses conclude that particular transaction. Other transactions may be required to get other resources found on the page. Remember that \\r\\n seperates the header from the actual data.

Example 1

::

    HTTP/1.1 200 OK
    Date: Mon, 27 Jul 2009 12:28:53 GMT
    Server: Apache/2.2.14 (Win32)
    Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
    Content-Length: 88
    Content-Type: text/html
    Connection: Closed

    (APPROPRIATE DATA HERE)

Example 2

::

    HTTP/1.1 404 Not Found
    Date: Sun, 18 Oct 2012 10:36:20 GMT
    Server: Apache/2.2.14 (Win32)
    Content-Length: 230
    Connection: Closed
    Content-Type: text/html; charset=iso-8859-1

    (APPROPRIATE DATA HERE)

Example 3

::

    HTCPCP/1.0 418 I'm a teapot


#######################


====================================
HTTP Status Codes
====================================

Status codes are a 3 digit number to tell you the result of the transaction.

Below are some common ones

100 Series, Informational
    - 100 Continue

200 Series, Successful responses
    - 200 OK - Your response will be in the data

300 Series, Redirection
    - 301 Moved Permenantly - new URI likely provided in data
    - 307 Temporary Redirect - Use this new URI now and same VERB to repeat the transaction
    - 308 Permenant Redirect - Use this new URI permentantly and same VERB to repeat the transaction

400 Series, Client Error
    - 400 Bad Request - Your request was not understood
    - 403 Forbidden - No access rights to URI
    - 404 Not Found - No such URI
    - 418 I'm a teapot - Coffee is poison!

500 Series, Server Error
    - 500 Internal Server Error - Something probably errored/crashed while processing your request
    - 503 Server Unavailable - No server can handle the request at this time. May include a "Retry-After" key-value pair



====================================
JSON
====================================

JavaScript Object Notaton

It's a human readable data interchange format. The data is defined using key value pairs.

JSON is used to pass structured data around. This can be a database record, the representation of an object, or configuration or staus messages. It is used because processing markup language (XML, HTML, etc) properly is difficult and expensive

In Python, it's basially a dictionary represented as a string and sent across the wire




#######################



====================================
JSON in Python Strings
====================================

There are only two functions that you use to transmit and receive JSON data:

json.dumps() - Dump a dict variable to a string. Will convert numbers to ints/floats

json.loads() - Load a string into a dict variable


You can also specify add a second parameter to parse numbers like floats and ints into Python's Decimal object. 

parse_int=Decimal

parse_float=Decimal


ref: http://www.yilmazhuseyin.com/blog/dev/advanced_json_manipulation_with_python/

#######################


====================================
Struct
====================================

Struct allows you to pack values into specified data types and sizes. Instead of manually parsing a chunk of data, struct will do it for you and provide you a list of the values.

We used this function call in the IPv6 multicast lab

This is how you would transfer binary data over the wire. It has an options for NETWORK BYTE ORDER

It uses a format string and variable arguments (like print or printf in C)

See: https://docs.python.org/2.7/library/struct.html#

#######################


====================================
Select()
====================================

Select() is a a potential solution for when you want to open multiple sockets for communication, but don't want your receive/send functions to block and hold up your program

Select is a Linux function call that operates on file descriptors. In Linux specifically, everything is a file. This means at it's core in Linux, a network socket is a file descriptor.

Since it's a syscall, it works in C, Python, and any other language you can make syscalls from (in Linux anyway)

Caveat: I have never tried using select outside of Linux 

#######################


====================================
Select - Socket setup
====================================

We need to import select, and set our sockets to be non-blocking


::

    import select
    ...

    p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    p1.setblocking(0)
    p1.bind( ('', 2000) )
    p1.listen(1)

    p2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2.setblocking(0)
    p2.bind( ('', p2port) ) 
    p2.listen(1)



#######################



====================================
Select - Setting up call
====================================

Select() takes 3 parameters, each is a list of file descriptors. 

The first parameter is for reads

The second parameter is for writes

The third parameter to see if there is any fds that threw an exception

FDs can be in multiple lists

::

    # Sockets to which we expect to read
    inputs = [ p1, p2 ]

    # Sockets to which we expect to write
    outputs = [ ]

    readable, writable, exceptional = select.select(inputs, outputs, inputs)    

#######################


====================================
Select - Using it
====================================

You do NOT need to use all return values in the for-loops below. If you only care about reading, then omit the remaining two loops.

The returned lists may also can be handled in any order. If you prioritize writes, handle that list first. 

Remember that the parameters and return values are all Python lists. There is NO guarantee of order of sockets within those lists

::

    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)    

        for s in readable:
            # compare s to your socket list to find out which one it is
            # read incoming data and handle it

        for s in writeable:
            # compare s to your socket list to find out which one it is
            # identify data that goes to that socket, and write it

        for s in exceptional:
            # compare s to your socket list to find out which one it is
            # handle the exception
            # You may have internal states to keep track of. Update them now 
                (e.g. is the user logged in? How far along in a buffer are you)


#######################





====================================
Lab 4A
====================================

Write a Python script to download the index.html file on the webserver. Parse the data and write only the actual html page to disk.


Hint: Linux has a program called 'xxd'. It is a hex editor for files. If you are unable to open your downloaded files, use xxd to determine if you properly parsed everything.



#######################

===================================
Lab 4B
====================================

Use the struct library and package both ICMP and TCP header values into a variable using an appropriate format string. Use your layer 4 labs for sample values. 

Print the data returned by packing, print the packed data using repr(), and then print the size of the packed data.

Validate that your sizes are correct with the actual sizes of eahc field in those headers


#######################

===================================
Lab 4C
====================================

Write a TCP server that listens on port 2222 for a string. Have the server split the string into words (space seperated) and send each word to a random port from the list below. 

    If the random port picked has already been used to transmit, it is ok to use it again

Write a TCP client that sends a sentence over port 2222, then listens on all ports below and uses select() to reconstruct the sentence as its sent back from the server.

Port list =  2345, 1789, 9999, 65233, 25000, 33912, 5901, 2223, 8768, 43848, 4432, 7292, 13666



#######################

===================================
Lab 4D
====================================

Write a Python script to request JSON data from the server.

Print each value returned, and its type.

ex:

::
dig
'my string': string
1: int

#######################


====================================
Layer 7 Overview  
====================================

DNS maps words to IP 

DNS also provides supplementary data about those domains via records

HTTP uses a transaction of Request and Response

HTTP Uses status codes to communicate the result of a request along with any data
