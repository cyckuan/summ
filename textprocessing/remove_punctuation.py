#! /usr/bin/env python

def replace_punctuation(raw):
    """ removes punctuation from a given string
    """
    punct = set(string.punctuation)

    return ''.join([r for r in raw if r not in punct])
