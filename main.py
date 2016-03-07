#! /usr/bin/env python

""" top-level summarisation pipeline
"""



def main():

    from params import paths as paths

    # from extract_input.partition_original_docs import partition_original_docs as partition_original_docs

    # prep data for DUC 
    # partition_original_docs(paths.source_aquaint_original,3,paths.source_aquaint_docs,False)

    # prep data for TAC 
    # partition_original_docs(paths.source_aquaint2_original,2,paths.source_aquaint2_docs,False)

    # from extract_input.convert_topicxml_duc_to_tac import convert_topicxml_duc_to_tac as convert_topicxml_duc_to_tac
    # convert_topicxml_duc_to_tac(paths.source_duc2007_topicxml_orig,paths.source_duc2007_topicxml,paths.source_aquaint_docs,paths.source_duc2007_docs)

    # from extract_input.rebuild_tac2011_topicxml_from_folder import rebuild_tac2011_topicxml_from_folder as rebuild_tac2011_topicxml_from_folder
    # rebuild_tac2011_topicxml_from_folder(paths.source_duc2006_docs,2,paths.source_duc2006_topicxml_orig,paths.source_duc2006_topicxml)

    # from evaluation.rename_rouge_files import rename_rouge_files as rename_rouge_files
    # rename_rouge_files(paths.source_duc2006_modelsummaries,0,'','-A')

    # /data/sourcedata/stopwords
    
    from preprocessing.extract_sentences_from_text import extract_sentences_from_text as extract_sentences_from_text
    from preprocessing.repair_duc_data import repair_duc_data as repair_duc_data
    from preprocessing.rebuild_doc_set import rebuild_doc_set as rebuild_doc_set
    
    # extract_sentences_from_text('/data/sourcedata/aquaint/docs','xml1','/data/summ/aquaint',0)
    # extract_sentences_from_text('/data/sourcedata/aquaint2/docs','xml2','/data/summ/aquaint2',0)
        
    extract_sentences_from_text('/data/swing/SWING/data/duc2006/docs','xml1','/data/summ/original_sentences_duc2006',2)
    repair_duc_data('/data/summ/original_sentences_duc2006')
    # rebuild_doc_set('/data/summ/original_sentences_duc2006','/data/swing/SWING/data/duc2006/docs_cleaned/sets')
    
    extract_sentences_from_text('/data/swing/SWING/data/duc2007/docs','xml1','/data/summ/original_sentences_duc2007',2)
    repair_duc_data('/data/summ/original_sentences_duc2007')
    # rebuild_doc_set('/data/summ/original_sentences_duc2007','/data/swing/SWING/data/duc2007/docs_cleaned/sets')
    
    #extract_sentences_from_text('/data/swing/SWING/evaluation/duc2007/ROUGE/models','/data/summ/summary_sentences_duc2007_models')
    #extract_sentences_from_text('/data/swing/SWING/data/Summaries/csi.sentence','/data/summ/summary_sentences_duc2007_peers')
    
    #extract_sentences_from_text('/data/swing/SWING/data/duc2007','/data/summ/original_sentences_duc2007',3)
    
    #from subprocess import call

    #for f in [
    #    'original_sentences_duc2006.txt',
    #    'original_sentences_duc2007.txt',
    #    'summary_sentences_duc2006_models.txt',
    #    'summary_sentences_duc2007_models.txt',
    #    'summary_sentences_duc2007_peers.txt'
    #]:
    #    cmd = "python"
    #    file = "/data/speciteller/speciteller/speciteller.py"
    #    call([cmd,file,"--input",f,"--output","scores_" + f])
    
    # from language_model.word2vec_sentence import word2vec_sentence as word2vec_sentence
    # word2vec_sentence('test')
    
if __name__ == '__main__':
    main()


    
    
