#! /usr/bin/env python

def scriptname(file=__file__):
	""" returns name of script without .py
	"""
	
	import os
	scriptname = os.path.basename(file)
	if scriptname[-3:] == '.py':
		scriptname = scriptname[:-3]
	return scriptname