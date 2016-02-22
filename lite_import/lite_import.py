#! /usr/bin/env python

def lite_import(packagename):
	""" imports existing custom packages and modules in current namespace
	"""
	
	import importlib
	globals().update(importlib.import_module(packagename).__dict__)

