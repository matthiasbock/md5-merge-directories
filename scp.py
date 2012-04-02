#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from sys import argv, exit
from subprocess import Popen
from shlex import split
from ssh import *


# Console argument parsing

args = {'--pack':False,
	'--unpack':False,
	'--continue':False,
	'--hash':False,
	'--remove-equal':False }
first = 0
source = ""
target = ""
for arg in argv:
	a = arg.lower()
	if 'scp.py' in a:
		first = argv.index(arg)
	elif '/' in a:
		if source == '':
			source = arg
		else:
			target = arg
	else:
		for x in args.keys():
			if a == x:
				args[x] = True
				del arg
first += 1


# Checking arguments ...

if source == "" or target == "":
	print "insufficient arguments"
	exit()
if source[len(source)-1] == '/':	# path ends with / : remove it (the parent folder is meant)
	source = source[:-1]
if target[len(target)-1] == '/':	# path end with / : add source's name (the subfolder is meant)
	d = path(source).split('/')
	name = d[len(d)-1]
	target += name
print 'Source: '+source
print 'Target: '+target
unpacked_source = source
unpacked_target = target


# Pack the source

if args['--pack']:
	print 'Packing source ...'
	p = path(source)
	tar_cmd = 'tar -c  -jf "'+p+'.tar.bz" "'+p+'"' #--remove-files
	print tar_cmd
	if is_remote(source):
		ssh(login(source), tar_cmd)
	else:
		Popen(split(tar_cmd)).wait()
	source += '.tar.bz'
	target += '.tar.bz'

exit()

print 'Transfering ...'
scp(source, target)

"""	if source is local:
		rm folder.tar.bz
	else:
		ssh source rm folder.tar.bz

if args['--unpack']:
	if host 2 is local:
		Popen tar unpack
		rm tar
	else:
		ssh target tar -xjf folder.tar.bz
		ssh target rm folder.tar.bz
	source = unpacked_source
	target = unpacked_target
"""
