#! /usr/bin/env python

def rename_rouge_files(rouge_folder,token_order,prefix,suffix):
	""" renames one token of rouge files
	"""
	
	# manifesting files
	from utils.recurse_folder import recurse_folder as recurse_folder
	filelist = recurse_folder(rouge_folder,0)
	
	from os import rename
	for f in filelist:
		farray = f.split('/')
		fn = farray[len(farray)-1]
		fnarray = fn.split('.')
		fntoken = fnarray[token_order]
		fnarray[token_order] = prefix+fnarray[token_order]+suffix
		farray[len(farray)-1] = '.'.join(fnarray)
		newf = '/'.join(farray)
		print(newf)
		rename(f,newf)
		
		
