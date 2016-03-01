#! /usr/bin/env python

def load_json_to_dict(json_file):
    """ loads json file into a python dict
    """
    
    import json

    f = open(json_file,"r")
    new_dict = json.load(f)
    f.close()

    return new_dict