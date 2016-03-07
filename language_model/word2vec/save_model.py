#! /usr/bin/env python

def save_model(model,model_path):
    """ saves model for future use
    """
    import gensim
    model.save(model_path)