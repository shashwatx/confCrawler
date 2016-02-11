## Bash One Liners
__Input: Conference File(s)__

1. Get _meaningful_ papers.
```
cat vldb* | grep -v "^[0-9]\+$" | grep -v "n/a$" | cut -d'|' -f2,3,4,5,6,7 > dump
```
2. Find fraction of self citations.
```
awk 'BEGIN{FS="|"}{if($3!=0){words[$1]=$6/$3;}}END{for(w in words)printf("%f %s\n",words[w],w)}' < dump > dump.fracSelfCites
```
3. Find missing papers.
```
awk 'BEGIN{FS="|"}{if(NF==4){printf("%s|%s|%s|%s\n",FILENAME,$2,$3,$4);}}END{}' vldb* > dump.missingPapers.0
cat dump.missingPapers.0 | grep -E -v "International Conference|Front Matter|Letter from the|Cover Page|Sponsors|Copyright Notice" > dump.missingPapers
rm -rf dump.missingPapers.0
```
4. Generate R data file.
```
awk 'BEGIN{FS="|"}{if(NF>4){printf("%s|%s|%s|%d|%d|%d|%d\n",FILENAME,$2,$3,$4,$5,$6,$7);}}END{}' vldb* > data.vldb.0
echo "conference|title|authors|citations|recent|patent|self" > data.vldb
cat data.vldb.0 | grep -E -v "International Conference|Front Matter|Letter from the|Cover Page|Sponsors|Copyright Notice" >> data.vldb
rm -rf data.vldb.0
```

## Errors

* VLDB2012: Following 9 lines contain "the" doubly. 
  * Volume 5, No. 2 through 10
* VLDB2013: Typo in title
  * ggregating Semantic Annotators (Chen et al.)
* VLDB1991: Typo in title
  * Conecptual Modeling Using and Extended E-R Model (Abstract) Elmasri et al.
