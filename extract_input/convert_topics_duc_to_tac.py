#! /usr/bin/env python

tac_xml_header = '<?xml version="1.0" encoding="ISO-8859-1"?>\n\
<TACtaskdata year="2006" track="SUMMARIZATION" task="GUIDED"  dataset="TRAIN">'
tac_xml_end = '</TACtaskdata>'

def convert_topics_duc_to_tac(duc_topics_xml,tac_topics_xml,all_docs,filtered_docs,category=1):
	""" converts topics.xml from duc format to tac
	"""
	
	import lxml
	from bs4 import BeautifulSoup
	
	with open(duc_topics_xml, 'r') as txf:
		tx_data = txf.read().encode()

	tx_xml = BeautifulSoup(tx_data, "html.parser")

	import os
	import shutil
	
	fo = open(tac_topics_xml, "w")
	fo.write(tac_xml_header)

	for t in tx_xml.find_all('topic'):
		title = t.find('title').get_text().strip()
		id = t.find('num').get_text().strip()
		narrative = t.find('narr').get_text().strip()
		docs = t.find('docs').get_text().strip()

		fo.write('<topic id="' + id + '" category="' + str(category) + '">')
		fo.write('<title> ' + title + ' </title>')
		fo.write('<docsetA id="' + id + '-A">')
		
		for d in docs.split('\n'):
			fo.write('<doc id="'+ d +'" />')
			
			filtered_set = filtered_docs + '/sets/' + id + '-A'
			if not os.path.exists(filtered_set):
				os.makedirs(filtered_set)
			shutil.copy(all_docs + '/' + d,filtered_set + '/' + d)
		
		fo.write('</docsetA>')
		fo.write('</topic>')
		
	fo.write(tac_xml_end)
	
	fo.close()

