# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:52:05 2019

@author: Nicolai Berk
"""

#%% setup
import csv
import sys
from urllib import request
from lxml import html
import time
from random import randint
import datetime
from sys import stdout
import os.path

basedir = os.path.expanduser('~/Dropbox/Studies/Semester 2/Block I/data_IMEM/intermediate/')

maxInt = sys.maxsize

# should prevent getting kicked off server, see https://stackoverflow.com/questions/54687304/python-web-scraping-zacks-website-error-winerror-10054-an-existing-connection
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',}

while True:
    # set the maximum field size limit and decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs. to get somewhere in the range of a
    # maximum value of the field size limit
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

#%% Scraping releases
releases = []
deadLinks = []
i = 0
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))


print("Collecting parties' press releases....")

with open(basedir+'Links20190516-190202.csv', mode="r", encoding="utf-8") as fi:
    with open(basedir+"Releases"+dt+".csv",mode="w", encoding="utf-8") as fo:
        with open(basedir+'Deadlinks' + dt + '.csv', mode="w", encoding="utf-8") as dl:
            
            # open csv to read links
            reader = csv.reader(fi)
            
            # open csv to write to
            writer = csv.writer(fo, lineterminator='\n')
            
            # open csv to write failed links to that can be collected later on if necessary
            dead_writer = csv.writer(dl, lineterminator='\n')

            # loop through links
            for row in reader:
                
                # print progress bar for ~30,000 releases
                bar = str('\t[' + '='*int((i / 1000)) + ' '*(30-int((i / 1000))) + ']  | ' + str(i) + ' / approx. 30,000')
                stdout.write('%s\r' % bar)
                stdout.flush()
                
                try:
                    
                    # define xpath dependent on the website scraped from
                    if row[1] == 'CDU':
                        xpathTxt = '/html/body/main/div[2]/div/article/div/p/text()'
                    elif row[1] == 'SPD':
                        xpathTxt = '//*[@id="block-system-main"]/div/section/div[1]/div//text()'
                    else:
                        dead_writer.writerow(row[3])
                        print('\n\tUnknown sender, skip row')
                        break
                    
                    # empty text string to write press release to
                    txt = ''
                    
                    # take link collected earlier
                    fetchLink = row[3]
                    
                    # short sleep time between access of new links
                    time.sleep(randint(1, 2))
                    for attempt in range(3):
                        try:
                            
                            # fetch link, get html
                            req = request.Request(fetchLink,  headers = header)
                            tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8", errors="ignore"))
                        
                        # in case of URLError, wait 5 seconds and try again 
                        except request.URLError:
                            print("\n\tWhoops, that went wrong, retrying page " + fetchLink)
                            time.sleep(5)
                            
                            # if already tried twice, give up and put in dead-link-list
                            if attempt == 2:
                                print("\n\tFetching result page " + fetchLink + " failed due to URLError")
                                dead_writer.writerow(fetchLink)
                                break
                            
                        # similar for HTTPError
                        except request.HTTPError:
                            print("\n\tWhoops, that went wrong, retrying page " + fetchLink)
                            time.sleep(5)
                            if attempt == 2:
                                print("\n\tFetching result page " + fetchLink + " failed due to HTTPError")
                                dead_writer.writerow(fetchLink)
                                break
                        
                        # similar for unknown errors (differentiation to identify errors that could be fixed)
                        except:
                            print("\n\tUnknown error, retrying page " + fetchLink)
                            time.sleep(5)
                            if attempt == 2:
                                print("\n\tFetching result page " + fetchLink + " failed due to unknown Error")
                                dead_writer.writerow(fetchLink)
                                break
                    
                    # bind text together
                    for tt in tree.xpath(xpathTxt):
                        txt = str(txt + tt)
                    
                    # get rid of line breaks that would mess up csv
                    txt = " ".join(txt.split("\n")) # this prevents line breaks when writing nto csv
                    
                    # append to existing row from linkscraper output
                    row.append(txt)
                    writer.writerow(row)
                    
                    #indicate that it worked in deadlinks so they have the same length as input file
                    dead_writer.writerow('0')
                    
                    # increase counter for collected texts
                    i += 1
                    
                    # exception for unexpected sender in csv
                except IndexError:
                    deadLinks.append(row[3])
                    print('Unknown sender, skip row')
              
# output indicating successful collection and number of links collected
print('\n\nFinished fetching ' + str(i) + ' press releases.')
