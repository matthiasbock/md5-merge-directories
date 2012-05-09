#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

def scp( source, target, debug=False ):
	from fs import exists, isdir
	from subprocess import Popen
	from shlex import split

	cmd = ['scp', '-Cpr', source, target.replace(' ', '\ ')]
	if debug:
		print ' '.join(cmd)
	Popen(cmd).wait()

	success = exists(source) and exists(target)
	if debug:
		print 'Success: '+str(success)

	return success
