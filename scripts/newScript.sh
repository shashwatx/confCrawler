awk 'BEGIN{FS="|"}{if(NF>4){printf("%s\n",$2);}}END{}' $1 > ~/raw.txt
