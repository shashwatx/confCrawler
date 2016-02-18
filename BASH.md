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

## Errors DBLP
* VLDB 91
  * The correct name for "Safe Referential Structures in Relational Databases." is "Safe Referential Integrity Structures in Relational Databases."
  * Typo in Paper "Conecptual Modeling Using and Extended E-R Model" Elmasri et al.
* VLDB95:
  * Paper "Duplicate Removal in Information Dissemination" is indexed as "Duplicate Removal in Information System Dissemination"
  * Paper "Avoiding Retrieval Contention for Composite Multimedia Objects" is indexed as "Retrieval of Composite Multimedia Objects".
* VLDB97:
  * Paper "Parallel Algorithms for High-dimensional Similarity Joins" is indexed as "Parallel Algorithms for High-dimensional Similarity Joins for Data Mining Applications"
* VLDB2004:
  * Paper "Automated design of multidimensional clustering tables for relational databases" is indexed as "Automating the design of multi-dimensional clustering tables in relational databases".
  * Paper "Managing RFID Data" is indexed as "Managing RDFI Data".
* VLDB2011: 
  * Paper "Analytics for the real-time web" is indexed as "Analytics for the realtime web".
* VLDB2012: Following 9 lines contain "the" doubly. 
  * Volume 5, No. 2 through 10
* VLDB2013: Typo in title
  * ggregating Semantic Annotators (Chen et al.)
* VLDB1991: Typo in title
* VLDB2000:
  * Paper "Novel Approaches in Query Processing for Moving Object Trajectories" is actually titled "Novel Approaches to the Indexing of Moving Object Trajectories"
* SIGMOD96:
  * The correct title for __An Open Storage System for Abstract Objects__ is __An open abstract-object storage system__.

## Errors Google Scholar
* VLDB90:
  * Paper "Query Processing for Multi-Attribute Clustered Records" is indexed as "Query processing method for multi-attribute clustered relations".
* VLDB95:
  * Paper "Duplicate Removal in Information Dissemination" is indexed as "Duplicate Detection in Information Dissemination"
* VLDB96:
  * Paper "Constructing Efficient Decision Trees by Using Optimized Numeric Association Rules" is indexed as "Constructing E cient Decision Trees by Using Optimized Numeric Association Rules"
* VLDB97:
  * Paper "Using Versions in Update Transactions: Application to Integrity Checking." is indexed as "Using Versions in Update Transactions"
* VLDB99:
  * Paper "On Efficiently Implementing SchemaSQL on an SQL Database System" by Lakshmanan et al. is indexed with the title "On E ciently Implementing SchemaSQL on an SQL Database System".
  * Paper " O-O-H, What Have They Done to DB2?" is indexed as "OO, What Have They Done to DB2?".
* VLDB 2007:
  * Paper "Making Sense of Suppressions and Failures in Sensor Data: A Bayesian Approach." is indexed as "Suppression and failures in sensor networks: A Bayesian approach"

