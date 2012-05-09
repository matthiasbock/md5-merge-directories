#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from fs import *
from os.path import join
from utils import format

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

			sourcesize = fsize(source)
			print '\t'+source+': '+format(sourcesize)
			targetsize = fsize(corresponding_target)
			print '\t'+corresponding_target+': '+format(targetsize)

			if sourcesize == targetsize:
				if md5sum(source) == md5sum(targetfile):
					print 'equal hashes'
				else:
					print 'hashes differ'

			elif sourcesize > targetsize:	# smaller
				if md5sum(source) != md5sum(targetfile)#, end=getsize(source)):	# different
					print 'Aborting: Partial files binary differ.'
					return
				else:								# equal
					print '\tTarget is source file''s partial. Continuing transfer ...'
#					partials = listdir(join(target, '*.partial-*'))
#					if len(partials) > 0:
#						concatenate_partial_files(source, target, Self, partials)
#					else:
#						calculate_missing_parts(source, target, Self)

			elif sourcesize < targetsize:	# bigger
				print 'Aborting: Target file is bigger.'
				return

