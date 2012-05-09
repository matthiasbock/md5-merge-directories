#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from fs import *
from os.path import join
from utils import format
from threading import Thread

def transfer_to_target(source, target):

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
	#		mkdir(target)
	#		scp(source, target)
	#		validate_transfer(source, target)

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

				def HashSource():
					global sourcehash
					sourcehash = md5sum(source)
					print '\t'+source+': '+sourcehash

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

				if sourcehash != targethash:
					print 'Aborting: Partial content binary differs.'
					return
				else:								# equal
					print '\tContinuing transfer ...'
#					partials = listdir(join(target, '*.partial-*'))
#					if len(partials) > 0:
#						concatenate_partial_files(source, target, Self, partials)
#					else:
#						calculate_missing_parts(source, target, Self)

			elif sourcesize < targetsize:	# bigger
				print 'Aborting: Target file is bigger.'
				return

