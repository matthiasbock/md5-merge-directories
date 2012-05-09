#!/usr/bin/python2.6
# -*- coding: iso-8859-15 -*-

def format(size):
	suffices = ['PB', 'TB', 'GB', 'MB', 'KB', 'Byte']
	for i in range(len(suffices)):
		exponent = len(suffices)-1-i
		divisor = 1024**exponent
		if size >= divisor:
			size = size/divisor
			suffix = suffices[i]
			break
	return str(size)+' '+suffix

