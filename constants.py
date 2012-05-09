#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

scp_plus = 0
smv = 1
smerge = 2

def Usage():
	from fs import fname
	from sys import argv
	print 'Usage: '+fname(argv[0])+' source1 source2 ... target/'
