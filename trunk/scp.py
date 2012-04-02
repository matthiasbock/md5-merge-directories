#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from filesystem import exists, isdir

def scp( source, target ):
	s = source.split('/')
	filename = s[len(s)-1]
	if target.find(filename) == len(target)-len(filename):	# wrong:  scp host1:/abc/test.tar.bz host2:/abc/test.tar.bz
		target = target[:-len(filename)]		# right:  scp host1:/abc/test.tar.bz host2:/abc/

	print "scp -Cpr "+source+" "+target
	from subprocess import Popen
	Popen( ["scp", "-Cpr", source, target] ).wait()
	if not exists(source) or not exists(target):
		raise	# should be fatal, else the file may accidently be deleted permanently

