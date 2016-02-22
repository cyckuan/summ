#! /usr/bin/env python

def timestamp():
	""" gets timestamp
	"""
	
	import datetime, time
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')