#!/usr/bin/env python

def codegen():
	""" returns last folder as the generation name for iterative development
	"""
	import os
	return os.path.dirname(__file__).split('/')[-1]