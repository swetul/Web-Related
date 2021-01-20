#!/usr/bin/python

import sys
import os
from os import environ
import cgi

form = cgi.FieldStorage()


print('''Content-type: text/html

<html>
<body>

<p>Hello {:s} from the family {:s}</p>

<a href="./">Back</a>
'''.format(form.getvalue('firstname'), form.getvalue('lastname')))
