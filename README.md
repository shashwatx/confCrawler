# Introduction

confCrawler is a tool to crawl conferences. 
It can be used to crawl any conference that is  
* Listed on dblp 
* Indexed by Google Scholar.

Given the dblp url of a conference, confCrawler
attempts to report, for each publication, the following fields.

 1. #citations
 2. #self-citations
 3. #patent-citations
 4. #recent-citations
 5. list-of-authors

confCrawler is not a full fledged crawler and reports
only the (very) basic statistics for each publication of
the said conference.

## Requirements

confCrawler requires the following components.
 * Python
 * BeautifulSoup
 * tor
 * Patience

## History

In the autumn of 2015, the author of confCrawler was asked to assist
in the process of selecting the best publication of a certain databases conference.

Thus, confCrawler was born.

## Usage

TODO: Write usage instructions

## License

Code shall be released under [the MIT license](https://github.com/shashwatx/confCrawler/blob/master/LICENSE)
