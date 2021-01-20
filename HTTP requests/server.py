#!/usr/bin/python

# SWETUL PATEL
# chatServer.py

import os
import subprocess
import socket
import sys

# server info
host = socket.gethostname()
port = 15024
addr = ("", port)

# create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# functions to support server


def beginServer():
    try:
        serverSocket.bind(addr)
    except Exception as exc:
        print(exc)

    # listen for connections
    serverSocket.listen(socket.SOMAXCONN)
    socketConnected()

# function to be run when a socket has sent a connection request


def socketConnected():
    # while connection is still active
    while True:
        returnSocket, returnAddress = serverSocket.accept()
        requestRAW = returnSocket.recv(4096)
        # no data is received
        if not requestRAW:
            break

        # get request info
        requestText = bytes.decode(requestRAW)
        requestArray = requestText.split(' ')
        requestMethod = requestArray[0]
        requestPath = requestArray[1]

        # send request to exe
        requestResponse = fulfillRequest(
            requestMethod, requestPath, requestText)
        returnSocket.sendall(requestResponse)
        returnSocket.close()
    # end of socketConnected()

# fulfills the request


def fulfillRequest(method, path, request):

    serverResponse = ""
    headers = ""
    content = ""
    # if no path file name is given
    if path == "/":
        path = "index.html"

    # if user trys to access a directory
    if path.endswith("/"):
        path += "index.html"

# ----------------------GET AND HEAD METHOD-------------------------------------
    if method == "GET" or method == "HEAD":
        # support for GET request HEAD
        keyVal = path.split('?')

        # keyvalue pairs in request path
        if len(keyVal) > 1:
            path = keyVal[0]
            keyVal = keyVal[1]

        path = path.strip("/")
        try:
            with open(path, "rb") as rFile:
                fileContent = rFile.read()
            rFile.close()

            # cgi file processing
            if path.endswith(".cgi"):
                headers += responseHeaders(200, 'cgi')

                inp = None
                # need to process cgi script
                if len(keyVal) > 1:  # key value pair exists
                    os.environ['QUERY_STRING'] = keyVal
                    inp = keyVal.encode()

                worker = subprocess.Popen(
                    path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                (workerResponse, WorkerERR) = worker.communicate(input=inp)
                content += workerResponse

                # if cookie in response header
                if content.find("Cookie:") != -1:
                    cook = content.split("Cookie:")[1]
                    os.environ['HTTP_COOKIE'] = cook

            else:  # text or other types of files
                headers += responseHeaders(200, 'html')
                content += fileContent

            if method == "HEAD":
                headers += "Content-Length: "+str(len(content))+"\n"
                content = ''

        except Exception as exc:
            print(exc)
            headers += responseHeaders(404, 'html')
            content += """<html><body><h2> Error 404 NOT FOUND!! </h2></body><html>"""

# ---------------------POST METHOD--------------------------------------------------

    elif method == "POST":
        post = request.split("\r\n\r\n")
        postHeader = post[0]
        postBody = post[1]
        path = path.strip("/")

        try:
            with open(path, "rb") as rFile:
                fileContent = rFile.read()
            rFile.close()

            # cgi file processing
            if path.endswith(".cgi"):
                headers += responseHeaders(200, 'cgi')
                postBody = postBody.strip()

                if postHeader.find("Cookie:") != -1:
                    cook = postHeader.split("Cookie:")[1]
                    os.environ['HTTP_COOKIE'] = cook

                # need to process cgi script
                if len(postBody) > 0:  # key value pair exists
                    os.environ['CONTENT_LENGTH'] = str(len(postBody))

                #  subprocess to execute script
                worker = subprocess.Popen(
                    path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                (workerResponse, workerERR) = worker.communicate(input=postBody)

                content += workerResponse

            else:
                # text or other types of files
                headers += responseHeaders(200, 'html')
                content += fileContent

        except Exception as exc:
            print(exc)
            headers += responseHeaders(404, 'html')
            content += """<html><body><h2> Error 404 NOT FOUND </h2></body></html>"""

    else:
        headers += responseHeaders(400, 'html')
        content += """<html><body><h2> Error 400 Bad Request (i.e NOT GET/POST/HEAD) </h2></body></html>"""

    serverResponse = headers + content
    return serverResponse


def responseHeaders(code, Type):
    sendHeader = "HTTP/1.1 "
    # append status code
    if code == 200:
        sendHeader += "200 OK \n"
    elif code == 404:
        sendHeader += "404 NOT FOUND-\n"
    elif code == 400:
        sendHeader += "400 Bad request\n"
    # append status Type

    if Type == "html":
        sendHeader += "Content-Type: text/html\n\n"

    return sendHeader


# start server
beginServer()
# end of file
