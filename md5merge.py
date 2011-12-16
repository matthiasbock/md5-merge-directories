#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import getopt
import sys
import os
import hashlib
import shutil


# move or copy?
parameter_keep_source = "copy"

# overwrite mismatching or rename mismatching source file?
parameter_overwrite_mismatching = "overwrite"

# Usage
if len(sys.argv) < 3:
	print "Usage: md5merge.py [--"+parameter_keep_source+"] [--"+parameter_overwrite_mismatching+"] target_folder source_folder1 source_folder2 ..."
	sys.exit()

# make sure, all parameters are preceeding the folders
if sys.argv[len(sys.argv)-1][:2] == "--":
	print "Error: Parameters must preceed folders."
	sys.exit(1)

# parse parameters
opts, args = getopt.getopt(sys.argv[1:], "", [parameter_keep_source, parameter_overwrite_mismatching])
global keep_source
global overwrite_mismatching
global overwrite_empty_files
keep_source = False
overwrite_mismatching = False
overwrite_empty_files = True
for o, a in opts:
	if o == "--"+parameter_keep_source:
		keep_source = True
	elif o == "--"+parameter_overwrite_mismatching:
		overwrite_mismatching = True
	else:
		print 'Warning: Ignoring unrecognized parameter "'+o+'".'

#_____________________________________________________________________________
#		| not found	| file	| link	| dir	|
# exists	|
# islink	|
# isfile	|
# isdir		|

# main merge function
def merge(target_folder, source_folder, relative_folder="."):

	global keep_source
	global overwrite_mismatching
	global overwrite_empty_files

	print relative_folder+"/"

	def largefileMD5( filename ):
		md5 = hashlib.md5()
		with open(filename,'rb') as f: 
			for chunk in iter(lambda: f.read(8192), ''): 
				md5.update(chunk)
		return md5.hexdigest()

	for item in os.listdir( os.path.join(source_folder, relative_folder) ):		# for every file in source folder :

		target = os.path.join(target_folder, relative_folder, item)
		source = os.path.join(source_folder, relative_folder, item)

		if os.path.isdir( source ):						## source is a folder ?
			if not os.path.exists( target ):	
				print "Creating Folder "+target
				try:
					os.mkdir( target )
				except:
					print "Error: Failed creating folder "+target
					sys.exit(1)
			else:
				print ".",

			merge( target_folder, source_folder, relative_folder=relative_folder+"/"+item )	# recurse into folder
			if not keep_source:
				os.rmdir( source )

			print "" # newline

		elif not os.path.exists( target ):					## source is a file or a link,
											## but does the target even exist ?
			if keep_source:
				try:
					shutil.copy( source, target )
				except:
					print "Error: Failed to copy "+source+" to "+target
					sys.exit(1)
			else:
				try:
					shutil.move( source, target )
				except:
					print "Error: Failed to move "+source+" to "+target
					sys.exit(1)

		else:									# yes, it does!

			if os.path.islink( source ):						## source is symbolic link ?

				if os.path.islink( target ):					# target also a link?
					source_target = os.readlink( source )
					target_target = os.readlink( target )
					if source_target == target_target:			# links identical
						# links with identical targets
						print ".",
						if not keep_source:
							os.remove( source )
					else:							# mismatching links
						print "Mismatching symbolic links: "
						print "\t"+source+": "+source_target
						print "\t"+target+": "+target_target
						if not keep_source:
							shutil.move( source, target+".merged_mismatching_link" )
						else:
							shutil.copy( source, target+".merged_mismatching_link" )

				elif os.path.isfile( target ):					# no, target is not a link!
					print "Mismatch: Source is a link, target a regular file."
					print "Sorry, don't know how to handle that, exiting ..."
					sys.exit(1)

			elif os.path.isfile( source ):						## regular file ?

				if os.path.islink( target ):					# but target is a link?
					print "Mismatch: Source is a regular file, target a symbolic link."
					print "Sorry, don't know how to handle that, exiting ..."
					sys.exit(1)

				elif os.path.isfile( target ):					# no, target is a regular file!
					target_filesize = os.path.getsize(target)
					source_filesize = os.path.getsize(source)
					if source_filesize != target_filesize:			# filesize differs
						source_md5sum = "filesize differs"
						target_md5sum = "doesn't matter"

						if (target_filesize == 0) and overwrite_empty_files:	# but target is empty anyway
							source_md5sum = "does'nt matter"
							target_md5sum = "empty file (overwriting)"

					else:							# compare by MD5sum
						source_md5sum = largefileMD5( source )
						target_md5sum = largefileMD5( target )

				if target_md5sum == source_md5sum:	# files are equal
					if not keep_source:
						os.remove( source )
					print ".",
				else:					# files differ
					print '\n'+item+' not equal:\t\t '+target_md5sum+' in "'+target_folder+'" vs. '+source_md5sum+' in "'+source_folder+'"'

					if overwrite_mismatching or ((target_filesize == 0) and overwrite_empty_files):
						os.remove( target )
						move_to_filename = target
					else:
						if len(source_md5sum) != 32:	# some stupid comment instead of MD5sum
							source_md5sum = largefileMD5( source )
						move_to_filename = target+"."+source_md5sum

					if keep_source:
						try:
							shutil.copy( source, move_to_filename )
						except:
							print "Error: Failed to copy "+source+" to "+move_to_filename
							sys.exit(1)
					else:
						try:
							shutil.move( source, move_to_filename )
						except:
							print "Error: Failed to move "+source+" to "+move_to_filename
							sys.exit(1)


target_folder = args[0]
if not os.path.exists( target_folder ):
	print "Error: '"+target_folder+"' not found"
	sys.exit(1)
if not os.path.isdir( target_folder ):
	print "Error: '"+target_folder+"' is not a folder"
	sys.exit(1)

for source_folder in args[1:]:
	if not os.path.exists( source_folder ):
		print "Error: '"+source_folder+"' not found"
		break
	if not os.path.isdir( source_folder ):
		print "Error: '"+source_folder+"' is not a folder"
		break

	print 'Merging "'+source_folder+'" into "'+target_folder+'" ...'
	merge(target_folder, source_folder)

	if not keep_source:
		print 'Removing remaining empty directory "'+source_folder+'" ...'
		os.rmdir(source_folder)

