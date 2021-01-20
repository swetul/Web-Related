#!/usr/bin/python

import sys
import os
from os import environ

length = 0
if 'CONTENT_LENGTH' in environ:
    length = int(environ['CONTENT_LENGTH'])

body = sys.stdin.read(length)

parts = body.split('&')
form = {}
for part in parts:
    # split it
    key = None
    value = None
    out = part.split('=')
    if len(out) >= 2:
        key = out[0]
        value = out[1]
        form[key] = value

print('''Content-type: text/html

<html>
<body>

<p>Hello {:s} from the family {:s}</p>

<a href="./">Back</a>
'''.format(form['firstname'], form['lastname']))
