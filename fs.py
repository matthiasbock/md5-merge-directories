#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import os, shutil
import fsremote

def fname(name):
	s = name.split('/')
	return s[len(s)-1]

def parent(name):
	s = name.rstrip('/').split('/')
	return '/'.join(s[:len(s)-1])

def listdir(folder):
	if fsremote.is_remote(folder):
		return fsremote.listdir(folder)
	else:
		return os.listdir(folder)

def isdir(thing):
	if fsremote.is_remote(thing):
		return fsremote.isdir(thing)
	else:
		return os.path.isdir(thing)

def mkdir(folder):
	par = parent(folder)
	if not exists(par):
		mkdir(par)
	if fsremote.is_remote(folder):
		return fsremote.mkdir(folder)
	else:
		return os.mkdir(folder)

def rmdir(folder):
	if fsremote.is_remote(folder):
		return fsremote.rmdir(folder)
	else:
		return os.rmdir(folder)

def exists(thing):
	if fsremote.is_remote(thing):
		return fsremote.exists(thing)
	else:
		return os.path.exists(thing)

def getsize(filename):
	if fsremote.is_remote(filename):
		return fsremote.getsize(filename)
	else:
		return os.path.getsize(filename)

def md5sum(filename, end=None):
	if fsremote.is_remote(filename):
		return fsremote.md5sum(filename, end)
	else:
		from md5 import md5sum as localmd5sum
		return localmd5sum(filename, end)

def isfile(thing):
	if fsremote.is_remote(thing):
		return fsremote.isfile(thing)
	else:
		return os.path.isfile(thing)

def islink(thing):
	if fsremote.is_remote(thing):
		return fsremote.islink(thing)
	else:
		return os.path.islink(thing)

def readlink(link):
	if fsremote.is_remote(link):
		return fsremote.readlink(link)
	else:
		return os.readlink(link)

def copy(source, target):
	if fsremote.is_remote(source) or fsremote.is_remote(target):
		return fsremote.copy(source, target)
	else:
		return shutil.copy(source, target)

def move(source, target):
	if fsremote.is_remote(source) or fsremote.is_remote(target):
		return fsremote.move(source, target)
	else:
		return shutil.move(source, target)

def remove(filename):
	if fsremote.is_remote(filename):
		return fsremote.remove(filename)
	else:
		return os.remove(filename)

def concatenate(file1, file2):	# cat file2 >> file1
	if fsremote.is_remote(file1):
		fsremote.concatenate(file1, file2)
	else:
		f = open(file1, 'ab')
		f.write(open(file2).read())
		f.close()
		os.remove(file2)

def truncate(filename, filesize):
	if fsremote.is_remote(filename):
		fsremote.truncate(filename, filesize)
	else:
		open(filename).truncate(filesize)

