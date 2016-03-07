#! /usr/bin/env python

""" top-level summarisation pipeline
"""



def main():

    from params import paths as paths

    from language_model.word2vec_pipeline import word2vec_pipeline as word2vec_pipeline
    word2vec_pipeline('/data/sourcedata/word2vec/GoogleNews-vectors-negative300.bin.gz','/data/summ/data/test.txt','/data/summ/data/w2v.model')

    
if __name__ == '__main__':
    main()

