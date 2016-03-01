#! /usr/bin/env python

def extract_sentences_from_text(text_path,output_basename,folder_depth=0):
    """ extract sentences from summaries for sentence specificity scoring using speciteller
    """
    import json

    # manifesting files
    from utils.recurse_folder import recurse_folder as recurse_folder
    filelist = recurse_folder(text_path, folder_depth)

    # text processing functions
    from textprocessing.tokenize_sentence import tokenize_sentence as tokenize_sentence
    from textprocessing.remove_tags import remove_tags as remove_tags
    
    from utils.save_dict_to_json import save_dict_to_json as save_dict_to_json

    from collections import defaultdict
    text_data = defaultdict(list)

    with open(output_basename + '.txt', 'w') as sf, open(output_basename + '.map', 'w') as sm:
        for f in filelist:
            farray = f.split('/')
            flen = len(farray)
            fbase = farray[flen-1]
            fset = farray[flen-2]
            fsetbase = fset+'_'+fbase
            
            with open(f, 'r', encoding='ISO-8859-1') as f:
                sentences = tokenize_sentence(remove_tags(f.read()))
                print("sentence count : " + str(len(sentences))) # includes empty lines
                
                for i,s in enumerate(sentences):
                    if s != '': # excludes empty lines
                        sf.write(s+'\n')
                        sm.write(s+'\n')
                
                text_data[fsetbase] = sentences
    
    save_dict_to_json(text_data, output_basename + '.json')

"""
problems:
"(PROFILE (WS SL:BC-China-Unrest; CT:i; (REG:EURO;) (REG:BRIT;) (REG:SCAN;) (REG:MEST;) (REG:AFRI;) (REG:INDI;) (REG:ENGL;) (REG:ASIA;) (LANG:ENGLISH;)) ) AP-NY-08-29-98 0502EDT"
"Copyright 1998 THE INDEPENDENT all rights reserved as distributed by WorldSources, Inc. (PROFILE (WS SL:ANTARCTICA-IN-THE-GRIP sked; CT:w; (REG:ENGL;) (LANG:ENGLISH;)) ) AP-NY-06-10-98 1109EDT"
"APW19980610.0858 NEWS STORY 06/10/1998 11:09:00 w1228 &Cx1f; wstm- r w &Cx13; &Cx11; ANTARCTICA-IN-THE-GRIPsk 06-10 0939 ANTARCTICA-IN-THE-GRIP sked Antarctica in the grip of global warming, THE INDEPENDENT Antarctica in the grip of global warming, THE INDEPENDENT &QL; June 10, 1998 THE INDEPENDENT BANGLADESH ENGLISH Danielle KnightASIA WorldSources, Inc. 201 PENNSYLVANIA AVENUE, S.E., 2nd Floor WASHINGTON, D.C. 20003 Tel: 202-547-4512 Fax: 202-546-4194 COPYRIGHT 1998 BY WORLDSOURCES, INC., A JOINT VENTURE OF FDCH, INC. AND WORLD TIMES, INC. NO PORTION OF THE MATERIALS CONTAINED HEREIN MAY BE USED IN ANY MEDIA WITHOUT ATTRIBUTION TO WORLDSOURCES, INC. Greenhouse gas emissions - blamed for global warming - may cause the collapse of the West Antarctic Ice Sheet and raise the average global sea level by four to six metres, beginning as early as the next century, a new scientific study predicted recently."
"http://www.millionmommarch.com/mission.html Women Against Gun Control (anti-march) _ http://www.wagc.com Andrew Mollison's e-mail address is andym(at)coxnews.com ENDIT Story Filed By Cox Newspapers For Use By Clients of the New York Times News Service NYT-04-12-00 1154EDT &QL;"
"(Story can end here.",
"Optional adds follow) ``A drill for a bomb threat is just like a fire drill, only it takes longer,'' said Kelly Boyd, a high school junior in Montgomery County, Md.",

"NYT19990227.0091 NEWS STORY 1999-02-27 12:45 A1573 &Cx1f; tta-z u a &Cx13; &Cx11; BC-CRACK-LEGACY-I-ART-5T 02-27 1163 BC-CRACK-LEGACY-I-ART-5TAKES-NYT THE WAR ON DRUGS RETREATS, STILL TAKING PRISONERS (ATTN: Calif., Pa., Kan., Ky., Mass., Texas, Fla., Mich.) (Eds: This is the first of two articles.",
"Next: The police arm themselves for the war on drugs.)",
"(ART ADV: Photo is being sent to NYT photo clients.",
"Graphic is being sent to NYT graphic clients.",
"Non-subscribers can make individual purchase by calling (888) 603-1036 or (888) 346-9867.)",
"XIE19981104.0056 1998-11-04 U.S.",
"E-mail Tom Abate at &LR; abate(AT)sfgate.com &LR; .",
"NYT19991009.0071 NEWS STORY 1999-10-09 11:57 A1626 &Cx1f; tta-z u a BC-KANSAS-CREATIONISM-12 10-09 1317 BC-KANSAS-CREATIONISM-1250(2TAKES)-NYT SCIENCE VS.",
"THE BIBLE.",
"DEBATE MOVES TO THE COSMOS (jt) By JAMES GLANZ c.1999 N.Y.        
 
    
sub markBreaks {

    my($text) = @_;
    my $t ="";

    # move period, exclamation/question mark after following quote mark
    # and separate with blank. 
    $text =~ s/([\.\!\?]+)([\"\'\)]+) /$2$1 /g;

    # w+{ becomes w+ {   - peculiarity of some newspaper data
    #$text =~ s/(\w+)({)/$1 $2 /g;
    $text =~ s/(\w+)({)/$1/g;

    # remove ; following . ? ! (SJMN peculiarity)
    $text =~ s/([\.\!\?])( *;)/$1/g;
	
    # a series of whitespace chars becomes a space	     
    $text =~ s/\s+/ /g;

    # insert a space before each comma
    $text =~ s/,/ ,/g;

    # this loop handles periods and ellipsis as well as question and 
    # exclamation marks - finding and marking each sentence-ending 
    # instance by inserting an end-of-sentence marker (\n)
    # - $1 has ? to minimize its matching so $2 can match maxmimally
    # and recognize ...
    # - $3 needs to be able to contain / end with punctuation e.g.,
    # an abbreviation starting the next sentence

    while ($text =~ / (\S+?)(\.\.\.|\.|\?|\!) +(\S+)( .+)$/) {
       my $pre = $1; 
       my $delim = $2;
       my $post = $3; 
       my $rest = $4;
       my $skipped = substr($text,0,length($text)-1-length($1.$2.$3.$4));

       $fullpost = $post;
       if (substr($post,-1) eq ".") {
	   chop $post;
       }

       if ($debug) 
       {
	   print "TEXT+[$text]\n";
	   print "\nSKI=[$skipped]\nPRE=[$pre]\nDELIM=[$delim]\nPOS=[$post]\nRES=[$rest]\n";
	   if ($pre =~ /^\w+\.\w+/) {print "$pre WITHPERIOD\n";}
	   if ($abbrevs{$pre} == 1 || $abbrevs{$pre} == 2) {print "$pre ABBREVIATION\n";}
	   if ($pnouns{$post}) {print "$post PROPER\n";}
       }
       # if the word before the delimiter is an appreviation that can't
       # end a sentence, then continue the current sentence.

       # Else if the word before the delimiter can legitimately precede
       # the delimiter and the word after the delimiter
       # is usually capitalized or is lowercase then mark the
       # period/ellipsis as NOT ending a sentence; otherwise mark
       # it as ending a sentence.
       if ( 	    
            ($abbrevs{$pre} == 2)
	    ||
	    (
	      (
	       $pre =~ /^\w+\.\w+/ || ($abbrevs{$pre} == 1) || 
               $delim eq "..."     || $delim eq "?"  || $delim eq "!"
	      ) 
              &&       
	      ($pnouns{$post} || $post =~ /^[a-zß-ÿ0-9,;:\-\.]/)  
            )   
	  )    
       {  
	   # C o n t i n u e   c u r r e n t   s e n t e n c e
	   $t .= $skipped.$pre."$delim ";
	   $restoredspaces = " ";
       }
       else 
       {
	   # M a k e   t h i s   a   s e n t e n c e - f i n a l   p e r i o d
	   $t .= $skipped.$pre.$delim."\n";
	   # lack of in initial space prevents a sentence initial abbrev.
	   # from being interpreted as sentence-terminating - we want this
	   # though it means one word sentences will be concatenated with
	   # the following.
	   $restoredspaces = ""; 
       }
       $text = $restoredspaces.$fullpost.$rest;
   }# endwhile

   $text = $t . $text;

   $text =~ s/\. *$/ ./; # final period will be followed by exactly 1 space
   $text =~ s/ +/ /g; # multiple spaces become one
   $text =~ s/^ //g;  # leading space is removed
   $text =~ s/ $//g;  # trailing space is removed

   $text =~ s/ ,/,/g; # remove the (added) space before commas

   $text .= "\n" unless $text =~ /\n$/; 

   $textout = "";
   @sentlist = split /\n/,$text;
   foreach $s (@sentlist)
   {
        $textout .= "$s\n";
   }
   $textout =~ s/ \././;
   return $textout;
}    
    
"""