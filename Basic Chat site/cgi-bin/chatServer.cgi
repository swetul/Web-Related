#!/usr/bin/python3

# SWETUL PATEL 
# chatServer.py

import re
import sys
import urllib
from os import environ
import json


database = {}

# read the messages
msgSize = 0
with open("Messages.txt","r") as rFile:
    msgSize = int(rFile.readline().strip())
    data = rFile.readline().strip()
rFile.close()

database = json.loads(data)


#read request body data
nameInput = sys.stdin.readline()
nameInput = nameInput.strip()
inputs = {}
requestType = "GET"

if nameInput != '':
    requestType = "POST"
    if "*&*" in nameInput:
    	#split the request body
    	for pair in nameInput.split('*&*'):
            (key, val) = pair.strip().split('=', 1) 
            inputs[key] = val




resultString = ''
# Get request
if requestType == "GET":
    #print("GET request:")
    resultString +=  json.dumps(database)
    contentLength = len(resultString)
    print("Content-type: text/plain")
    print("Content-length: " + str(contentLength)+"\r\n")
    print(resultString)

# POST request
else:
    #print("POST request")
    if inputs["Command"] == "ADD":
        #print(msgDict)
        msgSize = msgSize + 1
        msgSize = str(msgSize)
        addToTxt = "msgID"+msgSize
        tempDict= {}
        tempDict["Name"] = inputs["Name"]
        tempDict["Message"] = inputs["Message"]
        database[addToTxt] = tempDict
    
    elif inputs["Command"] == "DELETE":
        del database[inputs["msgID"]]


    with open("Messages.txt","w") as rFile:
        dataStr = json.dumps(database)
        rFile.write(str(msgSize)+"\n"+dataStr)
    rFile.close()
    print("Content-type: text/plain\r\n")
