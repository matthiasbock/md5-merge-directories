#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-


# Constants

from constants import *


# Console argument parsing

from sys import argv, exit

sources = []
target = ''
Self = scp_plus

for i in range(1, len(argv)):
	arg = argv[i]
	if arg == '--smv':
		Self = smv
		print 'Secure move ...'
	elif arg == '--smerge':
		Self = smerge
		print 'Secure merge ...'
	elif i+1 == len(argv):
		target = arg
	else:
		sources.append(arg)

print str(len(sources))+' sources: '+sources
print 'target: '+target


# Main

from main import transfer_to_target

for source in sources:
	transfer_to_target(source, target, Self)

