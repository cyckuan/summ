#! /usr/bin/env python

def create_single_corpus(input_basename):
    """ create a large consolidated corpus of sentences
    """
    import os
    
    from utils.load_json_to_dict import load_json_to_dict as load_json_to_dict
    
    text_data = load_json_to_dict(input_basename + '_repped.json')
    corpus_path = load_json_to_dict(input_basename + '_corpus.txt')
    
    for k,v in text_data.items():
        print(k)
        
        with open(corpus_path,'w') as f:
            for s in v:
                f.write(s + '\n')
