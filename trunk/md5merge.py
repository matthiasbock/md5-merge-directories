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

def merge(dir1, dir2, relative_folder="."):	# recurse
	global keep
	global overwrite

	print relative_folder+"/"

	for item in os.listdir( dir2+"/"+relative_folder ):				# für jede Datei/jedes Verzeichnis, das "rechts" existiert ...

		left_file = dir1+"/"+relative_folder+"/"+item
		right_file = dir2+"/"+relative_folder+"/"+item

		if os.path.isfile( right_file ):				#   ist es eine Datei:
			if os.path.exists( left_file ):
				left_filesize = os.path.getsize(left_file)
				right_filesize = os.path.getsize(right_file)
				if right_filesize != left_filesize:
					left_md5 = "Size Mismatch"
					right_md5 = "-"
				else:
					left_md5 = largefileMD5( left_file )
					if left_filesize == 0:
						right_md5 = "-"	# overwrite empty files left
					else:
						right_md5 = largefileMD5( right_file )
			else:
				left_md5 = "Not Found"
				right_md5 = "-"

			if left_md5 == right_md5:	# files are equal
				if not keep:
					os.remove( right_file )
				print ".",
			else:				# not equal
				print '\n'+item+'\t\t in "'+dir1+'": '+left_md5+' , in "'+dir2+'": '+right_md5
				if left_md5 == "Not Found":
					newname = left_file
				else:
					if overwrite:
						os.remove( left_file )
						newname = left_file
					else:
						if left_filesize == 0:
							os.remove( left_file )
							newname = left_file
						else:
							if right_md5 == "":
								right_md5 = largefileMD5( right_file )
							newname = left_file+"-"+right_md5
				if keep:
					shutil.copy( right_file, newname )
				else:
					shutil.move( right_file, newname )

		elif os.path.isdir( right_file ):				# wenn es allerdings ein Verzeichnis ist
			if not os.path.exists( left_file ):	
				print "Creating Folder "+left_file
				os.mkdir( left_file )						# erzeuge es ggf. auch links
			merge( dir1, dir2, relative_folder=relative_folder+"/"+item )
			if not keep:
				os.rmdir( right_file )
			print ""

if len(sys.argv) < 3:
	print "Usage: md5merge.py [--keep] [--overwrite] dir1 dir2 dir3 ..."
	exit()

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

dir1 = args[0]
if not os.path.exists( dir1 ):
	print "Error: '"+dir1+"' not found"
	sys.exit(1)
if not os.path.isdir( dir1 ):
	print "Error: '"+dir1+"' is not a folder"
	sys.exit(1)

for dir2 in args[1:]:
	if not os.path.exists( dir2 ):
		print "Error: '"+dir2+"' not found"
		break
	if not os.path.isdir( dir2 ):
		print "Error: '"+dir2+"' is not a folder"
		break

	print 'Merging "'+dir2+'" into "'+dir1+'" ...'
	merge(dir1, dir2)

	if not keep:
		print 'Removing remaining empty directory "'+dir2+'" ...'
		os.rmdir(dir2)

