#! /usr/bin/env python

def train_model(model,document_path):
    """ augment the word2vec model by training new documents
    """
    import gensim
    
    
    with open(document_path,'r') as rf:
        sentences = rf.read().split('\n')
        print(sentences)

    
    model.build_vocab(sentences)
    model.train(sentences)
    
    model.init_sims(replace=True)
    
    return model