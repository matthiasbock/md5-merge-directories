#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import getopt
import sys
import os
import hashlib
import shutil

def largefileMD5( filename ):
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()

def merge(target_folder, source_folder, relative_folder="."):	# recurse
	global keep
	global overwrite

	print relative_folder+"/"

	for item in os.listdir( os.path.join(source_folder, relative_folder) ):				# für jede Datei/jedes Verzeichnis, das "rechts" existiert ...

		target = os.path.join(target_folder, relative_folder, item)
		source = os.path.join(source_folder, relative_folder, item)

		if os.path.isfile( source ):				#   ist es eine Datei:
			if os.path.exists( target ):
				target_filesize = os.path.getsize(target)
				source_filesize = os.path.getsize(source)
				if source_filesize != target_filesize:
					target_md5sum = "Size Mismatch"
					source_md5sum = "-"
				else:
					target_md5sum = largefileMD5( target )
					if target_filesize == 0:
						source_md5sum = "-"	# overwrite empty files left
					else:
						source_md5sum = largefileMD5( source )
			else:
				target_md5sum = "Not Found"
				source_md5sum = "-"

			if target_md5sum == source_md5sum:	# files are equal
				if not keep:
					os.remove( source )
				print ".",
			else:				# not equal
				print '\n'+item+' not equal:\t\t in "'+target_folder+'": '+target_md5sum+' , in "'+source_folder+'": '+source_md5sum
				if target_md5sum == "Not Found":
					move_to_filename = target	# simply move/copy to move_to_filename
				else:
					if overwrite:
						os.remove( target )
						move_to_filename = target
					else:
						if target_filesize == 0:
							os.remove( target )
							move_to_filename = target
						else:
							if source_md5sum == "":
								source_md5sum = largefileMD5( source )
							move_to_filename = target+"-"+source_md5sum
				if keep:
					try:
						shutil.copy( source, move_to_filename )
					except:
						print "FAILED: copy "+source+" "+move_to_filename
						sys.exit(1)
				else:
					try:
						shutil.move( source, move_to_filename )
					except:
						print "FAILED: move "+source+" "+move_to_filename
						sys.exit(1)

		elif os.path.isdir( source ):				# wenn es allerdings ein Verzeichnis ist
			if not os.path.exists( target ):	
				print "Creating Folder "+target
				try:
					os.mkdir( target )		# erzeuge es ggf. auch im Zielverzeichnis
				except:
					print "FAILED: creating folder "+target
					sys.exit(1)
			merge( target_folder, source_folder, relative_folder=relative_folder+"/"+item )
			if not keep:
				os.rmdir( source )
			print ""

if len(sys.argv) < 3:
	print "Usage: md5merge.py [--keep] [--overwrite] target_folder source_folder1 source_folder2 ..."
	sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "k:o", ["keep", "overwrite"])
global keep
global overwrite
keep = False
overwrite = False
for o, a in opts:
	if o in ("-k", "--keep"):
		keep = True
	elif o in ("-o", "--overwrite"):
		overwrite = True
	else:
		print 'Warning: Ignoring unrecognized argument "'+o+'".'

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

	if not keep:
		print 'Removing remaining empty directory "'+source_folder+'" ...'
		os.rmdir(source_folder)

