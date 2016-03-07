#! /usr/bin/env python

def repair_duc_data(input_basename):
    """ repair idiosyncratic data issues
    """

    import json
    import re

    from textprocessing.clean_whitespace import clean_whitespace as clean_whitespace
    
    # reading in json
    from utils.load_json_to_dict import load_json_to_dict as load_json_to_dict
    from utils.save_dict_to_json import save_dict_to_json as save_dict_to_json
    
    text_data = load_json_to_dict(input_basename + '.json')
    
    altered = []
    deleted = []
    
    for k, v in text_data.items():
        karray = k.split('_')

        change_count = 1
        while change_count > 0:
            change_count = 0
            
            # fix text
            max_i = len(v) - 1
            for i,e in enumerate(v):
                lcase_e = e.lower()
                orig_e = e

                # remove initial part of first sentences
                if i <= 5 and e.find('c.19') > -1 or e.find('c.20') > -1 or e.find('Copyright') > -1:
                    for p in [
                        '_',
                        '--',
                        '-COX',
                        '-Global',
                        '-NYT',
                        'News Service',
                        'Houston Chronicle',
                        'Seattle Post-Intelligencer',
                        'Fort Worth Star-Telegram',
                        'Spirit magazine',
                        'The Boston Globe',
                        'The Arizona Republic(a)',
                        'The Arizona Republic',
                        'San Antonio Express-News',
                        'Child magazine',
                        'New Scientist',
                        'INTERNATIONAL CUBA-ELIAN MIAMI'
                    ]:
                        altered.append(e)

                        found = False
                        pos = e.find(p)
                        if pos > -1:
                            e = e[pos+len(p):]
                            lcase_e = e.lower()
                            found = True
                        else:
                            e_words = e.strip().split(' ')
                            first_copyright = -1
                            first_proper_lower = -1
                            for ei in range(0,len(e_words)-1):
                                if first_copyright < 0 and (e_words[ei][0:2] == 'c.' or e_words[ei] == 'Copyright'):
                                    first_copyright = ei
                                if first_copyright > 0 and e_words[ei] == e_words[ei].title() and e_words[ei+1] == e_words[ei+1].lower():
                                    first_proper_lower = ei
                                    found = True
                                    break
                            if found:
                                e = ' '.join(e_words[first_proper_lower:])

                        if found and i > 0:
                            
                            if i >= len(v):
                                i = len(v)
                            
                            for j in range(0,i):
                                deleted.append(v[0])
                                del v[0]
                                change_count += 1

                        altered.append(e)

                            
                if change_count > 0:
                    break

                # remove entire sentences

                incl_sentence = True
                
                for p in [
                    'NYT',
                    'AP',
                    'XIE'
                ]:
                    if i == 0 or i == max_i:
                        incl_sentence = incl_sentence and not (e[:len(p)] == p)

                for p in [
                    'http',
                    'is being sent to',
                    'contains items from',
                    'news story',
                    'news service',
                    'centerpiece clients',
                    '(profile',
                    'subscribers',
                    'this is an analysis',
                    'photo is being sent to',
                    'for use by clients of',
                    'information about purchasing',
                    'can make individual purchases',
                    'article has been transmitted',
                    'regret that this material',
                    'editors'
                ]:
                    incl_sentence = incl_sentence and lcase_e.find(p) == -1

                for p in [
                    ['nyt','edt'],
                    ['nyt','est']
                ]:
                    b = True
                    for pp in p:
                        b = b and lcase_e.find(pp) > -1
                    incl_sentence = incl_sentence and not b
                    
                if not incl_sentence:
                    deleted.append(e)
                    del v[i]
                    change_count += 1
                    break

                # remove location typically found in NYT articles
                
                e_words = e.strip().split(' ')
                first_comma = -1
                first_noncaps = -1
                first_cap = -1
                for ei, ea in enumerate(e_words):
                    if first_cap < 0 and ea.upper() != ea:
                        break
                    else:
                        first_cap = ei
                    if first_comma < 0 and ea[-1:] == ',' and ea.upper() == ea:
                        first_comma = ei
                        break
                    if first_noncaps < 0 and ea.upper() != ea:
                        first_noncaps = ei
                        break
                
                if first_cap >= 0:
                    altered.append(e)
                    last_loc_word = max(first_comma+1,first_noncaps-1)
                    e = ' '.join(e_words[last_loc_word+1:])
                    altered.append(e)
                                                        
                # remove between tags

                found = True
                while found:
                    found = False
                    for p in [
                        ['By','_'],
                        ['NYT','_'],
                        ['&HT;','_'],
                        ['&QL;','_'],
                        ['ENDIT','&QL;'],
                        ['&QL;','&QL;'],
                        ['&HT;','&HT;'],
                        ['NYT','&QL;'],
                        ['XXX','&QL;']
                    ]:
                        pos_left = e.find(p[0])
                        if pos_left > -1:
                            pos_right = e.rfind(p[1])
                            if pos_right > -1 and pos_right > pos_left:
                                found = True

                                altered.append(e)
                                
                                pos_right += len(p[1])
                                if pos_left == 0:
                                    e = e[pos_right:]
                                else:
                                    e = e[0:pos_left] + e[pos_right:]
                                lcase_e = e.lower()
                                
                                altered.append(e)
                                
                
                # remove matching part of sentence at beginning of sentence

                found = True
                while found:
                    found = False
                    for p in [
                        'nn '
                    ]:
                        pos = lcase_e.find(p)
                        if p == lcase_e[:len(p)]:
                            found = True

                            altered.append(e)
                            
                            e = e[len(p):]
                            lcase_e = lcase_e[len(p):]
                            
                            altered.append(e)

                            
                # remove matching part of sentence

                found = True
                while found:
                    found = False
                    for p in [
                        '(story can end here',
                        '(story could end here',
                        'optional adds follow)',
                        'optional material follows)',
                        'optional material follows.)',
                        'optional material follow)',
                        '; optional add follows.)',
                        '(first optional trim ends)',
                        '(begin optional trim)',
                        '(end optional trim)'
                    ]:
                        pos = lcase_e.find(p)
                        if pos > -1:
                            found = True

                            altered.append(e)
                            
                            if pos == 0:
                                e = e[len(p):]
                            else:
                                e = e[0:pos] + e[pos+len(p):]
                            lcase_e = e.lower()
                            
                            altered.append(e)


                # string replace punctuation

                for p in [
                    [' nn ',' '],
                    ['_','']
                ]:
                    e = e.replace(p[0], p[1])

                # regex replace whole line

                e = re.sub(r".*[0-9]{3}-[0-9]{3}-[0-9]{4}.*", "", e)
                e = re.sub(r".*[0-9]{3,4}E[DS]T.*", "", e)

                # regex replace short tags

                e = re.sub(r"\&[a-zA-Z0-9]+\;", "", e)
                e = re.sub(r"\([a-z]+\)", "", e)
                e = re.sub(r"[0-9] [0-9]{4}", "", e)

                # remove whitespace

                e = clean_whitespace(e)

                if orig_e != e:
                    altered.append(orig_e)
                    altered.append(e)
                    # change_count += 1
                    
                # not blanked

                if e == '' or e == '.':
                    del v[i]
                else:
                    v[i] = e
                    
            # rejoin incorrectly segmented sentences

            rejoin_count = 1
            while rejoin_count > 0:
                rejoin_count = 0
                max_i = len(v) - 1
                
                for i,e in enumerate(v):
                    e = e.strip()
                    if i < max_i:
                        if v[i+1][0:1].islower():
                            e = e + ' ' + v[i+1]
                            del v[i+1]
                            max_i -= 1
                            rejoin_count += 1

                    if i < max_i:
                        for p in [
                            'Gov.',
                            'No.'
                        ]:
                            if e[-len(p):] == p:
                                e = e + ' ' + v[i+1]
                                del v[i+1]
                                max_i -= 1
                                rejoin_count += 1
                    
                    if rejoin_count > 0:
                        break
                            
                            
        print()
        for e in v:
            print('[' + e.strip() + ']')
        
        text_data[k] = v
        
    save_dict_to_json(text_data, input_basename + '_repped.json')
    save_dict_to_json(altered, input_basename + '_altered.json')
    save_dict_to_json(deleted, input_basename + '_deleted.json')
    
    print()
    print('repped : ' + str(len(text_data)))
    print('altered : ' + str(len(altered)))
    print('deleted : ' + str(len(deleted)))