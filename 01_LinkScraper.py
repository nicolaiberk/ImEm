# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:47:13 2019

BDACA Final Project
Part I: Linkscraping

@author: Nicolai Berk
"""

#%% meta
# Period: 01.01.2000 (CDU/CSU) and 28.10.2009 (SPD) until 8.5.2019 (start of project)
# this relates mainly to data availability

#%% import
from lxml import html
from urllib import request
from random import randint
import time
import datetime
import csv
import re
from sys import stdout
import os.path

#%% define function
def linkScraper(file,       # string indicating (path and) name of file that the output should be written to 
                senders,    # list of strings indicating sender of the press release
                urls,       # list of strings indicating url that links should be collected from, in formattable form
                linkbases,  # list of strings indicating linkbase that directed links should be appended to
                maxpages,   # list of integers indicating number of pages that the scraper should go through when formatting url
                npages,     # list of integers indicating number to multiply by in case url formatting is not following pattern [0,1,2,3, ...]
                xpathLinks, # list of strings indicating xpath to link of press release
                xpathTitles,# list of strings indicating xpath to title of pr
                xpathDates, # list of strings indicating xpath to date
                regexDates, # list of strings indicating regular expression to find date   
                strToDates  # list of strings for the transformation of string date to time var
                ):
    
    '''
    scrapes links for subsequent collection from and writes them to a csv
    
    ----------------------------------------------------------------------------------
    
    Parameters:
    
    file        # string indicating (path and) name of file that the output should be written to 
    senders     # list of strings indicating sender of the press release
    urls        # list of strings indicating url that links should be collected from, in formattable form
    linkbases   # list of strings indicating linkbase that directed links should be appended to
    maxpages    # list of integers indicating number of pages that the scraper should go through when formatting url
    npages      # list of integers indicating number to multiply by in case url formatting is not following pattern [0,1,2,3, ...]
    xpathLinks  # list of strings indicating xpath to link of press release
    xpathTitles # list of strings indicating xpath to title of pr
    xpathDates  # list of strings indicating xpath to date
    regexDates  # list of strings indicating regular expression to find date   
    strToDates  # list of strings for the transformation of string date to time var
    
    '''
    
    # define time for filename
    now = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    
    # open csvs we want to write to
    with open(file + now + '.csv', mode="w", encoding="utf-8") as fo:
        writer=csv.writer(fo, lineterminator='\n')
        with open('Releases/Deadpages' + now + '.csv', mode="w", encoding="utf-8") as dl:
            dead_writer=csv.writer(dl, lineterminator='\n')
        
            # throw an error if input lists do not match
            if (len(senders) == len(urls) == len(linkbases) == len(maxpages) == len(npages) == len(xpathLinks) == len(xpathTitles) == len(xpathDates) == len(regexDates) == len(strToDates)) == False:
                print('Length of input lists does not match')
                
            else:
                # loop over lists of input
                for it in range(len(senders)):
                    
                    sender = senders[it]
                    url = urls[it]
                    linkbase = linkbases[it]
                    maxpage = maxpages[it]
                    npage = npages[it]
                    xpathLink = xpathLinks[it]
                    xpathTitle = xpathTitles[it]
                    xpathDate = xpathDates[it]
                    regexDate = regexDates[it]
                    strToDate = strToDates[it]
                    
                    print('\n\nFetching links ' + sender + ' (' + str(it+1) + ' / ' + str(len(senders)) + ')' + '...')
                    i = 0
                    
                    # loop through collection of pages
                    for n in range(maxpage):
                        
                        # define url
                        fetchLink = url.format(n*npage)
                        
                        time.sleep(randint(1, 3))
                        
                        for attempt in range(3):
                            try:
                                # get page content
                                req = request.Request(fetchLink, headers = header)
                                tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                            
                            # exceptions for errors
                            except request.HTTPError:
                                if attempt < 2:
                                    print('\n\t\t' + fetchLink + '\n\t\tdid not work, retrying...')
                                    time.sleep(5)
                                else:
                                    print('\n\t\tCollection failed due to HTTPError:\n\t\t' + fetchLink)
                                    dead_writer.writerow(fetchLink)
                                    break
                            except request.URLError:
                                if attempt < 2:
                                    print('\n\t\t' + fetchLink + '\n\t\tdid not work, retrying...')
                                    time.sleep(5)
                                else:
                                    print('\n\t\tCollection failed due to URLError:\n\t\t' + fetchLink)
                                    dead_writer.writerow(fetchLink)
                                    break
                            except:
                                if attempt < 2:
                                    print('\n\t\t' + fetchLink + '\n\t\tdid not work, retrying...')
                                    time.sleep(5)
                                else:
                                    print('\n\t\tCollection failed due to unknown error:\n\t\t' + fetchLink)
                                    dead_writer.writerow(fetchLink)
                                    break
                        
                        
                        # identify relevant objects on the webpage
                        tempLinks   = tree.xpath(xpathLink)
                        tempDate    = tree.xpath(xpathDate)
                        tempTitle   = tree.xpath(xpathTitle)
                        
                        # bind link, sender, title, and date of a given release and write it into csv
                        for lk, dt, tt in zip(tempLinks, tempDate, tempTitle):
                            tmpdt = time.strptime(re.match(regexDate, dt).group(1), strToDate)
                            date = time.strftime("%d-%m-%Y", tmpdt)
                            link = linkbase + lk
                            tt = " ".join(" ".join(tt.split("\n")).split("\r")) # this prevents line breaks when writing into csv
                            output = [date, sender, tt, link]
                            writer.writerow(output)
                            dead_writer.writerow("0")
                            i += 1
                        
                        # update progress bar
                        bar = str('\t\t[' + '='*int((n + 1)/ (maxpage / 30)) + ' '*(30-int((n + 1) / (maxpage / 30))) + ']   ' + str((n + 1)) + '/' + str(maxpage))
                        stdout.write('%s\r' % bar)
                        stdout.flush()
                        
                    # message when collection of one url is finished
                    print(str('\nFinished collecting ' + str(i) + ' links for ' + sender))
        
                
            
            
        

#%% define input (all in one run here to make them end up in the same file)
                    
deadLinks = []
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

senders = ['CDU']*4
senders.append('SPD')

urls = ['https://www.presseportal.de/nr/7846/{}?startDate=2015-01-01&endDate=2019-05-08',
        'https://www.presseportal.de/nr/7846/{}?startDate=2010-01-01&endDate=2014-12-31',
        'https://www.presseportal.de/nr/7846/{}?startDate=2005-01-01&endDate=2009-12-31',
        'https://www.presseportal.de/nr/7846/{}?startDate=2000-01-01&endDate=2004-12-31',
        'https://www.spdfraktion.de/presse/pressemitteilungen?s=&s_date%5Bdate%5D=&e_date%5Bdate%5D=&wp=All&sort_by=created&sort_order=&items_per_page=100&page={}']

linkbases = ['https://www.presseportal.de']*4
linkbases.append('https://www.spdfraktion.de')

maxpages = [86, 162, 211, 294, 93]

npages = [27]*4
npages.append(1)

xpathLinks = ['/html/body/main/div/ul[*]/li[*]/article/h3/a/@href']*4
xpathLinks.append('//*[@id="block-system-main"]/div/div/div/div[1]/div/div/div/div/div[1]/div[*]/article/h3/a/@href')

xpathTitles = ['/html/body/main/div/ul[*]/li[*]/article/h3/a/span/text()']*4
xpathTitles.append('//*[@id="block-system-main"]/div/div/div/div[1]/div/div/div/div/div[1]/div[*]/article/h3/a/text()')

xpathDates = ['/html/body/main/div/ul[*]/li[*]/article/div[1]/h5/text()']*4
xpathDates.append('//*[@id="block-system-main"]/div/div/div/div[1]/div/div/div/div/div[1]/div[*]/article/span/text()')

regexDates = ['(.*)']*4
regexDates.append('([0-9]*.[0-9]*.[0-9]*)')  

strToDates = ['%d.%m.%Y – %H:%M']*4
strToDates.append('%d.%m.%Y')


#%% run scraper
basedir = os.path.expanduser('~/Dropbox/Studies/Semester 2/Block I/data_IMEM/')
linkScraper(file = basedir+'intermediate/Links'
            senders = senders, 
            urls = urls, 
            linkbases = linkbases, 
            maxpages = maxpages, 
            npages = npages, 
            xpathLinks = xpathLinks,
            xpathTitles = xpathTitles, 
            xpathDates = xpathDates, 
            regexDates = regexDates, 
            strToDates = strToDates)

