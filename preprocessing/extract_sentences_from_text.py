#! /usr/bin/env python

def extract_sentences_from_text(text_path,text_type,output_basename,folder_depth=0):
    """ extract sentences from summaries for sentence specificity scoring using speciteller
    """
    import json

    # manifesting files
    from utils.recurse_folder import recurse_folder as recurse_folder
    filelist = recurse_folder(text_path, folder_depth)

    # text processing functions
    from textprocessing.tokenize_sentence import tokenize_sentence as tokenize_sentence
    from textprocessing.remove_tags import remove_tags as remove_tags
    from textprocessing.clean_whitespace import clean_whitespace as clean_whitespace
    
    from utils.save_dict_to_json import save_dict_to_json as save_dict_to_json

    from collections import defaultdict
    text_data = defaultdict(list)
    text_header = defaultdict(list)
    
    import lxml
    from bs4 import BeautifulSoup

    for f in filelist:
        farray = f.split('/')
        flen = len(farray)
        fbase = farray[flen-1]
        fset = farray[flen-2]
        fsetbase = fset+'_'+fbase
        
        skip = False
        with open(f, 'r', encoding='ISO-8859-1') as ff:
            
            print(f)
        
            raw_data = clean_whitespace(ff.read())
            
            # DUC xml format
            if text_type == 'xml1':
                d = BeautifulSoup(raw_data, "xml")

                doc = d.find('DOC')
                
                docid = doc.find('DOCNO')
                if docid is None:
                    docid = doc.find('DOCID')
                    if docid is None:
                        docid = ''
                    else:
                        docid = docid.get_text().strip()
                else:
                    docid = docid.get_text().strip()
                
                datetime = doc.find('DATELINE')
                if datetime is None:
                    datetime = ''
                else:
                    datetime = datetime.get_text().strip()
                
                body = doc.find('BODY')
                
                cat = body.find('CATEGORY')
                if cat is None:
                    cat = ''
                else:
                    cat = cat.get_text().strip()
                
                headline = body.find('HEADLINE')
                if headline is None:
                    headline = ''
                else:
                    headline = headline.get_text().strip()

                header = [docid,datetime,cat,headline]
                print(header)
                
                text = remove_tags(raw_data)
            
            # TAC xml format            
            elif text_type == 'xml2':
                d = BeautifulSoup(raw_data, "xml")

                doc = d.find('DOC')
                if doc is None:
                    skip = True
                else:
                    docid = doc['id']
                    
                    datetime = doc.find('DATELINE')
                    if datetime is None:
                        datetime = ''
                    else:
                        datetime = datetime.get_text().strip()
                    
                    cat = ''
                    
                    headline = doc.find('HEADLINE')
                    if headline is None:
                        headline = ''
                    else:
                        headline = headline.get_text().strip()

                    header = [docid,datetime,cat,headline]
                    print(header)
        
                    text = doc.find('TEXT')
                    if text is None:
                       text = ''
                    else:
                       text = text.get_text().strip()
            
            # text files
            else:
                header = []
                text = remove_tags(raw_data)
            
            if not skip:
                sentences = tokenize_sentence(text)
                print("sentence count : " + str(len(sentences))) # includes empty lines
                
                text_header[fsetbase] = header
                text_data[fsetbase] = sentences
    
    save_dict_to_json(text_header, output_basename + '_header.json')
    save_dict_to_json(text_data, output_basename + '.json')

