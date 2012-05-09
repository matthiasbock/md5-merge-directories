#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from fs import *
from os.path import join


def validate_transfer(source, target, Self):

	name = fname(source)

	if md5sum(source) == md5sum(targetfile):
		print 'transfer completed: '+name
		transfer_completed(source, target, Self)

	else:
		print 'transfer failed: '+name

