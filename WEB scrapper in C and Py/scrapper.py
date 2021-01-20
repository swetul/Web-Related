#!/usr/bin/python2.7

#Swetul Patel  
import socket, sys

input1 = sys.argv[1]
input2 = sys.argv[2]
print(input1,input2)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname("www-test.cs.umanitoba.ca")
print(ip)

port = 80

sock.connect((ip, port))
keyVal1 = 'Name='+ input1
keyVal2 = ''
if input2 == 'yes':
    keyVal2 = '&Attend='+input2 

keyValFull = keyVal1+keyVal2
cLen = len(keyValFull)
Host = 'Host: www-test.cs.umanitoba.ca\r\n\r\n'
request = 'POST /~patels15/cgi-bin/A1.cgi HTTP/1.1\r\nConnection: keep-alive\r\nContent-Length: '+str(cLen)+'\r\n'+Host
request += keyValFull
print(request)
sock.sendall(request.encode())
data = sock.recv(4096)

print('Received:')
print(data.decode("utf-8"))

cook1 = "Set-Cookie: Name="+input1
cook2 = "Set-Cookie: Attend="+input2
#assert to see if server set cookies
assert (data.find(cook1.encode())) != -1
assert (data.find(cook2.encode())) != -1


# send second request
cook1 = 'Cookie: Name='+input1+'; '+'Attend='+input2+';'
request = 'GET /~patels15/cgi-bin/A1.cgi HTTP/1.1\r\nConnection: keep-alive\r\n'+ cook1 +'\r\n'+Host
print(request)
sock1.connect((ip, port))
sock1.sendall(request.encode())
data = sock1.recv(4096)
# my website will redirect to search.cgi which is the invitation page that then redirects to the replied page
print('Received:')
print(data.decode("utf-8"))
