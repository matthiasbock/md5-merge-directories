#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from subprocess import Popen, PIPE
from shlex import split

def is_remote( url ):
	a = url.find('@')
	b = url.find(':/')
	if b < 0:
		b = url.find(':~')
	c = url.find('/')
	return ( a > -1 and b > -1 and a < c and b < c  and a < b )


def login( url ):
	return url[:url.find(':')]

def path( url ):
	return url[url.find(':')+1:]


def ssh( login, command ):
	print "ssh "+login+" "+command
	p = Popen( ["ssh", login, command], stdout=PIPE )
	out = [line.strip() for line in p.stdout.readlines()]
	return '\n'.join( out )

# see also: http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html

#def bash( login, script ):
#	return ssh( login, '/bin/bash -c '+script )


def listdir( folder ):
	return ssh( login(folder), 'ls -1 "'+path(folder)+'"' ).split('\n')

def isdir( thing ):
	return ssh( login(thing), "if [ -d '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

def mkdir( folder ):
	return ssh( login(folder), 'mkdir "'+path(folder)+'"' )

def rmdir( folder ):
	return ssh( login(folder), 'rmdir "'+path(folder)+'"' )

def exists( thing ):
	return ssh( login(thing), "if [ -e '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

def scp( source, target ):
	print "scp -Cpr "+source+" "+target
	Popen( ["scp", "-Cpr", source, target] ).wait()
	if not exists(source) or not exists(target):
		raise	# should be fatal, else the file may accidently be deleted permanently

def getsize( filename ):
	return int(ssh( login(filename), "stat -c %s '"+path(filename)+"'" ))

def md5sum( filename ):
	return ssh( login(filename), 'md5sum "'+path(filename)+'"' )[:32]

def isfile( thing ):
	return ssh( login(thing), "if [ -f '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

def islink( thing ):
	return ssh( login(thing), "if [ -h '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

def readlink( link ):
	return ssh( login(link), "readlink '"+path(link)+"'" )

def remove( filename ):
	ssh( login(filename), 'rm "'+path(filename)+'"' )

def copy( source, target ):
	scp(source, target)

def move( source, target ):
	scp(source, target)
	remove(source)

