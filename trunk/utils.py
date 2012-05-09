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

def run(cmd):
	from subprocess import Popen, PIPE
	from shlex import split

	print cmd

	pipes = cmd.split('|')
	if len(pipes) == 1:
		return Popen(split(pipes[0]), stdout=PIPE).communicate()[0]
	else:
		p = [ Popen(split(pipes[0]), stdout=PIPE) ]
		for i in range(1, len(pipes)):
			p.append( Popen(split(pipes[i]), stdin=p[i-1].stdout, stdout=PIPE) )
		return p[len(p)-1].communicate()[0]

def ggT(a, b):
	if a < b:
		a, b = b, a
	while a % b != 0:
		a, b = b, a % b
	return b

