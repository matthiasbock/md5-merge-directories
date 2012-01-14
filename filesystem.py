#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import os, shutil
from helper import largefileMD5

def listdir( folder ):
	return os.listdir( folder )

def isdir( thing ):
	return os.path.isdir( thing )

def exists( thing ):
	return os.path.exists( thing )

def islink( thing ):
	return os.path.islink( thing )

def mkdir( folder ):
	return os.mkdir( folder )

def rmdir( folder ):
	return os.rmdir( folder )

def copy( source, target ):
	return shutil.copy( source, target )

def move( source, target ):
	return shutil.move( source, target )

def readlink( link ):
	return os.readlink( link )

def remove( filename ):
	return os.remove( filename )

def getsize( filename ):
	return os.path.getsize( filename )

def md5sum( filename ):
	return largefileMD5( filename )

