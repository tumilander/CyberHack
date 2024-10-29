#!/usr/bin/python3
############################
##     Desenvolvido       ##
##         by             ##  
##   Anderson Ribeiro     ##
############################

import hashlib
import csv
import os
import pyfiglet
import requests
import sys
import subprocess

RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"
MAGENTA = "\033[095m"
WHITE = "\033[97"



def signal_handler(sig, frame):
    print("\nSaindo do Script...")
    sys.exit(0)

def install_ns_linux(script):
    print("")
    print(CYAN+"***************************************")
    print("Estrutura script de Instalação NS Linux")
    print("***************************************"+RESET)
    lines = script.strip().split('\n')
    for line in lines:
        print(line)

## inicio das funções -- identificação de hash em arquivo .csv
def hash_identifier(hash_list):
    hash_types = {
        32: "MD5",
        40: "SHA1",
        64: "SHA256"

    }

    identified_hashes = {}

    for hash_value in hash_list:
        hash_type = hash_types.get(len(hash_value))
        if hash_type:
            identified_hashes[hash_value] = hash_type
    
    return identified_hashes

def identify_hashes_in_csv(n_coluna, input_file, output_file,):
    identified_hashes = {}

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            hash_list = row[n_coluna].split(',') ## Feito com variável || input depende do usuário
            row_hashes = hash_identifier(hash_list)
            identified_hashes.update(row_hashes)

    with open(output_file,'w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output)
        for hash_value, hash_type in identified_hashes.items():
            csv_writer.writerow([hash_value, hash_type])
    print("")
    print("*************************************************************")
    print("Identificação de hashs finalizada e salvo em: ", output_file)
    print("*************************************************************")     
    print("")

def obter_detalhes_ip(ip):
    url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data
        else:
            return {"error": "Erro na resposta da API"}
    else:
        return {"error": "Erro na chamada HTTP" }
def parsing(url):
    try:
        comando = subprocess.run(["bash","./shell/parsing.sh",url], text=True, capture_output=True)
        if comando.returncode == 0:
            print(comando.stdout)
        else:
            print("Erro: ")
            print(comando.stderr)
    except subprocess.CalledProcessError as erro:
        print(f"Erro ao executar o script: {erro}")

def metadados(domain,tipo):
    try:
        comando = subprocess.run(["bash","./shell/metadados.sh",domain,tipo], text=True, capture_output=True)
        if comando.returncode == 0:
            print(comando.stdout)
        else:
            print("Erro: ")
            print(comando.stderr)
    except subprocess.CalledProcessError as erro:
        print(f"Erro ao executar o script: {erro}")

def cred():
    subprocess.run(["python3","cred.py"])

def sqli():
    subprocess.run(["python3","sqli.py"])

def xss(url):
    try:
        comando = subprocess.run(["bash","./shell/xss.sh",url], text=True, capture_output=True)
        if comando.returncode == 0:
            print(comando.stdout)
        else:
            print("Erro: ")
            print(comando.stderr)
    except subprocess.CalledProcessError as erro:
        print(f"Erro ao executar o script: {erro}")

def vuln(url):
    try:
        comando = subprocess.run(["bash","./shell/vuln.sh",url], text=True, capture_output=True)
        if comando.returncode == 0:
            print(comando.stdout)
        else:
            print("Erro: ")
            print(comando.stderr)
    except subprocess.CalledProcessError as erro:
        print(f"Erro ao executar o script: {erro}")
     
def menu():
    banner_text = "CyberHack"
    small_text = "by Anderson"

    space = " " * ((len(banner_text) - len(small_text)) // 2)
    banner = pyfiglet.figlet_format(banner_text,font="slant")
    bannerander =  pyfiglet.figlet_format(space + small_text, font="digital")
    print(BLUE+banner+RESET)
    print(CYAN+bannerander+RESET)
  
    while True:
        try:            
                print("")
                print(f"1 - Identificar hashs em um arquivo CSV""                        ""6 - Verificar metadados de arquivos publicos de dominios") 
                #print(f"2 - Exibe o script para instalação do Netskope no Linux""        ""7 - Encontrar possiveis urls para SQLi")
                print(f"3 - Realiza busca e detalhes AS de IP/Dominios""                 ""8 - Verifca XSS automaticamente")
                print(f"4 - Realizar parsing na página e obter url e IPs""               ""9 - Busca Vulns Automaticamente")
                print(f"5 - Realizar validacao de credenciais vazadas")
                #print("6 - Verificar metadados de arquivos publicos de dominios")
                #print("7 - Encontrar possiveis urls para SQLi")
                print("")
                print(UNDERLINE+"0 - Sair"+RESET)
                print("")
                choice = input("Digite sua opção: ") 
                if choice == '1':
                    try:
                        n_coluna = int(input("Digital qual coluna do arquivo esta o hash: ")) ## variavel criada para inserção da coluna(do aqruivo) onde esta o hash
                        input_file = input("Digite o caminho do arquivo .csv: ")## caminho do arquivo.csv exemplo /home/anderson/Documentos/arquivo.csv
                        output_file = input("Digite o caminho e nome de saÃ­da do arquivo em .csv: ") ## caminho para salvar o arquivo filtrado hashs em .csv exemplo /home/anderson/Documentos/arqfiltrado.csv
                        identify_hashes_in_csv(n_coluna, input_file, output_file)
                    except Exception as error:
                        print("*********************************************************************")
                        print("*****Favor insira os caminhos dos arquivos de entrada e de saída*****")
                        print("*********************************************************************")
                        print(error) ## --> identifica o erro 

                #Selif choice == '2':
                #S    install_ns_linux(script_ns)

                elif choice == '3':
                   ip = input("Digite um IP/Dominio: ")
                   detalhes_ip = obter_detalhes_ip(ip)
                   if 'error' in detalhes_ip:
                       print(detalhes_ip['error'])
                   else:
                         print("")
                         print("Detalhes do IP/Dominio")
                         print(MAGENTA+"="*50 + RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"País: {detalhes_ip['country']} ({detalhes_ip['countryCode']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"Região: {detalhes_ip['regionName']} ({detalhes_ip['region']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"Cidade: ({detalhes_ip['city']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"CEP/ZIP: ({detalhes_ip['zip']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"Fuso Horário: ({detalhes_ip['timezone']}"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"ISP: ({detalhes_ip['isp']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"Organizações: ({detalhes_ip['org']})"+RESET)
                         print(MAGENTA+" = "+RESET+YELLOW+f"AS: ({detalhes_ip['as']})"+RESET)
                         print(MAGENTA+"="*50+RESET)

                elif choice == '4':
                    print("")
                    url = input("Digite o dominio: ")
                    parsing(url)

                elif choice == '5':
                    print("")
                    print(BOLD + "Nao se esqueca de inserir os usuarios e senhas no arquivo" + RESET + RED + "./credenciais/cred.txt" + RESET + "\nSeparados por um espaco!!")
                    print("")
                    cred()

                elif choice == '6':
                    print("")
                    print(YELLOW+"Exemplo:\ndominio.com\npdf"+RESET)
                    print("")
                    domain = input("Digite o dominio: ")
                    tipo = input("Digite o tipo de arquivo: ")
                    print("")
                    metadados(domain,tipo)

                elif choice == '7':
                    sqli()

                elif choice == '8':
                    print("")
                    url = input("Digite o dominio: ")
                    xss(url)

                elif choice == '9':
                    print("")
                    url = input("Digite o dominio: ")
                    vuln(url) 

                elif choice == '0':
                    print("="*28)
                    print("= ""Finalizando e fechando...""=")
                    print("="*28)
                    break
                else:
                    print("")
                    print("Opção inválida. Por favor, tente novamente.")
        except KeyboardInterrupt:
            print("\n\nVoce pressionou Ctrl+C para interromper este programa!\nSAINDO...!\n")
            break
                        
menu()