#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import os

ssh_terminals = {}

def ssh( login, command, debug=False ):
	import paramiko
	if not login in ssh_terminals.keys():
		ssh_terminals[login] = paramiko.SSHClient()
		ssh_terminals[login].set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		s = login.split('@')
		ssh_terminals[login].connect(s[1], username=s[0])
	if debug:
		print command
	stdin, stdout, stderr = ssh_terminals[login].exec_command(command)
	result = (''.join(stdout.readlines())).strip()
	if debug:
		print result
	return result

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

# Bash guide: http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html
#def bash( login, script ):
#	return ssh( login, '/bin/bash -c '+script )

def listdir( folder ):
	result = ssh( login(folder), 'ls -1 "'+path(folder)+'"' ).split('\n')
	if result != ['']:
		return result
	else:
		return []

def isdir( thing ):
	return ssh( login(thing), "if [ -d '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

def mkdir( folder ):
	return ssh( login(folder), 'mkdir "'+path(folder)+'"' )

def rmdir( folder ):
	return ssh( login(folder), 'rmdir "'+path(folder)+'"' )

def exists( thing ):
	return ssh( login(thing), "if [ -e '"+path(thing)+"' ]; then echo true; else echo false; fi" )=='true'

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
	from scp import scp
	scp(source, target)

def move( source, target ):
	from scp import scp
	scp(source, target)
	remove(source)

