#!/bin/bash
echo "Parsing URLs"
#echo "Digite a página: "
#read page
wget $1 2>/dev/null
echo "==========================================================================================================="
echo "[+] Salvando arquivo: " $1
echo "==========================================================================================================="

grep href index.html | cut -d "/" -f 3 | grep "\." | cut -d '"' -f 1 | grep -v "<l" > $1.txt
echo "==========================================================================================================="
echo "[+] Resolvendo URLs"
echo "==========================================================================================================="
for url in $(cat $1.txt);
    do host $url;
    done | grep "has address" | sed 's/has address/=========>/' | grep -v "not found" | grep -v "youtube*"
rm index.html $1.txt
