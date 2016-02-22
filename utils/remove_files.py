#! /usr/bin/env python

def remove_files(hitlist):
	""" deletes files in the hit list
	"""
	
	import os
	for f in hitlist:
		if os.path.exists(f):
			os.remove(f)
			print('removed : ',f)
			