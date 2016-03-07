#! /usr/bin/env python

def partition_original_docs(raw_data, raw_data_depth, processed_data,verbose):
    """ extracts XML-based corpora and segment multi-document collections into single-document files
    """
    
    # manifesting files
    from utils.recurse_folder import recurse_folder as recurse_folder
    from textprocessing.clean_whitespace import clean_whitespace as clean_whitespace
    filelist = recurse_folder(raw_data,raw_data_depth)
    
    import os
    import gzip
    
    import lxml
    from bs4 import BeautifulSoup
    
    # lite doc xml parser
    doc_tag_start = b'<DOC'
    doc_tag_end = b'</DOC>'
    doc_end_len = len(doc_tag_end)

    file_count = 0
    total_doc_count = 0
    unique_doc_types = set()
    
    # traversing files
    for f in filelist:
    
        file_count += 1
    
        # aquaint data is stored in gz, aquaint2 in raw text
        if os.path.splitext(f)[1] == '.gz':
            with gzip.open(f, 'r') as df:
                original = df.read()
                original = original.replace(b'DOCNO',b'ID')
        else:
            with open(f, 'r') as df:
                original = df.read().encode()

        # traversing doc's within file
        doc_count = 0
        doc_start_pos = 0
        doc_start_pos = original.find(doc_tag_start, doc_start_pos)
        while doc_start_pos >= 0:
            doc_end_pos = original.find(doc_tag_end, doc_start_pos) + doc_end_len
            current_doc = original[doc_start_pos:doc_end_pos]
            doc_start_pos = original.find(doc_tag_start, doc_end_pos)
            doc_count += 1

            # d = BeautifulSoup(current_doc, "lxml-xml")
            d = BeautifulSoup(current_doc, "xml")

            doc = d.find('DOC')
            doc_id = doc['id'] if doc.has_attr('id') else ''

            doc_type = ''
            if doc.has_attr('type'):
                doc_type = doc['type']
                if doc_type not in unique_doc_types:
                    unique_doc_types.add(doc_type)

            h = d.find('HEADLINE')
            if h is None:
                main_headline = ''
            else:
                main_headline = clean_whitespace(h.get_text())
            
            title = ''
            titledone = ''
            text = ''
            textdone = ''
            
            article_complete = False
            doc_complete = False

            # traversing elements within doc
            for e in d.find_all():
                
                etext = clean_whitespace(e.get_text())
                
                # uncomment to reveal raw elements
                # print(e.name)
                # print(e.text)
                # print()

                # element traversal is necessary to extract subdivided or multi docs
                
                if e.name == 'ID':
                    doc_id = e.get_text().strip()

                if e.name == 'DOCTYPE':
                    doc_type = e.get_text().strip()
                    if doc_type not in unique_doc_types:
                        unique_doc_types.add(doc_type)
                
                if doc_type == '':
                    if e.name == 'HEADLINE':
                        doc_type = 'NEWS STORY'
                        titledone = main_headline
                        article_complete = False
                        doc_complete = False
                elif e.name == 'TEXT':
                    fulltext = etext
                    doc_complete = True
                    if doc_type == 'NEWS STORY' or doc_type == 'story':
                        textdone = etext
                        article_complete = True
                elif doc_type == 'SUBDIVIDED' or doc_type == 'multi':
                    if e.name == 'SUBHEADER':
                        titledone = title
                        textdone = text
                        article_complete = True
                        title = etext
                    elif e.name == 'P':
                        text = text + ' ' + etext
                
                # aquaint has doc_types {'NEWS STORY','SUBDIVIDED'}
                # aquaint2 has doc_types {'advis', 'multi', 'story', 'other'}
                
                # text before -- contain time, event, location data

                if article_complete:
                    print(str(file_count) + ' : ' + f)
                    print(doc_id)

                    if verbose:
                        print(doc_type)
                        print(titledone)
                        print(textdone)
                        print()
                    article_complete = False
                    
            if doc_complete and doc_id != '':
                fo = open(processed_data + '/' + doc_id, "w")
                # fo.write(main_headline + '\n' + fulltext)
                fo.write(current_doc.decode())
                fo.close()

        total_doc_count += doc_count

    print(unique_doc_types)
    print(total_doc_count)
    print(file_count)

    
    
    