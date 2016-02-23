#! /usr/bin/env python

tac_xml_header = '<?xml version="1.0" encoding="ISO-8859-1"?>\n\
<TACtaskdata year="2006" track="SUMMARIZATION" task="GUIDED"  dataset="TRAIN">\n'
tac_xml_end = '</TACtaskdata>'

def rebuild_tac2011_topicxml_from_folder(data_folder, data_depth, duc_topicxml, tac_topicxml,category=1):
	""" creates TAC2011 topics.xml based on document folder structure
	"""
	
	# manifesting files
	from utils.recurse_folder import recurse_folder as recurse_folder
	filelist = recurse_folder(data_folder, data_depth)

	# from os.path import dirname, basename, isfile
	
	from collections import defaultdict
	topic_doc_dict = defaultdict(list)
	
	for f in filelist:
		farray = f.split('/')
		topic_id = farray[len(farray)-2]
		doc_id = farray[len(farray)-1]
		topic_doc_dict[topic_id].append(doc_id)
		
	from bs4 import BeautifulSoup
	
	with open(duc_topicxml, 'r') as txf:
		tx_data = txf.read().encode()

	tx_xml = BeautifulSoup(tx_data, "html.parser")

	fo = open(tac_topicxml, "w")
	fo.write(tac_xml_header)

	for t in tx_xml.find_all('topic'):
		title = t.find('title').get_text().strip()
		id = t.find('num').get_text().strip()
		narrative = t.find('narr').get_text().strip()

		fo.write('<topic id="' + id + '" category="' + str(category) + '">\n')
		fo.write('<title> ' + title + ' </title>\n')
		fo.write('<docsetA id="' + id + '-A">\n')
		
		for doc_id in topic_doc_dict[id+'-A']:
			fo.write('<doc id="'+ doc_id +'" />\n')
		
		fo.write('</docsetA>\n')
		fo.write('</topic>\n')

	fo.write(tac_xml_end)
	fo.close()

	