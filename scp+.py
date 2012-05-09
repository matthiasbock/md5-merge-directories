#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-


# Constants

from constants import *


# Console argument parsing

from sys import argv, exit
from fs import fname, exists

global behavior
app = fname(argv[0])
if app == 'smv':
	behavior = smv
	print '### Secure Move ###'
elif app == 'smerge':
	behavior = smerge
	print '### Secure Merge ###'
else:
	behavior = scp_plus
	print '### Secure Copy ###'

if len(argv) < 3:
	print 'Aborting: Not enough console arguments.'
	Usage()
	exit()

global sources, target
sources = []
for i in range(1, len(argv)-1):
	arg = argv[i].rstrip('/')
	if exists(arg):
		sources.append(arg)
	else:
		print 'Omitting source "'+arg+'": Not found.'
target = argv[len(argv)-1].rstrip('/')

print str(len(sources))+' sources: '+str(sources)
print 'target: '+target

if len(sources) < 1:
	print 'Aborting: No sources.'
	exit()


# Main

from main import transfer_to_target
for source in sources:
	transfer_to_target(source, target)

