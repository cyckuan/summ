#! /usr/bin/env python

def tokenize_sentence(raw):

    from nltk.tokenize import sent_tokenize
    from textprocessing.clean_whitespace import clean_whitespace as clean_whitespace
    
    prefix_sig = ['-- ','--',') _',') -']
    result = []
    
    text = clean_whitespace(raw)
    for s in sent_tokenize(text):
        for p in prefix_sig:
            sig_pos = s.find(p)
            if sig_pos >= 0:
                s = s[sig_pos+len(p):].strip()
        result.append(s)
        
    return result