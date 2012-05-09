#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

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

	global corresponding_target
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

		elif isdir(corresponding_target):
			print 'Aborting: Target exists and is a directory.'
			return

		elif isfile(corresponding_target):
			print '\tTarget exists and is a file.'

			partial = fname(source)+'.part'
			for f in listdir(target):
				if partial in f:
					print '\tMerging partial file ...'
					concatenate(corresponding_target, join(target, f))
					break

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

			elif sourcesize > targetsize:	# smaller

				def HashSource():
					global sourcehash
					sourcehash = md5sum(source, end=targetsize)
					print '\t'+source+' (partial): '+sourcehash

				thread1 = Thread( target=HashSource )

				def HashTarget():
					global targethash
					targethash = md5sum(corresponding_target)
					print '\t'+corresponding_target+': '+targethash

				thread2 = Thread( target=HashTarget )

				thread1.start()
				thread2.start()
				thread1.join()
				thread2.join()

				global sourcehash, targethash

				if sourcehash != targethash:
					print 'Aborting: Partial content binary differs.'
					return
				else:
					from utils import run, ggT

					print '\tContinuing transfer ...'
					blocksize = 10*(1024**2)
					pos = (targetsize / blocksize) * blocksize
					if pos == 0:
						remove(corresponding_target)
						scp(source, target)
						sourcehash, targethash = hash_both(source, corresponding_target)
					else:
						truncate(corresponding_target, pos)
						count = sourcesize / blocksize
						remaining = sourcesize % blocksize
						for i in range(count):
							# if islocal:
							run('dd if="'+source+'" skip='+str(pos/blocksize)+' of="'+source+'.part" bs='+str(blocksize)+' count=1')
							pos += blocksize
							scp(source+'.part', target)
							concatenate(corresponding_target, corresponding_target+'.part')
						if remaining > 0:
							run('dd if="'+source+'" skip='+str(pos/blocksize)+' of="'+source+'.part"')
							scp(source+'.part', target)
							concatenate(corresponding_target, corresponding_target+'.part')
						sourcehash, targethash = hash_both(source, corresponding_target)


			elif sourcesize < targetsize:	# bigger
				print 'Aborting: Target file is bigger.'
				return

