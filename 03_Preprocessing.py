# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:10:43 2019

@author: samunico
"""

#%% import
import csv
import datetime
import nltk
from nltk.stem.snowball import SnowballStemmer
import spacy
from sys import stdout
import os.path

basedir = os.path.expanduser('~/Dropbox/Studies/Semester 2/Block I/data_IMEM/intermediate/')

stemmer = SnowballStemmer('german')
nlp = spacy.load("de_core_news_sm")


#%% text processing 

# stemming, vectorizing, pos-tags
dt = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+'Releases20190516-190649.csv', mode="r", encoding="utf-8") as fi:
    with open(basedir+"Cleaned"+dt+".csv",mode="w", encoding="utf-8") as fo:                
        reader = csv.reader(fi)
        fieldnames = ['date', 'sender','title', 'link', 'raw', 'clean_full', 'clean_rest']
        writer = csv.DictWriter(fo, lineterminator='\n', fieldnames = fieldnames)
        writer.writeheader() # define header
        i = 0
        
        for row in reader:
            
            # output indicating progress
            bar = str('\t\t[' + '='*int((i)/ (1000)) + ' '*(30-int((i) / (1000))) + ']   ' + str((i)) + '/' + '30,000')
            stdout.write('%s\r' % bar)
            stdout.flush()
            
            # alternative classifiers: restrict analysis to adverbs, adjectives and nouns :
            doc = nlp(row[4])
            pos = [(w.text, w.pos_) for w in doc]
            postxt = ''
            for tp in pos:
                if tp[1] == 'ADJ' or tp[1] == 'NOUN' or tp[1] == 'ADV':
                    postxt = postxt + tp[0] + ' '
            
            # tokenize, once for full text, once for restricted version                        
            tokens_f = nltk.word_tokenize(row[4])
            tokens_r = nltk.word_tokenize(postxt)
            
            # stem
            stems_f = ''
            for w in tokens_f:
                stems_f = stems_f + stemmer.stem(w) + ' '
            row.append(stems_f)
            
            stems_r = ''
            for w in tokens_r:
                stems_r = stems_r + stemmer.stem(w) + ' '
            row.append(stems_r)
            
            # write to csv with headers
            writer.writerow({'date':        row[0], 
                            'sender':       row[1],
                            'title':        row[2], 
                            'link':         row[3], 
                            'raw':          row[4], 
                            'clean_full':   row[5], 
                            'clean_rest':   row[6]})
            i += 1