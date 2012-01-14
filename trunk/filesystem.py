#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from helper import largefileMD5
import os, shutil
import ssh

def listdir( folder ):
	if ssh.is_remote( folder ):
		return ssh.listdir( folder )
	else:
		return os.listdir( folder )

def isdir( thing ):
	if ssh.is_remote( thing ):
		return ssh.isdir( thing )
	else:
		return os.path.isdir( thing )

def mkdir( folder ):
	if ssh.is_remote( folder ):
		return ssh.mkdir( folder )
	else:
		return os.mkdir( folder )

def rmdir( folder ):
	if ssh.is_remote( folder ):
		return ssh.rmdir( folder )
	else:
		return os.rmdir( folder )

def exists( thing ):
	if ssh.is_remote( thing ):
		return ssh.exists( thing )
	else:
		return os.path.exists( thing )

def getsize( filename ):
	if ssh.is_remote( filename ):
		return ssh.getsize( filename )
	else:
		return os.path.getsize( filename )

def md5sum( filename ):
	if ssh.is_remote( filename ):
		return ssh.md5sum( filename )
	else:
		return largefileMD5( filename )

def islink( thing ):
	if ssh.is_remote( thing ):
		return ssh.islink( thing )
	else:
		return os.path.islink( thing )

def readlink( link ):
	if ssh.is_remote( link ):
		return ssh.readlink( link )
	else:
		return os.readlink( link )

def copy( source, target ):
	if ssh.is_remote( source ) or ssh.is_remote( target ):
		return ssh.copy( source, target )
	else:
		return shutil.copy( source, target )

def move( source, target ):
	if ssh.is_remote( source ) or ssh.is_remote( target ):
		return ssh.move( source, target )
	else:
		return shutil.move( source, target )

def remove( filename ):
	if ssh.is_remote( filename ):
		return ssh.remove( filename )
	else:
		return os.remove( filename )

