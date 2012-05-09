#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from constants import *
from fs import *
from os.path import join
from utils import format
from transfer import scp
from threading import Thread
import settings as x

def hash_both(source, target):
	def HashSource():
		x.sourcehash = md5sum(source)
		print '\t'+source+': '+x.sourcehash
	thread1 = Thread( target=HashSource )

	def HashTarget():
		x.targethash = md5sum(target)
		print '\t'+target+': '+x.targethash
	thread2 = Thread( target=HashTarget )

	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()

def transfer_to_target(source, target):

	print '--- '+source+' ---'

	corresponding_target = join(target, fname(source))
	print '\tTarget: '+corresponding_target

	if isdir(source):
		print '\tSource is a directory. Entering ...'
		for item in listdir(source):
			transfer_to_target(join(source, item), corresponding_target)
		print '\tLeaving '+source+' ...'
		if x.behavior in [smv, smerge]:
			try:
				rmdir(source)
			except:
				print 'FAILED TO REMOVE DIRECTORY'
		return

	elif isfile(source):
		print '\tSource is a file.'

		if not exists(corresponding_target):
			print '\tCorresponding target doesn\'t exist.'
			if not exists(target):
				mkdir(target)
			scp(source, target)
			hash_both(source, corresponding_target)
			if x.sourcehash == x.targethash and x.behavior in [smv, smerge]:
				remove(source)
			return

		elif isdir(corresponding_target):
			print 'Aborting: Unmergeable: Source File and Target Directory.'
			return

		elif isfile(corresponding_target):
			print '\tTarget exists and is a file.'

			sourcesize = getsize(source)
			print '\t'+source+': '+format(sourcesize)
			targetsize = getsize(corresponding_target)
			print '\t'+corresponding_target+': '+format(targetsize)

			if sourcesize == targetsize:

				hash_both(source, corresponding_target)
				if x.sourcehash != x.targethash:
					if x.behavior != smerge:
						print 'Aborting: Same filesize but content binary differs.'
						return
					else:
						_source += '.'+x.sourcehash
						print '\tDifferent file. Saving as '+_source+'.'
						move(source, _source)
						transfer_to_target(_source, target)
						return
				else:
					print '\tSuccess: File complete. Content binary equal.'
					if x.behavior in [smv, smerge]:
						remove(source)
					return

			elif sourcesize > targetsize:	# smaller

				blocksize = 256*1024
				pos = (targetsize / blocksize) * blocksize

				def HashSource():
					x.sourcehash = md5sum(source, end=targetsize)
					print '\t'+source+' (partial): '+x.sourcehash
				thread1 = Thread( target=HashSource )

				def HashTarget():
					x.targethash = md5sum(corresponding_target)
					print '\t'+corresponding_target+': '+x.targethash
				thread2 = Thread( target=HashTarget )

				thread1.start()
				thread2.start()
				thread1.join()
				thread2.join()

				if x.sourcehash != x.targethash:
					print 'Aborting: Partial content binary differs.'
					return
				else:
					from utils import run
					from fsremote import login, path
					if pos == 0:
						print '\tRestarting transfer ...'
						remove(corresponding_target)
						scp(source, target)
						hash_both(source, corresponding_target)
						if x.sourcehash == x.targethash and x.behavior in [smv, smerge]:
							remove(source)
						return
					else:
						print '\tContinuing transfer ...'
						truncate(corresponding_target, pos)
						run('dd if="'+source+'" bs='+str(blocksize)+' skip='+str(pos/blocksize)+' | ssh -C '+login(target)+' dd of="'+path(corresponding_target)+'" bs='+str(blocksize)+' seek='+str(pos/blocksize))
						hash_both(source, corresponding_target)
						if x.sourcehash == x.targethash and x.behavior in [smv, smerge]:
							remove(source)
						return


			elif sourcesize < targetsize:	# bigger
				print 'Aborting: Target file is bigger.'
				return

