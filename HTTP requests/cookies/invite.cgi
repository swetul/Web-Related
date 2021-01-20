#!/usr/bin/python

from os import environ

# Check for cookies

name = None
attending = False
if 'HTTP_COOKIE' in environ and len(environ['HTTP_COOKIE']) > 0:
    # There is a cookie. They are key-value pairs
    # Could grab all the keys, but are only concerned with 2.
    cookies = environ['HTTP_COOKIE'].split(';')
    for cook in cookies:
        print(cookies)
        (key, value) = cook.split('=')
        key = key.strip()
        value = value.strip()
        if key == 'name' and len(value) > 0:
            name = value
        if key == 'attending' and value == 'True':
            # parse this one manually with the if above
            attending = True

# now... do we have valid info?
if name is not None:
    # Yes! print out the status
    print('Content-Type: text/html')
    print("")
    report = open(
        '/home/student/patels15/public_html/cookies/info.html').read()
    status = ''
    if not attending:
        status = 'not '
    print(report.format(name, status))
else:
    # No! Print out the Form
    print('Content-Type: text/html')
    print("")
    theForm = open(
        '/home/student/patels15/public_html/cookies/form.html').read()
    print(theForm)
