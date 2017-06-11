#!/bin/bash

getConfNameFromURL (){

	revUrl=$(echo $1 | rev)
	IFS='/' read -ra ADDR <<< "$revUrl"
	z=${ADDR[0]}
	IFS='\.' read -ra ADDR <<< "$z"
	z=${ADDR[1]}
	t=$(echo $z | rev)
	confName=$t
}

while read line
do
	confName="unknown"
	getConfNameFromURL $line
	
	rm -rf conferences.dat
	rm -rf paper.dat
	rm -rf paper_self.dat
	rm -rf paper_patent.dat
 
	printf "crawling %s\n" $line
	echo $line > confurl
	curl -s $line > confpage
        confStartTime=`date +%s`
	./launchCrawler.sh $confStartTime
	
	printf "finished crawling %s\n" $line
	mv conferences.dat $confName

done < "conflist" 
