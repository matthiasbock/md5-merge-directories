#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from fs import *
from os.path import join
from recurse import recurse

def calculate_missing_parts(source, target, Self):
	...


def concatenate_partial_files(source, target, Self, partials):
	targetfile = join(target, fname(source))

	for partial in partials:
		dd if=partial of=targetfile seek=position
		delete(partial)


def compare_filesizes(source, target, Self):

	targetfile = join(target, fname(source))

	sourcesize = fsize(source)
	targetsize = fsize(targetfile)

	if sourcesize == targetsize:	# equal
		if md5sum(source) == md5sum(targetfile):
			print 'transfer completed: '+name
			transfer_completed(source, target, Self)
		else:
			different_target(source, target, Self)

	elif sourcesize > targetsize:	# smaller
		# compare partial content
		if md5sum(source) != md5sum(targetfile, end=getsize(source)):	# different
			different_target(source, target, Self)
		else:								# equal
			partials = listdir(join(target, '*.partial-*'))
			if len(partials) > 0:
				concatenate_partial_files(source, target, Self, partials)
			else:
				calculate_missing_parts(source, target, Self)

	elif sourcesize < targetsize:	# bigger
		different_target(source, target, Self)
		

def check_target(source, target, Self):
	from transfer import scp

	targetfile = join(target, fname(source))

	if not exists(targetfile)
		mkdir(target)
		scp(source, target)
		validate_transfer(source, target, Self)

	elif isdir(targetfile):
		print 'abort: unmergeable: file and folder '+fname(source)
		return

	elif isfile(targetfile):
		compare_filesizes(source, target, Self)


def transfer_to_target(source, target, Self):

	if not exists(source):
		print 'abort: file not found: '+source
		return

	elif isdir(source):
		corresponding_target_folder = join(target, fname(source))
		recurse(source, corresponding_target_folder, Self)

	elif isfile(source):
		check_target(source, target, Self)

