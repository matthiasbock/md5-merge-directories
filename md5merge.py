#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import sys, os, shutil
from helper import *

# Note: the --verbose options is currently ignored

def merge(target_folder, source_folder, relative_folder="."):

	print relative_folder+"/"

	global keep_source, overwrite_mismatching, verbose, overwrite_empty_files, favor_nonempty_target

	currentfolder = os.path.join(source_folder, relative_folder)

	for item in os.listdir( currentfolder ):					# for every file in source folder :

		target = os.path.join(target_folder, relative_folder, item)
		source = os.path.join(source_folder, relative_folder, item)

		if os.path.isdir( source ):						## source is a folder
			if os.path.exists( target ):					### target exists
				if os.path.isdir( target ):
					print ".",
				else:							# but is not a folder -> FATAL, exit
					print "Fatal: Unable to merge directory into file '"+target+"'"
					sys.exit(1)
			else:
				print "Creating missing folder "+target+" ... "
				os.mkdir( target )

			merge( target_folder, source_folder, relative_folder+"/"+item )	# recurse into subfolder
			if not keep_source:
				print 'Removing remaining empty directory "'+source+'" ...'
				os.rmdir( source )

			print "" # newline

		elif not os.path.exists( target ):					## source is a file or a link,
											## but target does not exist anyway
			if keep_source:
				shutil.copy( source, target )
			else:
				shutil.move( source, target )

		else:									# source is file or link, and target exists

			if os.path.islink( source ):						## source is a link

				if os.path.islink( target ):					### target is also a link
					source_target = os.readlink( source )			# get link targets
					target_target = os.readlink( target )
					if source_target == target_target:			# link targets identical => identical
						print ".",
						if not keep_source:
							os.remove( source )
					else:							# link target mismatch !
						print "Mismatching symbolic links: "
						print "\t"+source+": "+source_target
						print "\t"+target+": "+target_target
						if not keep_source:
							shutil.move( source, target+".merged_mismatching_link" )
						else:
							shutil.copy( source, target+".merged_mismatching_link" )

				elif os.path.isfile( target ):					### target is a regular file -> FATAL, exit
					print "FATAL: Unable to merge link and regular file '"+target+"'"
					sys.exit(1)

			elif os.path.isfile( source ):						## source is a regular file

				if os.path.islink( target ):					### target is a link -> FATAL, exit
					print "FATAL: Unable to merge regular file and link '"+target+"'"
					sys.exit(1)

				elif os.path.isfile( target ):					### target is a regular file

					target_filesize = os.path.getsize(target)
					source_filesize = os.path.getsize(source)

					if source_filesize != target_filesize:			# compare by filesize (to avoid cpu-intense hash calculation)
						source_hash = "<different filesize>"
						target_hash = "<not calculated>"

						if (target_filesize == 0) and overwrite_empty_files:	# target is an empty file
							source_hash = "<not empty>"
							target_hash = "<empty>"

						elif (source_filesize == 0) and favor_nonempty_target:	# source is an empty file
							source_hash = "<empty>"
							target_hash = "<not empty>"
							os.remove( source )

					else:							# equal filesize -> compare by MD5 hash
						source_hash = largefileMD5( source )
						target_hash = largefileMD5( target )

					if target_hash == source_hash:	# files seem to be binary equal
						if not keep_source:
							os.remove( source )	# remove source file
						print ".",
					else:					# files differ or hash was not calculated
						if (source_filesize == 0) and favor_nonempty_target:
							print '\nFavored non-empty target file. '+source+' removed.'
						else:
							print '\nMismatch: '+item+':\t\t '+target_hash+' in "'+target_folder+'" vs. '+source_hash+' in "'+source_folder+'"'

							move_to_filename = target

							if overwrite_mismatching or ((target_filesize == 0) and overwrite_empty_files):
								os.remove( target )
							else:
								if len(source_hash) != 32: # we really need a hash, not some stupid comment
									source_hash = largefileMD5( source )
								move_to_filename = target+"."+source_hash

							if keep_source:
								shutil.copy( source, move_to_filename )
							else:
								shutil.move( source, move_to_filename )


if __name__ == '__main__':

	parse_console_arguments("copy", "overwrite", "verbose")
	ensure_target_is_valid()
	print_settings()

	for source_folder in source_folders:
		if source_is_valid( source_folder ):
			print 'Merging "'+source_folder+'" into "'+target_folder+'" ...'

			merge(target_folder, source_folder)

			if not keep_source:
				print 'Removing remaining empty directory "'+source_folder+'" ...'
				os.rmdir(source_folder)

