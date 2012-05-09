#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

def largefileMD5( filename, end=None ):
	import hashlib
	global md5, Buffer, nextBuffer
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		if end is None:
			for chunk in iter(lambda: f.read(8192), ''): 
				md5.update(chunk)
		else:

			# hier ist irgendwie der Wurm drinn
			# liefert falsche MD5-Summen

			from os.path import getsize
			size = getsize(filename)
			at_once = (1024**2)		# 1 MB
			blockcount = int(size/at_once)
			remaining = size % at_once
			print str(blockcount)+' * '+str(at_once)+' + '+str(remaining)+' = '+str(size)

			from threading import Thread

			def read():
				global nextBuffer
				nextBuffer = f.read(at_once)

			def update():
				global md5, Buffer
				md5.update( Buffer )

			if blockcount > 0:
				Buffer = f.read(at_once)
				for i in range(blockcount-1):
					thread1 = Thread( target=update() )
					thread2 = Thread( target=read() )
					thread1.start()
					thread2.start()
					thread1.join()
					thread2.join()
					Buffer = nextBuffer
				md5.update( Buffer )

			if remaining > 0:
				md5.update( f.read(remaining) )

	return md5.hexdigest()

def md5sum( filename, end=None ):
	from utils import run, ggT
	if end is None:
		return run('md5sum "'+filename+'"')[:32]
	else:
		buffersize = ggT( 1024**2, end )
		count = end/buffersize
		return run('dd if="'+filename+'" bs='+str(buffersize)+' count='+str(count)+' | md5sum')[:32]

