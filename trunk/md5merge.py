#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import sys, os

from helper import *
from filesystem import *
from md5 import *

# Note: the --verbose options is currently ignored


def merge(target_folder, source_folder, relative_folder="."):

	print relative_folder+"/"

	global keep_source, overwrite_mismatching, verbose, overwrite_empty_files, favor_nonempty_target

	currentfolder = os.path.join(source_folder, relative_folder)

	for item in listdir( currentfolder ):					# for every file in source folder :

		if item == '':
			print 'Error: Empty item. Programming error? Please report this incident.'
			sys.exit(1)

		target = os.path.join(target_folder, relative_folder, item)
		source = os.path.join(source_folder, relative_folder, item)

		if isdir( source ):							## source is a folder
			if exists( target ):						### target exists
				if isdir( target ):
					print ".",
				else:							# target is not a folder -> FATAL, exit
					print "Fatal: Unable to merge directory into file '"+target+"'"
					sys.exit(1)
			else:
				if islink( target ):					 # target is a broken link -> FATAL, exit
					print "Fatal: Unable to merge directory into broken link '"+target+"'"
					sys.exit(1)

				print "Creating missing folder "+target+" ... "
				mkdir( target )

			merge( target_folder, source_folder, relative_folder+"/"+item )	# recurse into subfolder
			if not keep_source:
				print 'Removing remaining empty directory "'+source+'" ...'
				rmdir( source )

			print "" # newline

		elif not (exists( target ) or islink( target )):			## source is a file or a link, but target does not exist anyway
											## second statement exludes broken links, that are handled below
			if keep_source:
				copy( source, target )
			else:
				move( source, target )
		else:									# source is file or link, and target exists

			if islink( source ):							## source is a link

				if islink( target ):						### target is also a link
					source_target = readlink( source )			# get link targets
					target_target = readlink( target )
					if source_target == target_target:			# link targets identical => identical
						print ".",
						if not keep_source:
							remove( source )
					else:							# link target mismatch !
						print "Mismatching symbolic links: "
						print "\t"+source+": "+source_target
						print "\t"+target+": "+target_target
						if not keep_source:
							move( source, target+".merged_mismatching_link" )
						else:
							copy( source, target+".merged_mismatching_link" )

				elif isfile( target ):						### target is a regular file -> FATAL, exit
					print "FATAL: Unable to merge link and regular file '"+target+"'"
					sys.exit(1)

			elif isfile( source ):							## source is a regular file

				if islink( target ):						### target is a link -> FATAL, exit
					print "FATAL: Unable to merge regular file and link '"+target+"'"
					sys.exit(1)

				elif isfile( target ):						### target is a regular file

					target_filesize = getsize(target)
					source_filesize = getsize(source)

					if source_filesize != target_filesize:			# compare by filesize (to avoid cpu-intense hash calculation)
						source_hash = str(source_filesize)+' bytes'
						target_hash = str(target_filesize)+' bytes'

						if (target_filesize == 0) and overwrite_empty_files:	# target is an empty file
							target_hash = "<empty->overwrite>"

						elif (source_filesize == 0) and favor_nonempty_target:	# source is an empty file
							source_hash = "<empty->favor non-empty>"
							remove( source )

					else:							# equal filesize -> compare by MD5 hash
						source_hash = md5sum( source )
						target_hash = md5sum( target )

					if target_hash == source_hash:	# files seem to be binary equal
						if not keep_source:
							remove( source )	# remove source file
						print ".",
					else:					# files differ or hash was not calculated
						if (source_filesize == 0) and favor_nonempty_target:
							print '\nFavored non-empty target file. '+source+' removed.'
						else:
							print '\nMismatch: '+item+':\t'+target_hash+' in "'+target_folder+'" vs. '+source_hash+' in "'+source_folder+'"'

							move_to_filename = target
							do_transfer = True

							if overwrite_mismatching or ((target_filesize == 0) and overwrite_empty_files):
								remove( target )
							else:
								if len(source_hash) != 32: # we really need a hash, not some stupid comment
									source_hash = md5sum( source )
								move_to_filename = target+"."+source_hash

								# if a target.source_hash exists, we must assume, the transfer has already taken place, but was interrupted
								# so, if the md5 hash if target.source_hash == source_hash, we may safely remove the source and skip transfering it
			
								if exists(move_to_filename) and md5sum(move_to_filename) == source_hash:
									print "Target "+move_to_filename+" already exists and is binary equal to the source. Transfer skipped."
									do_transfer = False
									if not keep_source:
										remove(source)
										print "Source removed: "+source

							if do_transfer:
								if keep_source:
									copy( source, move_to_filename )
								else:
									move( source, move_to_filename )


if __name__ == '__main__':

	target_folder, source_folders, keep_source, overwrite_mismatching, verbose, overwrite_empty_files, favor_nonempty_target = parse_console_arguments("copy", "overwrite", "verbose")

	ensure_target_is_valid()
	print_settings()

	for source_folder in source_folders:
		if source_is_valid( source_folder ):
			print 'Merging "'+source_folder+'" into "'+target_folder+'" ...'

			merge(target_folder, source_folder)

			if not keep_source:
				print 'Removing remaining empty directory "'+source_folder+'" ...'
				rmdir(source_folder)

