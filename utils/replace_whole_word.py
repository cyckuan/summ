#! /usr/bin/env python

def replace_whole_word(text,original_word,new_word):
	""" replaces word tokens
	"""
	
	from nltk.tokenize import word_tokenize
	
	lcase_original_word = original_word.lower()
	wordlist = word_tokenize(text)
	for i,w in enumerate(wordlist):
		if w.lower() == lcase_original_word:
			wordlist[i] = new_word
	
	return ' '.join(wordlist)