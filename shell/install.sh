#!/bin/bash

if [ $UID -ne 0 ]; then
    echo -e "\e[1;31m\nVocê precisa ser root para executar este script!\e[0m"
    echo -e "\n"
    exit 
fi


chmod +x ./metadados.sh
chmod +x ./parsing.sh
chmod +x ./vuln.sh
chmod +x ./xss.sh

echo -e "\n\n\033[33;1mUnzip \033[m";

if [ -e /usr/bin/unzip ];then
        echo -e "\033[32;1mUnzip Ok\033[m";
else
        echo -e "\n\n\033[32;1m Instalando golang \033[m";
        apt-get install unzip -y
fi

echo -e "\n\n\033[33;1mGolang \033[m";

com=$(go version | cut -d " " -f 3)
if [ $com == go1.21 ];then
        echo -e "\n\n\033[32;1m Instalando golang \033[m";
        curl -LO https://go.dev/dl/go1.21.1.linux-amd64.tar.gz
        rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz
        export PATH=$PATH:/usr/local/go/bin
        rm go1.21.1.linux-amd64.tar.gz
     
else
        echo -e "\033[32;1mGolang Ok\033[m";  
fi

echo -e "\n\n\033[33;1mFindomain\033[m";
if [ -e /usr/bin/findomain ];then
        echo -e "\033[32;1mFindomain Ok\033[m";
else
        curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip;
        unzip findomain-linux-i386.zip;
        chmod +x findomain;
        mv findomain /usr/bin/findomain;
        rm findomain-linux-i386.zip;
fi

echo -e "\n\n\033[33;1mHTTPROBE\033[m";

if [ -e /usr/bin/httprobe ];then
        echo -e "\033[32;1mHTTPROBE Ok\033[m";
else
        go install github.com/tomnomnom/httprobe@latest;
        mv /root/go/bin/httprobe /usr/bin/;
fi


echo -e "\n\n\033[33;1mNuclei\033[m";

if [ -e /usr/bin/nuclei ];then
        echo -e "\033[32;1mNuclei Ok\033[m";
else
        go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest;
        mv /root/go/bin/nuclei /usr/bin/;
fi

echo -e "\n\n\033[33;1mDalfox\033[m";

if [ -e /usr/bin/dalfox ];then
        echo -e "\033[32;1mNDalfox Ok\033[m";
else
        go install github.com/hahwul/dalfox/v2@latest;
        mv /root/go/bin/dalfox /usr/bin/;
fi


echo -e "\n\n\033[33;1mHTTPX\033[m";

if [ -e /usr/bin/httpx ];then
        echo -e "\033[32;1mHttpx Ok\033[m";
else
        go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest;
        mv /root/go/bin/httpx /usr/bin/;
fi

echo -e "\n\n\033[33;1mGAU\033[m";

if [ -e /usr/bin/gau ];then
        echo -e "\033[32;1m GAU Ok\033[m";
else
        go install github.com/lc/gau/v2/cmd/gau@latest;
        mv /root/go/bin/gau /usr/bin/;
fi

echo -e "\n\n\033[33;1mLynx\033[m";

if [ -e /usr/bin/lynx ];then
        echo -e "\033[32;1m Lynx Ok\033[m";
else
       apt-get install lynx -y
fi

echo -e "\n\n\033[33;1mExiftool\033[m";
if [ -e /usr/bin/exiftool ];then
        echo -e "\033[32;1m Lynx Ok\033[m";
else
       apt-get install exiftool -y
fi

echo -e "\n\n\033[33;1mCaso houver problemas com GO siga os passos abaixo:\033[m"
echo "================================================================================="
echo "     sudo rm -rf /usr/local/go"                                                  
echo "     curl -LO https://go.dev/dl/go1.21.1.linux-amd64.tar.gz"                     
echo "     rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz" 
echo "     export PATH=/\$PATH:/usr/local/go/bin"                                      
echo "================================================================================="