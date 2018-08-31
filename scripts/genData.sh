echo "conference|title|authors|citations|recent|patent|self" > data.all
awk 'function basename(file) {
    sub(".*/", "", file)
        return file
          }BEGIN{FS="|"}{if(NF>4){printf("%s|%s|%s|%d|%d|%d|%d\n",FILENAME,$2,$3,$4,$5,$6,$7);}}END{}' $1 | grep -E -v "International Conference|Front Matter|Letter from the|Cover Page|Sponsors|Copyright Notice" >> data.all

