#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-


# Constants

from constants import *


# Console argument parsing

from sys import argv, exit
from fs import fname, exists
import settings

app = fname(argv[0])
if app == 'smv':
	settings.behavior = smv
	print '### Secure Move ###'
elif app == 'smerge':
	settings.behavior = smerge
	print '### Secure Merge ###'
else:
	settings.behavior = scp_plus
	print '### Secure Copy ###'

if len(argv) < 3:
	print 'Aborting: Not enough console arguments.'
	Usage()
	exit()

for i in range(1, len(argv)-1):
	arg = argv[i].rstrip('/')
	if exists(arg):
		settings.sources.append(arg)
	else:
		print 'Omitting source "'+arg+'": Not found.'
settings.target = argv[len(argv)-1].rstrip('/')

print str(len(settings.sources))+' sources: '+str(settings.sources)
print 'target: '+settings.target

if len(settings.sources) < 1:
	print 'Aborting: No sources.'
	exit()


# Main

from main import transfer_to_target
for source in settings.sources:
	transfer_to_target(source, settings.target)

