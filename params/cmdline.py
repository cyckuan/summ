#!/usr/bin/env python

def cmdline_params():
	import optparse
	parser = optparse.OptionParser()
	# parser.add_option("-f", dest="filename", help="corpus filename")
	(options, args) = parser.parse_args()
	
	""" needs some work