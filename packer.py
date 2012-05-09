#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from subprocess import Popen
from shlex import split

def bzip2(filename):
	Popen(split('bzip2 -z9v '+filename)).wait()
	return filename+'.bz'

