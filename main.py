#! /usr/bin/env python

""" top-level summarisation pipeline
"""



def main():

	# import params
	from params import paths as paths
	
	from extract_input.partition_original_docs import partition_original_docs as partition_original_docs
	
	# prep data for DUC 
	partition_original_docs(paths.source_aquaint_original,3,paths.source_aquaint_docs,False)
	
	# prep data for TAC 
	# extract_input.partition_original_docs(paths.source_aquaint2_original,2,paths.source_aquaint2_docs,False)

	from extract_input.convert_topics_duc_to_tac import convert_topics_duc_to_tac as convert_topics_duc_to_tac
	convert_topics_duc_to_tac(paths.source_duc2007_topicxml_orig,paths.source_duc2007_topicxml,paths.source_aquaint_docs,paths.source_duc2007_docs)



if __name__ == '__main__':
	main()

