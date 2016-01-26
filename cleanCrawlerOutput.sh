getConfName() {
    IFS='/' read -ra arr <<<$1
    conf=${arr[1]}
    IFS='\.' read -ra arr2 <<<$conf
    conf=${arr2[0]}
}

FILES=$1
printf "[\n"
for f in $FILES*
do
    conf="unknown"
    getConfName $f

    tail -n+2 $f > dump

    while read -r line
    do
        #$line
        
        if [[ $line == *"n/a"* ]]
        then
            #echo "$line";
            x=0
        else
            #echo $line
            idx=0;
            printf "{"
            IFS='|' read -ra ADDR <<<$line
            for i in "${ADDR[@]}"; do
                if [[ $idx == 1 ]]
                then
                    titleEnhanced=$(sed -e 's/"//g'<<<$i)
                    printf "title: \"%s\"," "$titleEnhanced";
                fi
                if [[ $idx == 2 ]]
                then
                    printf " authors: \"%s\"," "$i";
                fi
                if [[ $idx == 3 ]]
                then
                    printf " citations: \"%s\"," "$i";
                fi
                if [[ $idx == 5 ]]
                then
                    printf " selfcitations: \"%s\"," "$i";
                fi
                if [[ $idx == 6 ]]
                then
                    printf " patentcitations: \"%s\"," "$i";
                fi
                ((idx++))
            done
            printf " conf: \"%s\"" "$conf";
            printf "},\n"
        fi
    done < "dump"

done
printf "]\n"
rm -rf dump
