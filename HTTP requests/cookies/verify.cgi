#!/usr/bin/python

from os import environ
import sys
import re


def hasAChar(theString):
    match = re.search('[A-Za-z]', theString)
    return match is not None


# get the body
valid = False
theName = "(you did't even write anything)"

length = 0
if 'CONTENT_LENGTH' in environ:
    length = int(environ['CONTENT_LENGTH'])


body = sys.stdin.read(length)

# body should be formatted: name=adsadd&attending=on
# but checked may or may not be in the string
parts = body.split('&')
attending = False
for part in parts:
    # split it
    key = None
    value = None
    out = part.split('=')
    if len(out) >= 2:
        key = out[0]
        value = out[1]

    if key == 'name' and len(value) > 0:
        theName = value
        valid = hasAChar(theName)
    if key == 'attending' and value == 'on':
        attending = True


# now... do we have valid info?
if valid:
    print('Content-Type: text/html')
    print("Set-Cookie: name={0}".format(theName))
    print("Set-Cookie: attending={0}".format(attending))

    print("")
    page = open('/home/student/patels15/public_html/cookies/info.html').read()
    status = ''
    log = open('/home/student/patels15/public_html/cookies/list.txt', 'a')
    if not attending:
        status = 'not '
        log.write("{:s} not coming\n".format(theName))
    else:
        log.write("{:s} attending\n".format(theName))

    log.close()
    print(page.format(theName, status))
else:
    print('Content-Type: text/html')
    print("")
    err = open('/home/student/patels15/public_html/cookies/error.html').read()
    print(err.format(theName))
