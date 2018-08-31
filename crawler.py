#!/usr/bin/env python
from __future__ import unicode_literals
from pattern.web import URL
import coloredlogs
coloredlogs.install()
#from termcolor import colored

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

import logging
#FORMAT = '%(asctime)-15s %(message)s'
#logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger("main")

# BEGIN: --try-to-fool-Google--
import socket
import socks
import random
import requests
import pygeoip
#from selenium import webdriver
from fake_useragent import UserAgent
import time

lines = open('proxies').read().splitlines()
myline =random.choice(lines)
proxyHostname=myline.split()[0]
proxyPort=int(myline.split()[1])
print "random proxy hostname: "+proxyHostname
print "random proxy port: "+str(proxyPort)

try:
    #SOCKS5_PROXY_HOST = proxyHostname
    #SOCKS5_PROXY_PORT = proxyPort
    SOCKS5_PROXY_HOST = 'localhost'
    SOCKS5_PROXY_PORT = 9020
    #default_socket = socket.socket
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
    socket.socket = socks.socksocket
    #socket.socket=default_socket
except socks.GeneralProxyError:
    logger.error('Proxy failure.')
    sys.exit(1)
# END: --try-to-fool-Google--

import difflib
import math
import hashlib
import urllib
import urllib2
import time
import os
import re
import os.path
import codecs
from geoip import open_database

from bs4 import BeautifulSoup

#url = 'http://dblp.uni-trier.de/db/conf/kdd/kdd99.html'
#url = 'http://dblp.uni-trier.de/db/conf/edbt/edbt88.html'
#url = 'http://dblp.uni-trier.de/db/conf/sigmod/sigmod2013.html'
#url = 'http://dblp.uni-trier.de/db/journals/cacm/cacm53.html'
#url = 'http://dblp.uni-trier.de/db/conf/sigmod/sigmod2002.html'

def getConfURL(path):
    with open(path) as f:
        content = f.readlines()
    #print content
    return content[0].strip('\n')

#print url
#sys.exit(1)
#url='http://dblp.uni-trier.de/db/conf/vldb/vldb2005.html'

citesPerPage=15
startYear=2012
endYear=2017
timeoutSec=30


class SinisterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getMyIP():
    r = requests.get(r'http://jsonip.com')
    ip= r.json()['ip']
    logger.info('We are in %s', ip)
    with open_database('/home/shashwat/resources/GeoLite2-Country.mmdb') as db:
        match = db.lookup(ip)
        logger.info('%s',match)
    #browser=webdriver.Firefox()
    #browser.get('http://icanhazip.com')


def getRandomHeader():
    google_id = hashlib.md5(str(random.random())).hexdigest()[:16]
    ua = UserAgent()
    timestamp=int(time.time())
    
    randomHeader = { 'user-Agent': ua.random, 'cookie': 'GSP=LM=%d:S=%s' % (timestamp, google_id), 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.8', 'accept-encoding': 'gzip, deflate, sdch, br'}
    #randomHeader = { 'user-Agent': ua.random, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.8', 'accept-encoding': 'gzip, deflate, sdch, br', 'cookie': 'GSP=LM=%d:S=%s'% (timestamp, google_id)}
    #randomHeader = { 'user-Agent': ua.random, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'accept-encoding': 'gzip, deflate, sdch, br'}
    
    #logger.info('Random Header: %s',randomHeader)
    return randomHeader

def getSimilarityScore(seq1, seq2):
    return difflib.SequenceMatcher(
        a=seq1.strip().lower(),
        b=seq2.strip().lower()).ratio()


def parseRecentCitesString(citeString):

    numRC = 0

    isAboutPresent = "About" in citeString
    isResultPresent = "result" in citeString

    if isResultPresent:
        if isAboutPresent:
            m = re.search('About (.+) results (.+)', citeString)
            numRC = int(m.group(1).replace(',',''))
        else:
            m = re.search('(.+) result(.+)', citeString)
            numRC = int(m.group(1).replace(',',''))
    else:
        numRC = 0

    return numRC


def getSoup_CitationPageWithOffset(offset, fetched_citation_url):
    mybaseurl = "http://scholar.google.fr"
    citations_base_url = mybaseurl + fetched_citation_url + "&num=" + str(citesPerPage) + "&start=" + str(offset)
    logger.info('\t\turl-offset: %s',citations_base_url)

    request = urllib2.Request(citations_base_url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\t\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def getSoup_GS(title):
   
    title=title.decode('utf8','ignore').encode('ascii','ignore')

    titleEnhanced = urllib2.quote(title)
    gs_base_url = "https://scholar.google.com/scholar?hl=en&as_q="+titleEnhanced
    logger.info('\tfetching paper: %s',gs_base_url)

    request = urllib2.Request(gs_base_url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\tcode:%s',response.getcode())

    gs_page = response.read()
    gs_soup = BeautifulSoup(gs_page,"lxml")

    return gs_soup

def getSoup_GS_Home():
   
    gs_base_url = "http://scholar.google.com"
    logger.warn('\tfetching scholar home page: %s',gs_base_url)

    request = urllib2.Request(gs_base_url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\tcode:%s',response.getcode())

    gs_page = response.read()
    gs_soup = BeautifulSoup(gs_page,"lxml")

    return gs_soup

def getSoup_RecentCitationPage(fetched_citation_url):
    mybaseurl = "http://scholar.google.com"
    citations_base_url = mybaseurl + fetched_citation_url + "&as_ylo="+str(startYear)+"&as_yhi="+str(endYear)
    logger.info('\turl-recent: %s',citations_base_url)

    request = urllib2.Request(citations_base_url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def getSoup_PatentCitationPage(fetched_citation_url):

    mybaseurl = "http://scholar.google.es"
    uniqueId=getUniquePaperId(fetched_citation_url)
    #url = mybaseurl + fetched_citation_url + "&num=" + str(citesPerPage) + "&q=" + "US+Patent" + "&scipsc=1" + "&start=" + str(offset)
    url = mybaseurl + "/scholar?" + "q=" + "US+Patent" + "&btnG=" + "&hl=en" + "&as_sdt=2005" + "&sciodt=0%2C5" + "&cites=" + uniqueId + "&scipsc=1" + "&num=15"
    logger.info('\t\tpatent-citation-url :%s',url)
    
    request = urllib2.Request(url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\t\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def getSoup_PatentCitationPageWithOffset(offset, fetched_citation_url):
    
    mybaseurl = "http://scholar.google.es"
    uniqueId=getUniquePaperId(fetched_citation_url)
    #url = mybaseurl + fetched_citation_url + "&num=" + str(citesPerPage) + "&q=" + "US+Patent" + "&scipsc=1" + "&start=" + str(offset)
    url = mybaseurl + "/scholar?" + "q=" + "US+Patent" + "&btnG=" + "&hl=en" + "&as_sdt=2005" + "&sciodt=0%2C5" + "&cites=" + uniqueId + "&scipsc=1" + "&num=15" + "&start=" + str(offset)
    
    logger.info('\tpatent citation url: %s',url)


    request = urllib2.Request(url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\t\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def getSoup_SelfCitationPage(fetched_citation_url, paperAuthors):
    mybaseurl = "http://scholar.google.es"
    uniqueId=getUniquePaperId(fetched_citation_url)
    #url = mybaseurl + fetched_citation_url + "&num=" + str(citesPerPage) + "&q=" + composeAuthorString(paperAuthors) + "&scipsc=1" + "&btnG=" + "&as_sdt=2005" + "&sciodt=0,5"
    url = mybaseurl + "/scholar?" + "q=" + composeNewAuthorString(paperAuthors) + "&btnG=" + "&hl=en" + "&as_sdt=2005" + "&sciodt=0%2C5" + "&cites=" + uniqueId + "&scipsc=1" + "&num=15"
    
    logger.info('\tself citation url: %s',url)

    request = urllib2.Request(url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\t\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def composeAuthorString(ats):
    authorList = getAuthorsFromString(ats)
    aString=''
    pre=''
    for i in range(0, len(authorList)):
	aString=aString+pre+'"'+authorList[i].decode('utf8','ignore').encode('ascii','ignore')+'"'
	pre=' OR '
    #title=title.decode('utf8','ignore').encode('ascii','ignore')
    aStringEnhanced = urllib2.quote(aString)
    return aStringEnhanced

def composeNewAuthorString(ats):
    authorList = getAuthorsFromString(ats)
    aString=''
    pre=''
    for i in range(0, len(authorList)):
	aString=aString+pre+'"'+authorList[i].decode('utf8','ignore').encode('ascii','ignore').replace(" ","+")+'"'
	pre='+OR+'
    #title=title.decode('utf8','ignore').encode('ascii','ignore')
    #aStringEnhanced = urllib2.quote(aString)
    logger.info("author string: %s",aString)
    return aString

def getSoup_SelfCitationPageWithOffset(offset, fetched_citation_url, paperAuthors):

    mybaseurl = "http://scholar.google.es"
    uniqueId=getUniquePaperId(fetched_citation_url)
    #url = mybaseurl + fetched_citation_url + "&num=" + str(citesPerPage) + "&q=" + composeAuthorString(paperAuthors) + "&scipsc=1" + "&start=" + str(offset)
    url = mybaseurl + "/scholar?" + "q=" + composeNewAuthorString(paperAuthors) + "&btnG=" + "&hl=en" + "&as_sdt=2005" + "&sciodt=0%2C5" + "&cites=" + uniqueId + "&scipsc=1" + "&start=" + str(offset) + "&num=15"
    
    logger.info('\tself citation offset url: %s',url)

    request = urllib2.Request(url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)
    logger.info('\t\tcode:%s',response.getcode())

    cs_page = response.read()
    cs_soup = BeautifulSoup(cs_page,"lxml")
    return cs_soup

def getAuthorsFromString(authorString):
    shortAuthorString = authorString.split(' - ')[0]
    list1=shortAuthorString.split(',')
    strip_list = [item.strip().rstrip('.') for item in list1]
    return strip_list

# /scholar?cites=3318215302492877669&as_sdt=5,41&sciodt=0,41&hl=en
def getUniquePaperId(halfUrl):
    first = halfUrl.split('=')[1]
    second = first.split('&')[0]
    return second

def doAuthorListsMatch(list1, list2):
    for i in range(0, len(list1)):
        for j in range(0, len(list2)):
            if getSimilarityScore(list1[i], list2[j]) > 0.95:
                return True
    return False

def isBogusTitle(title, i):
    flag=False
    title=title.strip()
    bogusList=["Front Matter", "Letter from the"]
    for i in range(0, len(bogusList)):
	if title.startswith(bogusList[i]):
	    flag = True
    if "Proceedings of" in title:
        flag = True
    if "International Conference" in title:
        flag = True
    return flag

def isPatentCitation(currentAuthors):
    presentPatent = "US Patent" in currentAuthors
    if presentPatent:
        return True
    else:
        return False

def getStartIndexFromContext(path):
    with open(path) as f:
        content = f.readlines()
    return len(content)-1

def isSelfCitation(originalAuthors, currentAuthors):
    authorList1 = getAuthorsFromString(originalAuthors)
    #logger.info(authorList1)
    authorList2 = getAuthorsFromString(currentAuthors)
    #logger.info(authorList2)
    return doAuthorListsMatch(authorList1, authorList2)

def getNumPagesToRead(numCites):
    numPagesToRead = numCites / citesPerPage
    carryOver = numCites % citesPerPage
    numPagesToRead = math.floor(numPagesToRead)
    numPagesToRead = int(numPagesToRead)
    if carryOver > 0:
        numPagesToRead = numPagesToRead + 1

    return numPagesToRead

def getCiteIndexFromPaperContext(path, i):
    
    if os.path.exists(path)!=True:
        logger.info('no paper context found. start over from 0')
        return 0
    
    logger.info('\tpaper context found.')

    with open(path) as f:
        content = f.readlines()
    if int(content[0]) == i:
        logger.info('\tmy context.')
        return int(content[1])+1
    else:
        logger.info('\tnot my context.')
        return 0

def getMainSoupFromContext(path, i):
    
    if os.path.exists(path)!=True:
        logger.info('no main context found.')
        return None
    
    logger.info('\tmain context found.')

    with open(path) as f:
        content = f.readlines()
    if int(content[0]) == i:
        logger.info('\tmy context.')
        return int(content[1])+1
    else:
        logger.info('\tnot my context.')
        return 0

def getSelfIndexFromPaperContext(path, i):
    
    if os.path.exists(path)!=True:
        logger.info('no self context found. start over from 0')
        return 0
    
    logger.info('\tself context found.')

    with open(path) as f:
        content = f.readlines()
    if int(content[0]) == i:
        logger.info('\tmy context.')
        return int(content[1])+1
    else:
        logger.info('\tnot my context.')
        return 0

def getPatentIndexFromPaperContext(path, i):
    
    if os.path.exists(path)!=True:
        logger.info('no patent context found. start over from 0')
        return 0
    
    logger.info('\tpatent context found.')

    with open(path) as f:
        content = f.readlines()
    if int(content[0]) == i:
        logger.info('\tmy context.')
        return int(content[1])+1
    else:
        logger.info('\tnot my context.')
        return 0

def getSelfCounterFromPaperContext(path,i):
    
    if os.path.exists(path)!=True:
        return 0

    with open(path) as f:
        content = f.readlines()
    
    if int(content[0]) == i:
        return int(content[2])
    else:
        return 0

def getPatentCounterFromPaperContext(path,i):
    
    if os.path.exists(path)!=True:
        return 0
    
    with open(path) as f:
        content = f.readlines()
    
    if int(content[0]) == i:
        return int(content[2])
    else:
        return 0

def writeCitePageSoupToFile(sp, index):
    soupPage=codecs.open(str(index)+".html",'w',encoding='utf8')
    soupPage.write(sp.prettify("utf-8"))
    soupPage.write('\n')
    soupPage.close()

def noteGoogleFuckUp(fuckup_file_path, infoString):
    fuckup_file=codecs.open(fuckup_file_path,'a',encoding='utf8')
    fuckup_file.write(infoString)
    fuckup_file.write('\n')
    fuckup_file.close()

def writePaperResult(context_path, i, cpg, counter):
    paper_context=codecs.open(context_path,'w',encoding='utf8')
    paper_context.write(str(i))
    paper_context.write('\n')
    paper_context.write(str(cpg))
    paper_context.write('\n')
    paper_context.write(str(counter))
    paper_context.write('\n')
    paper_context.close()

def writeResult(context_path, thisResult):
    context=codecs.open(context_path,'a',encoding='utf8')
    context.write(thisResult)
    context.write('\n')
    context.close()

#getMyIP()

url = getConfURL('confurl')
logger.info("DBLP url: %s",url)

# check if context exists
context_path="conferences.dat"
conf_page_file_path="confpage"
paper_context_path_self="paper_self.dat"
paper_context_path_patent="paper_patent.dat"


# load soup from conf_page_file_path 
conf_page_file = open(conf_page_file_path,'r')
soup = BeautifulSoup(conf_page_file.read(),"lxml")
conf_page_file.close()

logger.info('Read page at: %s', conf_page_file_path)

data = soup.find_all("div", {"class": "data"})
length = len(data)

if os.path.exists(context_path)!=True:
    context=codecs.open(context_path,'w',encoding='utf8')
    context.write(str(length))
    context.write('\n')
    context.close()
    logger.info("conference file created")
else:
    logger.info("conference file retained")

#logger.info("dblp url parsed")

     
startIndex=getStartIndexFromContext(context_path)

logger.debug("start index %d",startIndex)
logger.warn("total papers in conference:  %d",length)

for i in range(startIndex, length):
    
    papersLeft=length-i-1
    logger.warn("remaining papers:  %d",papersLeft)
    thisResult=""

    # get paper title
    title = ''.join(data[i].find("span", {"class": "title"}).text)

    logger.warn("title: %s",title)
    
    # get authors
    # authors = data[i].find_all("a")
    authors = data[i].find_all("span", {"itemprop": "author"})
    lengthA = len(authors)
    
    logger.info("\t#authors: %d",lengthA)

    if lengthA > 0:
        thisResult=thisResult+str(i+1)+"|"+title+"|"
        for j in range(0, lengthA - 1):
            author = ''.join(authors[j].find("a").findAll(text=True))
            author = author
            thisResult=thisResult+author+","
        author = ''.join(authors[lengthA - 1].find("a").findAll(text=True))
        thisResult=thisResult+author+"|"
    else:
        thisResult=thisResult+str(i+1)+"|"+title+"|"+"n/a"
        writeResult(context_path,thisResult)
        continue
    

    # skip conference proceedings.
    # Example Titles: Front Matter, 
    if isBogusTitle(title, i): 
        thisResult=thisResult+"n/a"
        writeResult(context_path,thisResult)
        logger.warn('Bogus title: %s',title)
	continue
    #get abstract url
    #navElement = data[i].previous_sibling
    #acmD = navElement.ul.li.div.a
    #strVal = str(acmD.get('href'))

    # print strVal

    # formatType=strVal.find("dx.doi")
    # base_springer_url=strVal
    # springer_page=urllib2.urlopen(base_springer_url).read()
    # springer_soup=BeautifulSoup(springer_page)
    # sec_abstract=springer_soup.find("section",{"class":"Abstract"})
    # abstract=''.join(sec_abstract.p.findAll(text=True))
    # abstract=abstract.encode("utf-8")

    # print abstract

    try:
        title=title.replace('(Extended Abstract)','')        
        title=title.replace('(extended abstract)','')        
        
        #gs_tt = getSoup_GS_Home()
        #tt_path="_tt"
        #tt_file=open(tt_path,"w")
        
        #logger.warn('Writing _tt')
        #tt_file.write(str(gs_tt))
        #tt_file.close()
        #time.sleep(0.5)
         
        gs_soup = getSoup_GS(title)
      
        # check to see if google returned a "No Results" page
        gs_sanity = gs_soup.find("p", {"class": "gs_med"})
        if gs_sanity is not None:
            gs_entry = gs_soup.find("div", {"class": "gs_ri"})
            if gs_entry is None:
                thisResult=thisResult+"n/a"
                writeResult(context_path,thisResult)
                logger.info('fetched no results page. this may be a no results page')
                continue
        
        # receive first hit
        gs_entry = gs_soup.find("div", {"class": "gs_ri"})
        
        # check if turing test, bypass if yes.
        if gs_entry is None:
            raise SinisterError('gs_entry: Google wants turing test')
       
        # get title
        gs_rt = gs_entry.find_all("h3", {"class": "gs_rt"})[0]

        
        # if first hit is neither a normal link nor a citation, skip to next. 
        # Check first for normal, then for citation
        if gs_rt.a is not None:
            extractedTitle = ''.join(gs_rt.a.find_all(text=True))
        elif gs_rt.span is not None:
            extractedTitle = ''.join(gs_rt.span.find_all(text=True))
        else:
            thisResult=thisResult+"n/a"
            writeResult(context_path,thisResult)
            continue

        #extractedTitle = ''.join(gs_rt.a.find_all(text=True))
        logger.warn('GS Title: %s',extractedTitle)

        # get google citation count
        gs_fl = gs_entry.find_all("div", {"class": "gs_fl"})[0]
        citationCount = ''.join(gs_fl.a.findAll(text=True))

        similarityScore = getSimilarityScore(extractedTitle, title)
        isSubstring = "Cited by" in citationCount

        if similarityScore > 0.8:

            logger.info('\thit')

            if isSubstring:

                logger.info('\thas citations')
                
                # get authors
                gs_a = gs_entry.find_all("div", {"class": "gs_a"})[0]
                gs_authors = ''.join(gs_a.text)
                extractedAuthors = gs_authors
                # extracted Authors split on " - "
                logger.warn('extractedAuthors : %s',extractedAuthors)
                
                # get total citations
                m = re.search('Cited by (.+)', citationCount)
                numCites = m.group(1)
                numCites = int(numCites)
                thisResult=thisResult+str(numCites)+"|"

                # get total number of cite pages
		numPagesToRead = getNumPagesToRead(numCites)

                # get base citations page url
		citations_base_url = gs_fl.a.get('href')
		logger.info('\tcitations-base-url %s',citations_base_url)
		logger.info('\tWill not extract recent citations')

		# get recent citations
		#recent_bib_soup = getSoup_RecentCitationPage(citations_base_url)
                #numRecentCitesMeta = recent_bib_soup.find_all("div", {"id": "gs_ab_md"})
		#if not numRecentCitesMeta:
                #    raise SinisterError('Could not find recent cites')
		#numRecentCites=numRecentCitesMeta[0].text
                #numRecentCites = parseRecentCitesString(numRecentCites)
                numRecentCites=0
                thisResult=thisResult+str(numRecentCites)+"|"

		
		# -----------------------------------------------------------------------
		# BEGIN: self citations
		# -----------------------------------------------------------------------
		self_page_soup = getSoup_SelfCitationPage(citations_base_url,extractedAuthors)
                
		numPossibleSelfCitesMeta = self_page_soup.find_all("div", {"id": "gs_ab_md"})
		if not numPossibleSelfCitesMeta:
                    raise SinisterError('Could not find self cites')
		numPossibleSelfCites=numPossibleSelfCitesMeta[0].text
                numPossibleSelfCites = parseRecentCitesString(numPossibleSelfCites)
		numSelfPagesToRead = getNumPagesToRead(numPossibleSelfCites)
                
		selfPageIndex = getSelfIndexFromPaperContext(paper_context_path_self, i)
                selfCounter = getSelfCounterFromPaperContext(paper_context_path_self, i)
                

                logger.info("\tself pages to read %d",numSelfPagesToRead)
                
                for cpg in range(selfPageIndex, numSelfPagesToRead):

                    logger.info('\tself page %d / %d',(cpg+1),numSelfPagesToRead)
                    paperResult=""

                    #wt=random.uniform(1,3)
                    #time.sleep(0.5);

                    self_current_page = getSoup_SelfCitationPageWithOffset(citesPerPage*(cpg), citations_base_url,extractedAuthors)
                    self_divs = self_current_page.find_all("div", {"class": "gs_ri"})
 
                    if not self_divs:
			if citesPerPage*cpg<1000:
			    logger.error('FUCK ! Google found us.')
			    raise SinisterError('Google found us while looking for self citations')
			else:
			    logger.error('FUCK ! This paper has too many self citations.')
			    writePaperResult(paper_context_path_self, i, numSelfPagesToRead, selfCounter)
			    break
				

                    for self_div in range(0, len(self_divs)):
                        self_author_list = self_divs[self_div].find_all("div", {"class": "gs_a"})
                        if not self_author_list:
                            continue
                        self_author=self_author_list[0]

                        selfAuthors = ''.join(self_author.text)
                        if isSelfCitation(extractedAuthors,selfAuthors):
                            selfCounter = selfCounter + 1
                    
                    writePaperResult(paper_context_path_self, i, cpg, selfCounter)
		# -----------------------------------------------------------------------
		# END: self citations
		# -----------------------------------------------------------------------


		# -----------------------------------------------------------------------
		# BEGIN: patent citations
		# -----------------------------------------------------------------------
		patent_page_soup = getSoup_PatentCitationPage(citations_base_url)
                
		numPossiblePatentCitesMeta = patent_page_soup.find_all("div", {"id": "gs_ab_md"})
		if not numPossiblePatentCitesMeta:
                    raise SinisterError('Could not find patent cites')
		numPossiblePatentCites=numPossiblePatentCitesMeta[0].text
                numPossiblePatentCites = parseRecentCitesString(numPossiblePatentCites)
		numPatentPagesToRead = getNumPagesToRead(numPossiblePatentCites)
                
		patentPageIndex = getPatentIndexFromPaperContext(paper_context_path_patent, i)
		patentCounter = getPatentCounterFromPaperContext(paper_context_path_patent, i)

                logger.info("\tpatent pages to read %d",numPatentPagesToRead)
                
                for cpg in range(patentPageIndex, numPatentPagesToRead):

                    logger.info('\tpatent page %d / %d',(cpg+1),numPatentPagesToRead)
                    paperResult=""

                    #wt=random.uniform(1,3)
                    #time.sleep(0.5);

                    patent_current_page = getSoup_PatentCitationPageWithOffset(citesPerPage*(cpg), citations_base_url)
                    patent_divs = patent_current_page.find_all("div", {"class": "gs_ri"})
 
                    if not patent_divs:
			if citesPerPage*cpg<1000:
			    logger.error('FUCK ! Google found us.')
		            raise SinisterError('Google found us while looking for patents')
			else:
			    logger.error('FUCK ! This paper has too many patent citations.')
			    writePaperResult(paper_context_path_patent, i, numPatentPagesToRead, patentCounter)
			    break

                    for patent_div in range(0, len(patent_divs)):
                        patent_author_list = patent_divs[patent_div].find_all("div", {"class": "gs_a"})
                        if not patent_author_list:
                            continue
                        patent_author=patent_author_list[0]

                        patentAuthors = ''.join(patent_author.text)
                        if isPatentCitation(patentAuthors):
                            patentCounter = patentCounter + 1
                    
                    writePaperResult(paper_context_path_patent, i, cpg, patentCounter)
		# -----------------------------------------------------------------------
		# END: patent citations
		# -----------------------------------------------------------------------


                thisResult=thisResult+str(patentCounter)+"|"
                thisResult=thisResult+str(selfCounter)

            else: # case: paper has no citations
                thisResult=thisResult+"0|0|0|0"  # citations|recentCitations|selfCitations|patentCitations

        else:   # case: google scholar did not index the paper
            thisResult=thisResult+"n/a"

        # update context
        writeResult(context_path,thisResult)

        #time.sleep(2);
        
    except urllib2.HTTPError,e:
        logger.error('HTTP failure. Code: %d',e.code)
        sys.exit(1)
    
    except urllib2.URLError:
        logger.error('URL failure.')
        sys.exit(1)

    except SinisterError,e:
        logger.error('Sinister failure: %s',str(e))
        sys.exit(1)

    except AttributeError:
        logger.error('Attribute failure.')
        sys.exit(1)
    
    except socks.ProxyConnectionError:
        logger.error('tor proxy failure.')
        sys.exit(1)
    
    except socks.GeneralProxyError:
        logger.error('tor proxy failure (type 2).')
        sys.exit(1)
    
success_path="_SUCCESS"
success=open(success_path,"w")
success.write('and we are done...\n')
success.close()

# time.sleep(2);
