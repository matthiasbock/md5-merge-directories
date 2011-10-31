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
	print relative_folder+"/"

	for item in os.listdir( dir2+"/"+relative_folder ):				# für jede Datei/jedes Verzeichnis, das "rechts" existiert ...

		left_item = dir1+"/"+relative_folder+"/"+item
		right_item = dir2+"/"+relative_folder+"/"+item

		if os.path.isfile( right_item ):				#   ist es eine Datei:
			if os.path.exists( left_item ):						# gibt es dieselbe Datei auch links?
				right_filesize = os.path.getsize(right_item)				# Dateigröße rechts
				left_filesize = os.path.getsize(left_item)				# Dateigröße links
				if right_filesize != left_filesize:					# wenn die Dateigrößen schon ungleich sind, kann ich mir die MD5-Summe sparen
					left_md5 = "Groessenunterschied!"
				else:
					left_md5 = largefileMD5( left_item )
				if left_filesize > 0:
					right_md5 = largefileMD5( right_item )				# Prüfsumme rechts, die brauche ich auf jeden Fall
				else:
					right_md5 = "leere Datei ersetzen"
			else:
				left_md5 = "nicht vorhanden"						# ansonsten mach einen Dummy, der immer "ungleich" triggert
				right_md5 = "nach links verschieben"
			if left_md5 == right_md5:							# wenn die Prüfsummen gleich sind
				os.remove( right_item )							# lösche die Datei rechts, belasse sie links
				print ".",
			else:										# wenn die Prüfsummen ungleich sind oder die Datei links nicht existiert
				print "\n"+item+"\t\t\""+dir1+"\":"+left_md5+" , \""+dir2+"\":"+right_md5
				if left_md5 == "nicht vorhanden":					# ... und benenne sie dabei um (um die linke nicht zu überschreiben)
					newname = left_item
				else:
					newname = left_item+"-"+right_md5
					if left_filesize == 0:						# wenn sie links leer ist, dann überschreibe sie einfach
						os.remove( left_item )
						newname = left_item
				shutil.move( right_item, newname )

		elif os.path.isdir( right_item ):				# wenn es allerdings ein Verzeichnis ist
			if not os.path.exists( left_item ):	
				print "-> creating folder "+left_item
				os.mkdir( left_item )						# erzeuge es ggf. auch links
			merge( dir1, dir2, relative_folder=relative_folder+"/"+item )		# und führe die beiden Verzeichnisse zusammen
			os.rmdir( right_item )							# nachdem das rechte danach leer sein sollte, können wir es löschen
			print ""

if len(sys.argv) < 3:
	print " Dieses Skript führt zwei Verzeichnisse zusammen, die den gleichartigen Inhalt möglicherweise in unterschiedlichen Fassungen enthalten."
	print " Alle Dateien werden anhand ihrer MD5-Prüfsummen verglichen."
	print " Dateien, die sich unterscheiden, werden umbenannt und in das erstere angegebene Verzeichnis verschoben."
	exit()

opts, args = getopt.getopt(sys.argv[1:], "c", ["copy"])
copy = False
for o, a in opts:
	if o in ("-c", "--copy"):
		copy = True
	else:
		print 'Warning: Ignoring unrecognized argument "'+o+'".'

dir1 = a[0]
if not os.path.exists( dir1 ):
	print "Error: '"+dir1+"' not found"
	sys.exit(1)
if not os.path.isdir( dir1 ):
	print "Error: '"+dir1+"' is not a folder"
	sys.exit(1)

for dir2 in a[1:]:
	if not os.path.exists( dir2 ):
		print "Error: '"+dir2+"' not found"
		break
	if not os.path.isdir( dir2 ):
		print "Error: '"+dir2+"' is not a folder"
		break

	print 'Merging "'+dir2+'" into "'+dir1+'" ..."
	merge(dir1, dir2)
	print 'Removing remaining empty directory "'+dir2+'" ...'
	os.rmdir(dir2)

