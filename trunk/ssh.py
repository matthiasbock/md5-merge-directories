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

def ssh( command ):
	...


def listdir( folder ):
	return os.listdir( folder )

def isdir( thing ):
	return os.path.isdir( thing )

def mkdir( folder ):
	return os.mkdir( folder )

def rmdir( folder ):
	return os.rmdir( folder )

def exists( thing ):
	return os.path.exists( thing )

def getsize( filename ):
	return os.path.getsize( filename )

def md5sum( filename ):
	return largefileMD5( filename )

def islink( thing ):
	return os.path.islink( thing )

def readlink( link ):
	return os.readlink( link )

def copy( source, target ):
	return shutil.copy( source, target )

def move( source, target ):
	return shutil.move( source, target )

def remove( filename ):
	return os.remove( filename )

