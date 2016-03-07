#! /usr/bin/env python

def rebuild_doc_set(input_basename,document_path):
    """ rebuilds document sets for NUS/SWING consumption
    """
    import os
    
    from utils.load_json_to_dict import load_json_to_dict as load_json_to_dict
    
    text_data = load_json_to_dict(input_basename + '_repped.json')
    text_header = load_json_to_dict(input_basename + '_header.json')
    
    for k,v in text_data.items():
        karray = k.split('_')
        print(k)
        
        folder_path = document_path + '/' + karray[0]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        full_document_path = folder_path + '/' + karray[1]
        with open(full_document_path, 'w') as df:
            df.write('\n'.join(v))
            

        
