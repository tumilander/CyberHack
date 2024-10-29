#!/bin/bash

if [ $UID -ne 0 ]; then
    echo -e "\e[1;31m\nVocê precisa ser root para executar este script!\e[0m"
    echo -e "\n"
    exit 
fi

findomain --output -t $1
cat $1".txt" | httprobe > resolv.txt
cat resolv.txt | sort -u > param.txt
cat param.txt | httpx -mc 200 -o 200.txt
cat 200.txt | nuclei 
rm $1.txt resolv.txt param.txt 200.txt
            

     