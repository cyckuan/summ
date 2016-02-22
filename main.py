#! /usr/bin/env python

""" top-level summarisation pipeline
"""

def main():

	# import params
	from params import paths as paths
	
	# from extract_input.read_original_data import read_original_data as read_original_data
	
	import extract_input
	
	# prep data for DUC 
	# extract_input.partition_original_docs(paths.source_aquaint_original,3,paths.source_aquaint_docs,False)
	
	# prep data for TAC 
	# extract_input.partition_original_docs(paths.source_aquaint2_original,2,paths.source_aquaint2_docs,False)

	extract_input.convert_topics_duc_to_tac()


if __name__ == '__main__':
	main()

