#! /usr/bin/env python

def clean_whitespace(text):
	""" cleans whitespace by
		1. translating line breaks and tabs to spaces
		2. compressing multiple adjacent spaces to a single space
		3. trimming leading and trailing spaces
	"""
	text = text.translate(str.maketrans('\n\t','  '))
	text = ' '.join(text.split())
	text = text.strip()
	return text