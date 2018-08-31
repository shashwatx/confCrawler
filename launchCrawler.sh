#!/bin/bash

rm -rf _SUCCESS

log(){
    echo "[$(date)]: $*"
}

log "start"

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blue=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

existsContext(){

    if [ -f conferences.dat ]; then
        log "context found"
        return 0
    fi
    return -1
}

asksure() {
    printf "\nI found local context: ${red}conferences.dat${end}\n"
    printf "Press Y/y to resume context. To start new context, press N/n ? "
    while read -r -n 1 -s answer; do
        if [[ $answer = [YyNn] ]]; then
            [[ $answer = [Yy] ]] && purgeVal=0
            [[ $answer = [Nn] ]] && purgeVal=1
            break
        fi
    done
}


if existsContext; then
    purgeVal=0
    asksure
    echo
    if [[ $purgeVal -eq 1 ]]; then
        rm -rf conferences.dat
        rm -rf paper.dat
        log "context purged"
    fi
fi


log "relaunch tor; sleep for 15"

pidof tor > /dev/null
if [[ $? -eq 0 ]]; then
    pidof tor | xargs 'kill'
fi

tor --quiet -f torrc&

sleep 15

while true; do

    ./fetchNewProxies

    log "launch crawler"
    python crawler.py
       
    if [ ! -f _SUCCESS ]; then
        timeCur=`date +%s`
	timeOnThisConfSoFar=$(($timeCur-$1)) 
	log "premature crawler exit...time spent on this conference: ${mag}$timeOnThisConfSoFar${end} seconds"
	log "relaunch tor; sleep for 15"
	pidof tor > /dev/null
	if [[ $? -eq 0 ]]; then
		pidof tor | xargs 'kill'
	fi
        tor --quiet -f torrc&
        sleep 15
    else
        log "${cyn}mature crawler exit${end}"
        exit 0
    fi
done
