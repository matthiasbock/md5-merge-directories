#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

from fs import *
from os.path import join
from main import transfer_to_target


def recurse(source, target, Self):
	for item in listdir(source):
		transfer_to_target(join(source, item), join(target, item), Self)

