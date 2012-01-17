#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import hashlib

def largefileMD5( filename ):
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()

