#! /usr/bin/env python

def train_punkt_sent_tokenizer(train_ref,train_pickle):
    """ train punkt sentence tokenizer
    """
    
    import nltk.tokenize.punkt
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

    # read training corpus
    import codecs
    text = codecs.open(train_ref).read()
    tokenizer.train(text)

    # dump pickled tokenizer
    import pickle
    out = open(train_pickle,"wb")
    pickle.dump(tokenizer, out)
    out.close()