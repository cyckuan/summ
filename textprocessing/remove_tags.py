#! /usr/bin/env python

def remove_tags(text):
    """ removes markup tags from text
    """
    import re
    from re import sub
    return re.sub('<.*?>', '', text)