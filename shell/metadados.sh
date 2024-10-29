#!/bin/bash
if [ $# -lt 2 ];then
    echo "Uso: <site> <extensao>"
    exit
fi

busca_url="https://google.com/search?num500&q=site:$1+ext:$2"

if [ $? -ne 0 ];then
    echo "Erro ao executar o comando Lynx!"
    exit 
fi

filtrar_url=$(lynx --dump "$busca_url" | grep ".$2" | cut -d "=" -f2 | grep "https://" | grep -v "accounts.google" | sed 's/...$//' )

if [ -z "$filtrar_url" ];then
    echo "Nenhum resultado para extensao .$2"
    exit
fi

echo "$filtrar_url" > dump.txt
for url in $(cat dump.txt);do wget -q $url;done

echo "Encontrados os seguintes arquivos"
echo "********************************************************************************************************"
echo "$filtrar_url"
echo "********************************************************************************************************"
exiftool *.$2
rm *.$2
rm dump.txt