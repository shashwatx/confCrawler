**TODO** 
  1. Setup and launch a heroku app for the data we have crawled.
  2. Identify and fix "N/A" entries.
    1. Develop crawler to crawl **only** the "N/A" entries.
    2. Inform DBLP team about the spotted errors.

**Update: March 1, 2016**: From Feb-1-2016 to Feb-28-2016 I crawled the following conferences.
  1. AI: AAAI (1990-2015), ICML (1990-2015), IJCAI (1991-2015), KDD (1995-2015), NIPS (1990-2014)
  2. ACL (1990-2015), ICCV (1990-2013), WWW (2001-2015)
  3. ASPLOS (1991-2015), CCS (1993-2015), DAC (1990-2015), HPCA (1995-2015)
  4. FOCS (1990-2015), LICS (1990-2015), SIAM (19-44), STOC (1990-2015)

**Update: Jan 26, 2016**: _After crawling top 4 conferences in databases, I have moved on to crawling major conferences in the following domains._
  1. AI: AAAI, IJCAI, ICML, NIPS, KDD
  2. WWW, ICCV, ACL
  3. HPCA, CCS, ASPLOS, DAC
  4. STOC, SIAM, FOCS, LICS, SCG

**Update: Dec 4, 2015**: _Finished crawling SIGMOD1990-2014. Now crawling VLDB1990-2007. Must generate a list of conferences to target._

**Update: Nov 16, 2015**: _I have finished writing the first stable and (hopefully) bug-free version of confCrawler. Rerouting page requests through tor has greater latency than expected. The code is being tested on a select few conferences. More details to follow._

## Motivation

Go [here](https://github.com/shashwatx/confCrawler/blob/master/MOTIVATION.md) for motivation.

## Introduction

confCrawler is a tool to generate raw stats about conference/journal publications. Congruence of [dblp](http://dblp.uni-trier.de/) and [Google Scholar](http://scholar.google.com) is exploited to generate the following figures for each paper.
  1. #citations
  2. #self-citations
  3. #patent-citations
  4. #recent-citations
  5. list-of-authors

It can be used to crawl any venue that
* is listed on dblp 
* is indexed by Google Scholar.

While the reported stats are basic, it remains to be seen to if there are any hidden patterns in the data.

## Requirements

The following components are required to launch the crawler.
 * Python
 * BeautifulSoup
 * tor
 * Internet

## History

In the autumn of 2015, the author of confCrawler was asked to assist
in the process of selecting the best publication of a certain databases conference.

Thus, confCrawler was born.

## Usage

TODO: Write usage instructions

## License

Code shall be released under [the MIT license](https://github.com/shashwatx/confCrawler/blob/master/LICENSE)
