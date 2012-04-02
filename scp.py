#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from sys import argv
from subprocess import Popen

Continue = False
TarBz = False
first = 0
host1 = ""
host2 = ""
for arg in argv:
	a = arg.lower()
	if 'scp.py' in a:
		first = argv.index(arg)
	elif ':/' in a:
		if host1 == '':
			host1 = arg
		else:
			host2 = arg
	elif a == '--tar.bz':
		TarBz = True
		del arg
	elif a == '--continue':
		Continue = True
		del arg
first += 1

if TarBz:
	if host1 is local:
		Popen tar -c --remove-files -jf folder.tar.bz
	else:
		ssh host1 tar...
	scp host1:/folder.tar.bz to host2
	if host1 is local:
		rm folder.tar.bz
	else:
		ssh host1 rm folder.tar.bz
	if host 2 is local:
		Popen tar unpack
		rm tar
	else:
		ssh host2 tar -xjf folder.tar.bz
		ssh host2 rm folder.tar.bz
else:
	print "Operation not yet supported."

