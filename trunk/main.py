#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from constants import *
from fs import *
from os.path import join
from utils import format
from threading import Thread

def hash_both(source, target):
	def HashSource():
		global sourcehash
		sourcehash = md5sum(source)
		print '\t'+source+': '+sourcehash

	thread1 = Thread( target=HashSource )

	def HashTarget():
		global targethash
		targethash = md5sum(target)
		print '\t'+target+': '+targethash

	thread2 = Thread( target=HashTarget )

	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()

	return sourcehash, targethash

def transfer_to_target(source, target):
	from transfer import scp

	print '--- '+source+' ---'

	global behavior, corresponding_target
	corresponding_target = join(target, fname(source))
	print '\tTarget: '+corresponding_target

	if isdir(source):
		print '\tSource is a directory. Entering ...'
		for item in listdir(source):
			transfer_to_target(join(source, item), join(corresponding_target, item))
		print '\tLeaving '+source+' ...'

	elif isfile(source):
		print '\tSource is a file.'

		if not exists(corresponding_target):
			print '\tCorresponding target doesn''t exist.'
			if not exists(target):
				mkdir(target)
			scp(source, target)
			sourcehash, targethash = hash_both(source, corresponding_target)
			if sourcehash == targethash and behavior == smv:
				remove(source)

		elif isdir(corresponding_target):
			print 'Aborting: Target exists and is a directory.'
			return

		elif isfile(corresponding_target):
			print '\tTarget exists and is a file.'

			sourcesize = getsize(source)
			print '\t'+source+': '+format(sourcesize)
			targetsize = getsize(corresponding_target)
			print '\t'+corresponding_target+': '+format(targetsize)

			if sourcesize == targetsize:

				sourcehash, targethash = hash_both(source, corresponding_target)

				if sourcehash != targethash:
					print 'Aborting: Content binary differs.'
					return
				else:
					print 'Success: File complete. Content binary equal.'
					if behavior == smv:
						remove(source)

			elif sourcesize > targetsize:	# smaller

				blocksize = 256*1024
				pos = (targetsize / blocksize) * blocksize

				global sourcehash, targethash
				def HashSource():
					global sourcehash
					sourcehash = md5sum(source, end=pos)
					print '\t'+source+' (partial): '+sourcehash
				thread1 = Thread( target=HashSource )
				def HashTarget():
					global targethash
					targethash = md5sum(corresponding_target, end=pos)
					print '\t'+corresponding_target+': '+targethash
				thread2 = Thread( target=HashTarget )
				thread1.start()
				thread2.start()
				thread1.join()
				thread2.join()

				if sourcehash != targethash:
					print 'Aborting: Partial content binary differs.'
					return
				else:
					from utils import run
					from fsremote import login, path
					if pos == 0:
						print '\tRestarting transfer ...'
						remove(corresponding_target)
						scp(source, target)
						sourcehash, targethash = hash_both(source, corresponding_target)
						if sourcehash == targethash and behavior == smv:
							remove(source)
					else:
						print '\tContinuing transfer ...'
						truncate(corresponding_target, pos)
						run('dd if="'+source+'" bs='+str(blocksize)+' skip='+str(pos/blocksize)+' | ssh -C '+login(target)+' dd of="'+path(corresponding_target)+'" bs='+str(blocksize)+' seek='+str(pos/blocksize))
						sourcehash, targethash = hash_both(source, corresponding_target)
						if sourcehash == targethash and behavior == smv:
							remove(source)


			elif sourcesize < targetsize:	# bigger
				print 'Aborting: Target file is bigger.'
				return

