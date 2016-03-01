#! /usr/bin/env python

def build_stopword_dict(path_stopwords):
    """ extends nltk stopwords and saves to file
    """

    import os
    import nltk

    print('\nbuilding stopwords')

    # if load_stopwords():
    #   return

    stopwords = nltk.corpus.stopwords.words('english')
    for f in os.listdir(path_stopwords):
        filepath = path_stopwords  + '/' + f
        with open(filepath,'r') as f:
            for l in f:
                w = l.strip()
                w = re.sub(r"[\x80-\xff]"," ",w)
                if (w not in stopwords):
                    stopwords.append(w)

    # wip improve with POS and remove numbers
    # with open(paths.path_data_stopwords_txt,'w') as outf:
    #    outf.write('\n'.join(stopwords))

    print('\nstopword count : ' + str(len(stopwords)))
    
    return stopwords