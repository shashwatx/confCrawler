## Introduction

_confCrawler_ is a tool to gather publication metrics about conference/journal publications.  
Congruence of [dblp](http://dblp.uni-trier.de/) and [Google Scholar](http://scholar.google.com) is exploited to generate the following metrics for each research paper.
  1. `citations`: number of citations
  2. `self-citations`: number of self citations
  3. `patent-citations`: number of patent citations
  4. `recent-citations`: number of citations since 2010
  5. `list-of-authors`: list of authors

It can be used to crawl any venue that
* is listed on dblp 
* is indexed by Google Scholar.


### History

This was written to quickly identify the 5 _best_ papers amongst the papers published in 2005 in a major databases conference.
In the autumn of 2015, I was asked to assist in the process of selecting the best publication of a certain databases conference.
Thus, _confCrawler_ was born.

## Motivation

Go [here](https://github.com/shashwatx/confCrawler/blob/master/motivation/MOTIVATION.md) for more research oriented motivation.


## Requirements

The following components are required to launch the crawler.
 * Python
 * BeautifulSoup
 * tor
 * Internet


## Usage

TODO: Write usage instructions

## License

Code shall be released under [the MIT license](https://github.com/shashwatx/confCrawler/blob/master/LICENSE)

## Updates

**Update: March 1, 2016**: From Feb-1-2016 to Feb-28-2016 I crawled the following conferences.
```
  AAAI (1990-2015), ICML (1990-2015), IJCAI (1991-2015), KDD (1995-2015), NIPS (1990-2014)
  ACL (1990-2015), ICCV (1990-2013), WWW (2001-2015)
  ASPLOS (1991-2015), CCS (1993-2015), DAC (1990-2015), HPCA (1995-2015)
  STOC (1990-2015), SIAM (19-44), FOCS (1990-2015), LICS (1990-2015)
```

**Update: Jan 26, 2016**: Finished with top 4 DB venues. Now crawling following major conferences.
```
  1. AAAI, ICML, IJCAI, KDD, NIPS
  2. ACL, ICCV, WWW
  3. ASPLOS, CCS, DAC, HPCA
  4. STOC, SIAM, FOCS, LICS, SCG
```

**Update: Dec 4, 2015**: Finished crawling `SIGMOD1990-2014`. Now crawling `VLDB1990-2007`. Must generate a list of conferences to target.

**Update: Nov 16, 2015**: Finished writing the first stable and (hopefully) bug-free version of confCrawler. Rerouting page requests through tor has greater latency than expected. The code is being tested on a select few conferences. More details to follow.

## TODO

  1. Setup and launch a heroku app for the data we have crawled.
  2. Identify and fix "N/A" entries.
      1. Develop crawler to crawl **only** the "N/A" entries.
      2. Inform DBLP team about the spotted errors.

