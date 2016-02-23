#! /usr/bin/env python

def recurse_folder(startdir,targetlevel,currentlevel=0):
	""" recursively traverses the directory tree from starting path and level of 0 until the target level is reached
	"""

	result = []
	import os
	for f in os.listdir(startdir):
		d = os.path.join(startdir,f)
		if currentlevel == targetlevel:
			if os.path.isfile(d):
				print(str(currentlevel) + ' - ' + d)
				result.append(d)
		else:
			if os.path.isdir(d):
				print(str(currentlevel) + ' : ' + d)
				result = result + recurse_folder(d,targetlevel,currentlevel+1)

	return result