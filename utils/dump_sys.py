#! /usr/bin/env python

def dump_sys():
	""" dump system variables
	"""
	
	import sys, setuptools, pkg_resources
	print(sys.path)
	print(pkg_resources.__file__)
	print(setuptools.__file__)
	# dict(locals().items()+globals().items())