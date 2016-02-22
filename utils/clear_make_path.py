#! /usr/bin/env python

def clear_make_path(pathname,clear=True):
	""" clears and prepares directory 
	"""
	
	import os
	if clear:
		os.system('rm -rf ' + pathname)
	if not os.path.exists(pathname):
		os.makedirs(pathname)