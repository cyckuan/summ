#! /usr/bin/env python

def word2vec_pipeline(in_model_path,document_path,out_model_path):

    import gensim

    from language_model.word2vec.load_model import load_model as load_model
    from language_model.word2vec.train_model import train_model as train_model
    from language_model.word2vec.save_model import save_model as save_model
    
    from textprocessing.remove_punctuation import remove_punctuation as remove_punctuation

    with open(document_path,'r') as rf:
        sentences = rf.read().split('\n')
        print(sentences)    
    
    #model = load_model(in_model_path)
    model = gensim.models.word2vec.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model = train_model(model,document_path)
    save_model(model,out_model_path)
    
    print('word2vec pipeline completes :)')
    
    """
    with open('/data/swing/SWING/data/sentences_train.txt', 'r') as rf:
        for s in rf.read().split('\n'):
            s_len = len(s)
            for w in s.split(' '):
                wc = remove_punctuation(w.lower().strip())
                if wc in model.keys():
                    print(w + ' : ' + str(model[wc]))
    """
          
        
    

    