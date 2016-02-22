#!/usr/bin/env python

global config_names, config_dict

import collections

config_names = [
	'datafile', 
	'num_cases', 
	'num_topics', 
	'model_list', 
	'search_criteria_question', 
	'search_criteria_sniptext', 
	'search_criteria_longtext',
	'include_no_abstracts',
	'append_whole_abstracts', 
	'grouping_level', 
	'candidate_sentences', 
	'search_algo', 
	'search_results_tag',
	'run_dataprep', 
	'run_training', 
	'run_application', 
	'run_consolidation', 
	'run_analysis',
	'similarity_fname',
	'partition_data',
	'eval_test',
	'eval_train',
	'eval_all',
	'description',
	'extra_params'
]

config_dict = collections.dict()
config_dict['xp53'] = [
	['ClinicalInquiries.xml', -1, 500, ['tfidf'], True, False, False, False, False, 2, 3, 'singleproc_similarity_threshold', 'tm',  True, True, True, True, False, 'distance_cosine_similarity', True, True, False, False, 'tfidf',['auto',0,1e-5]]
]