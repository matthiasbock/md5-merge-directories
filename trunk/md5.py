#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

def largefileMD5( filename ):
	import hashlib
	global md5, Buffer, nextBuffer
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()

def md5sum( filename, end=None ):
	from utils import run, ggT
	if end is None:
		return run('md5sum "'+filename+'"')[:32]
	else:
		buffersize = ggT( 1024**2, end )
		count = end/buffersize
		return run('dd if="'+filename+'" bs='+str(buffersize)+' count='+str(count)+' | md5sum')[:32]

