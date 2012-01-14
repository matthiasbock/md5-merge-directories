#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

import sys, os, hashlib, getopt

def parse_console_arguments(_keep_source='copy', _overwrite_mismatching='overwrite', _verbose='verbose'):

	global keep_source, overwrite_mismatching, verbose, overwrite_empty_files, favor_nonempty_target

	# console parameters
	keep_source = False				# move or copy ?
	overwrite_mismatching = False			# on hash mismatch: overwrite target or rename source ?
	verbose = False					# print a verbose line for every file, or just print dots on match ?

	# hardcoded parameters
	overwrite_empty_files = True			# overwrite empty target files ?
	favor_nonempty_target = True			# remove empty source files, if the target is not empty ?

	# Usage
	if len(sys.argv) < 3:
		print "Usage: md5merge.py [--"+_keep_source+"] [--"+_overwrite_mismatching+"] [--"+_verbose+"] <target> <source 1> <source 2> ..."
		sys.exit()

	# make sure, all parameters are preceeding the folders
	if sys.argv[len(sys.argv)-1][:2] == "--":	# last argument is not a parameter
		print "Error: Parameters must preceed folders"
		sys.exit(1)

	# parse parameters
	opts, args = getopt.getopt(sys.argv[1:], "", [_keep_source, _overwrite_mismatching, _verbose])

	for o, a in opts:
		if o == "--"+_keep_source:
			keep_source = True
		elif o == "--"+_overwrite_mismatching:
			overwrite_mismatching = True
		elif o == "--"+_verbose:
			verbose = True
		else:
			print 'Warning: Ignoring unrecognized parameter "'+o+'".'

	global target_folder, source_folders

	target_folder = args[0]
	source_folders = args[1:]


def ensure_target_is_valid():

	global target_folder

	if not os.path.exists( target_folder ):
		print "Error: '"+target_folder+"' not found"
		sys.exit(1)
	if not os.path.isdir( target_folder ):
		print "Error: '"+target_folder+"' is not a folder"
		sys.exit(1)


def print_settings():
	global ...

	print ...
	print "You can always interrupt using Ctrl+C"
	print ""

	wait = 3
	print "Starting in ..."
	for i in range(wait):
		print 
		sleep(1)


def source_is_valid( source ):
	if not os.path.exists( source ):
		print "Error: Source '"+source+"' not found. Skipping."
		return False
	if not os.path.isdir( source ):
		print "Error: Source '"+source+"' is not a folder. Skipping."
		return False
	if source_is_a_subfolder_of_target( source ):
		print "Error: Source must not be a subfolder of target: '"+source+"'. Skipping."
		return False
	return True


def largefileMD5( filename ):
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()


def source_is_a_subfolder_of_target( source ):
	global target_folder

	return (target_folder.find(source) > -1)

