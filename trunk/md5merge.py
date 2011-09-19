#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Programm Parameter

import sys

try:
	dir1 = sys.argv[1].rstrip("/")
	dir2 = sys.argv[2].rstrip("/")
except:
	print " Dieses Skript führt zwei Verzeichnisse zusammen, die nominal das Gleiche enthalten sollen."
	print " Dabei wird die Equivalenz von Dateien mit demselben Pfad anhand der MD5-Prüfsummen validiert."
	print " Dateien, die sich unterscheiden, werden umbenannt und in das erstere angegebene Verzeichnis verschoben."
	sys.exit(1)

# gibt es die übergebenen Pfade wirklich ?

import os

if (not os.path.exists( dir1 )) or (not os.path.isdir( dir1 )):
	print dir1+" does not exist / is not a folder"
	sys.exit(1)

if (not os.path.exists( dir2 )) or (not os.path.isdir( dir2 )):
	print dir2+" does not exist / is not a folder"
	sys.exit(1)

# compare directory by directory

import hashlib
import shutil

def largefileMD5( filename ):
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(8192), ''): 
			md5.update(chunk)
	return md5.hexdigest()

def compare( relative_folder ): 							# rekursive Funktion
	print relative_folder+"/"
	for item in os.listdir( dir2+"/"+relative_folder ):				# für jede Datei/jedes Verzeichnis, das "rechts" existiert ...
		left_item = dir1+"/"+relative_folder+"/"+item
		right_item = dir2+"/"+relative_folder+"/"+item
		if os.path.isfile( right_item ):			#   ist es eine Datei:
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
					right_md5 = "ueberschreibe die leere Datei"
			else:
				left_md5 = "nicht vorhanden"						# ansonsten mach einen Dummy, der immer "ungleich" triggert
				right_md5 = "verschiebe sowieso"
			if left_md5 == right_md5:					# wenn die Prüfsummen gleich sind
				os.remove( right_item )					# lösche die Datei rechts, belasse sie links
				print ".",
			else:								# wenn die Prüfsummen ungleich sind oder die Datei links nicht existiert
				print "\n"+item+"\t\t\""+dir1+"\":"+left_md5+" , \""+dir2+"\":"+right_md5	# bewege die rechte Datei in das linke Verzeichnis
				if left_md5 != "nicht vorhanden":			# ... und benenne sie dabei um (um die linke nicht zu überschreiben)
					newname = left_item+"-"+right_md5
					if left_filesize == 0:	# wenn sie links leer ist, dann überschreibe sie einfach
						os.remove( left_item )
						newname = left_item
					shutil.move( right_item, newname )
				else:							# ... bzw. wenn sie links nicht existiert, dann benenne dabei nichts um
					shutil.move( right_item, left_item )
		elif os.path.isdir( right_item ):		# wenn es allerdings ein Verzeichnis ist
			if not os.path.exists( left_item ):	
				print "-> creating folder "+left_item
				os.mkdir( left_item )		# erzeuge es ggf. auch links
			if not os.path.islink( right_item ):
				compare( relative_folder+"/"+item )	# und vergleiche (rekursiv) die beiden Verzeichnisse
			try:
				os.rmdir( right_item )		# nachdem das rechte danach leer sein sollte, können wir es löschen
			except:
				pass
			print ""

compare( "." )
os.rmdir( dir2 )

