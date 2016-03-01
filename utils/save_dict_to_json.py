#! /usr/bin/env python

def save_dict_to_json(data_dict,json_file):
    """ saves data to json file
    """
    import json
    f = open(json_file,"w")
    json.dump(data_dict, f, indent=4) # sort_keys=True, ensure_ascii = False
    f.close()
    
 