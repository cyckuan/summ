#! /usr/bin/env python

tac_xml_header = '<?xml version="1.0" encoding="ISO-8859-1"?>\n\
<TACtaskdata year="2006" track="SUMMARIZATION" task="GUIDED"  dataset="TRAIN">\n'
tac_xml_end = '</TACtaskdata>'

def convert_topicxml_duc_to_tac(duc_topicxml,tac_topicxml,all_docs,filtered_docs,category=1):
	""" converts topics.xml from duc format to tac
	"""
	
	from bs4 import BeautifulSoup
	
	with open(duc_topicxml, 'r') as txf:
		tx_data = txf.read().encode()

	tx_xml = BeautifulSoup(tx_data, "html.parser")

	import os
	import shutil
	
	fo = open(tac_topicxml, "w")
	fo.write(tac_xml_header)

	for t in tx_xml.find_all('topic'):
		title = t.find('title').get_text().strip()
		id = t.find('num').get_text().strip()
		narrative = t.find('narr').get_text().strip()
		docs = t.find('docs').get_text().strip()

		fo.write('<topic id="' + id + '" category="' + str(category) + '">\n')
		fo.write('<title> ' + title + ' </title>\n')
		fo.write('<docsetA id="' + id + '-A">\n')
		
		for d in docs.split('\n'):
			fo.write('<doc id="'+ d +'" />\n')
			
			filtered_set = filtered_docs + '/sets/' + id + '-A'
			if not os.path.exists(filtered_set):
				os.makedirs(filtered_set)
			shutil.copy(all_docs + '/' + d,filtered_set + '/' + d)
		
		fo.write('</docsetA>\n')
		fo.write('</topic>\n')
		
	fo.write(tac_xml_end)
	
	fo.close()

