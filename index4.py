import requests
from deep_translator import GoogleTranslator
import os
from colorama import Fore, Style, init

# Função para obter conselhos traduzidos da API
def obter_conselhos(quantidade, traduzir=True):
    conselhos = []
    for _ in range(quantidade):
        try:
            resposta = requests.get("https://api.adviceslip.com/advice")
            if resposta.status_code == 200:
                dados = resposta.json()
                conselho = dados.get("slip", {}).get("advice", "")
                if conselho:
                    # Traduz automaticamente, se solicitado
                    if traduzir:
                        conselho = traduzir_conselho(conselho)
                    conselhos.append(conselho)
            else:
                print("Erro ao Obter Conselho da API.")
        except Exception as e:
            print(f"Não foi possível obter conselhos no momento. Tente novamente mais tarde.: {e}")
    return conselhos


# Função para exibir os conselhos na tela
def mostrar_conselhos(conselhos):
    if conselhos:
        for conselho in conselhos:
            print(f"Conselho: {conselho}")
    else:
        print("Nenhum Conselho Encontrado!")


# Função para salvar conselhos em um arquivo
def salvar_conselhos(conselhos, arquivo="conselhos.txt"):
    try:
        with open(arquivo, "a", encoding="utf-8") as f:
            for conselho in conselhos:
                f.write(f"{conselho}\n")
        print(f"Conselhos Salvos em '{arquivo}' com Sucesso!")
    except Exception as e:
        print(f"Erro ao Salvar os Conselhos: {e}")


# Função para ler conselhos salvos no arquivo
def ler_conselhos(arquivo="conselhos.txt"):
    try:
        if not os.path.exists(arquivo) or os.path.getsize(arquivo) == 0:
            print("Nenhum Conselho Salvo Ainda.")
            return []
        with open(arquivo, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        print(f"Erro ao Ler o Arquivo: {e}")
        return []


# Função para traduzir conselhos para português
def traduzir_conselho(conselho, idioma_destino="pt"):
    try:
        traduzido = GoogleTranslator(source="auto", target=idioma_destino).translate(conselho)
        return traduzido
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return conselho


# Função para traduzir conselhos armazenados no arquivo
def traduzir_conselhos_arquivo(arquivo="conselhos.txt", idioma_destino="en"):
    try:
        linhas = ler_conselhos(arquivo)
        if not linhas:
            print("Nenhum conselho salvo no arquivo para traduzir.")
            return

        print(f"\nConselhos traduzidos para '{idioma_destino}':")
        for linha in linhas:
            try:
                conselho = linha.strip()
                # Traduz o conselho para o idioma escolhido
                traducao = traduzir_conselho(conselho, idioma_destino)
                print(f"Tradução: {traducao}")
            except Exception as e:
                print(f"Erro ao processar a linha: {linha.strip()} - {e}")
    except Exception as e:
        print(f"Erro ao traduzir os conselhos do arquivo: {e}")


# Função do menu principal
def menu():
    conselhos_memoria = []  # Armazena conselhos obtidos na execução atual
    vermelho = "\033[31m"  # Cor vermelha
    reset = "\033[0m"      # Reset de cor
    init(autoreset=True)

    while True:
        print("------------------------------------------------------------------------------------")
        print(f"\n{Fore.BLUE}\033[1m---> Menu do Seu Zé <---{Style.RESET_ALL}")
        print(f"\n{Fore.RED}\033[1m1.{Style.RESET_ALL} Ouvir o Seu Zé - Buscar Conselhos Traduzidos para Português")
        print(f"{Fore.RED}\033[1m2.{Style.RESET_ALL} Veja os Conselhos - Mostrar Conselhos da Memória")
        print(f"{Fore.RED}\033[1m3.{Style.RESET_ALL} Guardar a Sabedoria - Salvar Conselhos no Arquivo")
        print(f"{Fore.RED}\033[1m4.{Style.RESET_ALL} Mostrar os Conselhos Salvos - Ler Arquivo")
        print(f"{Fore.RED}\033[1m5.{Style.RESET_ALL} Traduzir Conselhos - Exibir Traduções dos Conselhos")
        print(f"{Fore.RED}\033[1m6.{Style.RESET_ALL} Traduzir Conselhos Salvos - Exibir Traduções do Arquivo")
        print(f"{Fore.RED}\033[1m0.{Style.RESET_ALL} Sair")

        opcao = input("\nPor favor, escolha a opção desejada: ")

        if opcao == "1":
            try:
                qtd = int(input("Quantos Conselhos Você Deseja Buscar? "))
                conselhos_memoria = obter_conselhos(qtd)
                mostrar_conselhos(conselhos_memoria)
            except ValueError:
                print("Por favor, digite um número válido.")
        elif opcao == "2":
            mostrar_conselhos(conselhos_memoria)
        elif opcao == "3":
            if conselhos_memoria:
                salvar_conselhos(conselhos_memoria)
            else:
                print("Nenhum Conselho Disponível Ainda para Salvar. Use a opção 1 primeiro.")
        elif opcao == "4":
            conselhos = ler_conselhos()
            if conselhos:
                for c in conselhos:
                    print(c.strip())
        elif opcao == "5":
            idioma = input("Digite o idioma que deseja traduzir (ex: en, es, fr): ").strip()
            if conselhos_memoria:
                for conselho in conselhos_memoria:
                    traducao = traduzir_conselho(conselho, idioma)
                    print(f"Tradução: {traducao}")
            else:
                print("Nenhum Conselho na Memória Ainda. Use a opção 1 primeiro.")
        elif opcao == "6":
            idioma = input("Digite o idioma que deseja traduzir (ex: en, es, fr): ").strip()
            traduzir_conselhos_arquivo(idioma_destino=idioma)
        elif opcao == "0":
            print("Até a próxima, Seu Zé! Seus conselhos foram super válidos, thank you!")
            break
        else:
            print("Opção inválida, tente novamente.")


# Iniciar o programa
if __name__ == "__main__":
    menu()
