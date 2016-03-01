import os

import pickle
import collections

import re
import string

import nltk
import gensim

import config
import paths

regex_punct = re.compile('[%s]' % re.escape(string.punctuation))


def get_globals():
	return globals()


def train_punkt_sent_tokenizer(train_ref,train_pickle):
	""" train punkt sentence tokenizer
	"""
	import nltk.tokenize.punkt
	tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
	
	# read training corpus
	import codecs
	text = codecs.open(train_ref).read()
	tokenizer.train(text)

	# dump pickled tokenizer
	import pickle
	out = open(train_pickle,"wb")
	pickle.dump(tokenizer, out)
	out.close()


def replace_punctuation(raw):
	""" removes punctuation from a given string
	"""
	punct = set(string.punctuation)
	
	return ''.join([r for r in raw if r not in punct])


def preprocess_sentence(raw):
	""" preprocessing of sentences incl
		word tokenization, strip, lower, punctuation removal
	"""
	
	# raw = re.sub(r"[\x80-\xff]"," ",raw)
	
	raw = regex_punct.sub(' ',raw)
	raw = raw.strip()
	raw = raw.lower()
	
	words = nltk.word_tokenize(raw)
	words = [replace_punctuation(w) for w in words if not w in stopwords and len(w) > 1]
	
	return(' '.join(words))


def preprocess_document(raw,sentence_level):
	""" preprocessing of document incl
		sentence tokenization
	"""

	# raw = raw.decode("utf-8")
	# raw = raw.encode("ascii","ignore")
	
	from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
	param = PunktParameters()
	tokenizer = PunktSentenceTokenizer(param)
	if sentence_level:
		sentences = tokenizer.tokenize(raw)
		sentences_words = list()
		for s in sentences:
			sentences_words.append((s.strip(),preprocess_sentence(s)))
		return sentences_words
	else:
		return [(raw.strip(),preprocess_sentence(raw))]


def load_partitions():
	global partition_test

	partitions = []

	for p in [paths.path_data_train_ids_txt,paths.path_data_test_ids_txt]:
		with open(p,'r') as partf:
			data = partf.read().split('\n')
			partitions.append(data)
	
	partition_test = partitions[1]


def load_corpus_questions():
	""" loads ClinicalInquiries.xml data into search criteria, solution and linked abstracts
	"""
	global search_criteria_dict, solution_dict, linked_abstracts_dict
	if os.path.exists(paths.path_data_questions_pickle):
		print('\nloading questions and answers')
		search_criteria_dict = pickle.load(open(paths.path_data_questions_pickle,"rb"))
		solution_dict = pickle.load(open(paths.path_data_answers_pickle,"rb"))
		linked_abstracts_dict = pickle.load(open(paths.path_data_linkedabstracts_pickle,"rb"))
		
		print(len(search_criteria_dict))
		print(len(solution_dict))
		print(len(linked_abstracts_dict))
		
		return True
	else:
		return False


def build_corpus_questions(criteria_incl_question=True, criteria_incl_snip=False, criteria_incl_long=False, level=0):
	""" reads ClinicalInquiries.xml data and extracts search criteria, solutions and search spaces (linked abstracts)
	"""

	print('\nbuilding questions and answers')

	if load_corpus_questions():
		return

	import xml.etree.ElementTree as ET

	question_count = 0
	no_abstract_tag = 0
	no_abstract_file = 0
	long_count = 0
	
	global search_criteria_dict, solution_dict, linked_abstracts_dict
	
	search_criteria_dict = collections.defaultdict(list)
	solution_dict = collections.defaultdict(list)
	linked_abstracts_dict = collections.defaultdict(list)
	common_map_dict = collections.defaultdict(list)
	
	tree = ET.parse(paths.path_data_questions)
	root = tree.getroot()
	for record in root.findall('record'):
		record_id = record.get('id')
		question_text = preprocess_document(record.find('question').text,True)

		if level == 0:
			key = record_id # key
		
		answer = record.find('answer')
		if answer is not None:
			for s in answer.findall('snip'):
				if s is not None:
					snip_id = s.get('id')
					snip_text = preprocess_document(s.find('sniptext').text,True)
					
					if level == 1:
						key = record_id + '_' + snip_id # key
					
					for i,l in enumerate(s.findall('long')):
						if l is not None:
							long_id = l.get('id')
							
							if level == 2:
								key = record_id + '_' + snip_id + '_' + long_id # key
								
							if criteria_incl_question:
								for x in question_text:
									search_criteria_dict[key].append(x) # question
							if criteria_incl_snip:
								for x in snip_text:
									search_criteria_dict[key].append(x) # snip
							
							long_text = l.find('longtext')
							if long_text is not None:
								long_text = preprocess_document(long_text.text,True)
								for x in long_text:
									solution_dict[key].append(x) # long - answer
								if criteria_incl_long:
									for x in long_text:
										search_criteria_dict[key].append(x) # long - search

							if key not in search_criteria_dict.keys():
								search_criteria_dict[key].append('')

							long_refs = l.findall('ref')
							for long_ref in long_refs:
								abstract =  long_ref.get('abstract')[10:]
								abstract_path = paths.path_data_abstracts + '/' + abstract
								abstract_sentences = abstracts_dict[abstract]
								linked_abstracts_dict[key].append(abstract) # linked abstracts
								
								long_count += 1
								
		question_count += 1
		# print(str(question_count) + ' : ' + str(question_text) + ' : ' + str(no_abstract_file) + ' : ' + str(no_abstract_tag) + ' : ' + str(long_count))

	pickle.dump(search_criteria_dict,open(paths.path_data_questions_pickle,"wb"))
	pickle.dump(solution_dict,open(paths.path_data_answers_pickle,"wb"))
	pickle.dump(linked_abstracts_dict,open(paths.path_data_linkedabstracts_pickle,"wb"))
	
	print(len(search_criteria_dict))
	print(len(solution_dict))
	print(len(linked_abstracts_dict))
	
	print('\ncorpus build complete')


def load_corpus_abstracts():
	""" loads abstract data into search space from file
	"""
	
	global abstracts_dict
	if os.path.exists(paths.path_data_abstracts_pickle):
		print('\nloading abstracts')
		abstracts_dict = pickle.load(open(paths.path_data_abstracts_pickle,"rb"))
		return True
	else:
		return False


def build_corpus_abstracts(sentence_level):
	""" reads abstracts and saves search space data to file
	"""

	print('\nbuilding abstracts')
	
	if load_corpus_abstracts():
		return
	
	import xml.etree.ElementTree as ET

	abstract_count = 0
	
	global abstracts_dict
	abstracts_dict = collections.defaultdict(list)
	
	with open(paths.path_data_logfile,'a') as logf:
		for filename in os.listdir(paths.path_data_abstracts):
			path_abstract_in = paths.path_data_abstracts + '/' + filename
			
			failed = True
			
			tree = ET.parse(path_abstract_in)
			root = tree.getroot()
			pubmed = root.find('pubmedarticle')
			if pubmed is not None:
				medline = pubmed.find('medlinecitation')
				if medline is not None:
					article = medline.find('article')
					if article is not None:
						abstract = article.find('abstract')
						if abstract is not None:
							failed = False
							abstracttexts = abstract.findall('abstracttext')
							for abstracttext in abstracttexts:
								text_subset = preprocess_document(abstracttext.text,sentence_level)
								for s in text_subset:
									if len(s[1]) > 0:
										abstracts_dict[filename].append(s)
								
								abstract_count += 1
								# print(str(abstract_count) + ' : ' + filename)
			
			if failed:
				logf.write(filename+'\n')
	
	pickle.dump(abstracts_dict,open(paths.path_data_abstracts_pickle,"wb"))


def load_stopwords():
	""" loads extended stopwords from file
	"""
	global stopwords
	if os.path.exists(paths.path_data_stopwords_txt):
		print('\nloading stopwords')
		with open(paths.path_data_stopwords_txt,'r') as inf:
			stopwords = inf.read().split('\n')
		return True
	else:
		return False


def build_stopwords():
	""" extends nltk stopwords and saves to file
	"""
	print('\nbuilding stopwords')
	
	if load_stopwords():
		return

	global stopwords
	stopwords = nltk.corpus.stopwords.words('english')
	for f in os.listdir(paths.path_data_stopwords):
		path_stopwords = paths.path_data_stopwords  + '/' + f
		with open(path_stopwords,'r') as f:
			for l in f:
				w = l.strip()
				w = re.sub(r"[\x80-\xff]"," ",w)
				if (w not in stopwords):
					stopwords.append(w)
	
	# wip improve with POS and remove numbers
	with open(paths.path_data_stopwords_txt,'w') as outf:
		outf.write('\n'.join(stopwords))
	
	print('\nstopword count : ' + str(len(stopwords)))


def combine_corpus(include_whole_abstracts=False):
	""" build common corpus consisting of questions and abstracts and saves to file
	"""
	if load_combined_corpus_maps():
		return
	
	global gensim_dictionary
	global search_criteria_dict, solution_dict, linked_abstracts_dict, abstracts_dict
	global common_corpus_list, question_map, abstract_map, abstract_whole_map
	global corpus_layout
	
	print('\nbuilding common corpus')
	
	common_corpus_list = list()
	question_map = dict()
	abstract_map = dict()
	abstract_whole_map = dict()
	
	sentence_count = 0
	
	corpus_layout = []
	
	for qi,qv in search_criteria_dict.items():
		questions = qv
		
		sentence_incr = len(questions)
		question_map[qi] = (sentence_count,sentence_count + sentence_incr)
		sentence_count += sentence_incr
		
		for st in questions:
			common_corpus_list.append(st)
	
	corpus_layout.append(('Q',sentence_count))
	
	for ai,av in abstracts_dict.items():
		abstract = av
		
		sentence_incr = len(abstract)
		abstract_map[ai] = (sentence_count,sentence_count + sentence_incr)
		sentence_count += sentence_incr

		for st in abstract:
			common_corpus_list.append(st)
	
	corpus_layout.append(('A',sentence_count))

	if include_whole_abstracts:
		for ai,av in abstracts_dict.items():
			abstract = av
			
			abstract_whole_map[ai] = (sentence_count,sentence_count + 1)
			sentence_count += 1

			st = tuple('\n'.join(s) for s in zip(*abstract))
			if len(st) < 2:
				st = ('','')

			common_corpus_list.append(st)
		
		corpus_layout.append(('W',sentence_count))
	
	pickle.dump(question_map,open(paths.path_data_map_questions_pickle,"wb"))
	pickle.dump(abstract_map,open(paths.path_data_map_abstracts_pickle,"wb"))
	pickle.dump(abstract_whole_map,open(paths.path_data_map_abstracts_whole_pickle,"wb"))	
	pickle.dump(common_corpus_list,open(paths.path_data_corpus_pickle,"wb"))
	pickle.dump(corpus_layout,open(paths.path_data_corpus_layout_pickle,"wb"))


def load_combined_corpus_maps():
	""" loads common corpus from file
	"""
	global common_corpus_list, question_map, abstract_map, abstract_whole_map, corpus_layout

	if os.path.exists(paths.path_data_corpus_pickle):
		print('\nloading corpus')
		common_corpus_list = pickle.load(open(paths.path_data_corpus_pickle,"rb"))
		question_map = pickle.load(open(paths.path_data_map_questions_pickle,"rb"))
		abstract_map = pickle.load(open(paths.path_data_map_abstracts_pickle,"rb"))
		abstract_whole_map = pickle.load(open(paths.path_data_map_abstracts_whole_pickle,"rb"))
		corpus_layout = pickle.load(open(paths.path_data_corpus_layout_pickle,"rb"))
		return True
	else:
		return False


def map_question_linked_abstracts(include_no_abstracts):
	""" maps question (search criteria) and linked abstracts (search space) according to common corpus indices
	"""
	if load_common_map():
		return
		
	global question_map, abstract_map, common_map
	global search_criteria_dict, solution_dict, linked_abstracts_dict

	print('\nmapping question to answers')
	
	common_map = collections.defaultdict(list)
	
	no_abstract_count = 0
		
	for i,v in question_map.items():
		print(i)
		abstracts = linked_abstracts_dict[i]
		for a in abstracts:
			if (a != 'NO_ABSTRACT') and (a in abstract_map.keys()):
				common_map[i].append([v,abstract_map[a]])
			else:
				if include_no_abstracts:
					common_map[i].append([v,()])
				no_abstract_count += 1
	
	print('\nabstractless : ' + str(no_abstract_count))
	
	print(len(question_map))
	print(len(abstract_map))
	print(len(common_map))
	
	pickle.dump(common_map,open(paths.path_data_map_common_pickle,"wb"))


def load_common_map():
	""" load map of questions (search criteria) and linked abstracts (search space) from file
	"""
	global common_map
	if os.path.exists(paths.path_data_map_common_pickle):
		print('\nloading map')
		common_map = pickle.load(open(paths.path_data_map_common_pickle,"rb"))
		return True
	else:
		return False


def load_oracle_sentences():
	global oracle_sentences
	
	if os.path.exists(paths.path_data_oraclesentences_pickle):
		print('\nloading oracle sentences')
		oracle_sentences = pickle.load(open(paths.path_data_oraclesentences_pickle, 'rb'))
		print(len(oracle_sentences))
		return True
	else:
		return False

def load_dictionary_gensim():
	""" load common dictionary
	"""
	global gensim_dictionary
	
	if os.path.exists(paths.path_data_dictionary_dict):
		print('\nloading dictionary')
		gensim_dictionary = gensim.corpora.Dictionary().load(paths.path_data_dictionary_dict)
		# print(gensim_dictionary.token2id)
		print(gensim_dictionary)
		return True
	else:
		return False


def build_dictionary_gensim():
	""" build common dictionary consisting of words from question and abstracts
	"""
	# if load_dictionary_gensim():
	#	return
	
	global gensim_dictionary, common_corpus_list
	
	print('\nbuilding dictionary')
	gensim_dictionary = gensim.corpora.Dictionary()
	
	for v in common_corpus_list:
		gensim_dictionary.add_documents([v[1].lower().split()])
		
	gensim_dictionary.save_as_text(paths.path_data_dictionary_txt)
	gensim_dictionary.save(paths.path_data_dictionary_dict)

	# print(gensim_dictionary.token2id)
	print(gensim_dictionary)


def build_corpus_gensim():
	""" build common corpus using common dictionary and combined and saves to file
	"""
	if load_corpus_gensim():
		return
	
	global gensim_corpus, common_corpus_list

	print('\nbuilding gensim corpus')

	gensim_corpus = [ gensim_dictionary.doc2bow(v[1].lower().split()) for v in common_corpus_list ]
	gensim.corpora.MmCorpus.serialize(paths.path_data_mmcorpus,gensim_corpus)
	# print(gensim_corpus)

	
def load_corpus_gensim():
	""" load common corpus from file
	"""
	global gensim_corpus
	if os.path.exists(paths.path_data_mmcorpus):
		print('\nloading gensim corpus')
		gensim_corpus = gensim.corpora.MmCorpus(paths.path_data_mmcorpus)
		print(gensim_corpus)
		return True
	else:
		return False

	
def transform_coord_to_vector(coords,vector_dim):
	""" unpacks inverted index to full vector_dim
	"""
	
	new_vector = [0] * vector_dim
	for c in coords:
		new_vector[c[0]] = c[1]

	return new_vector