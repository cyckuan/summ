#! /usr/bin/env python

def load_model(model_file):
    """ loads pre-trained model into memory
        example: '/data/sourcedata/word2vec/GoogleNews-vectors-negative300.bin.gz'
    """ 
    import gensim, logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = gensim.models.Word2Vec.load_word2vec_format(model_file,binary=True)
    
    return model