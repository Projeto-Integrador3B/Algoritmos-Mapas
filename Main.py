from GrafoManager import GrafoManager
import os

arquivo_grafo = "grafo.pkl"
gm = GrafoManager()

def main():
    while True:
        print("\n=== Menu ===")
        print("1. Baixar grafo do OSM")
        print("2. Carregar grafo salvo")
        print("3. Exibir grafo")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if os.path.exists(arquivo_grafo):
                print("Grafo já existe. Carregando do arquivo salvo...")
                gm.carregar_grafo(arquivo_grafo)
            else:
                print("Baixando grafo do OSM...")
                gm.baixar_grafo(arquivo_grafo)

        elif opcao == "2":
            if os.path.exists(arquivo_grafo):
                print("Carregando grafo salvo...")
                gm.carregar_grafo(arquivo_grafo)
            else:
                print("Arquivo de grafo não encontrado. Baixe primeiro.")

        elif opcao == "3":
            if gm.grafo is not None:
                print("Exibindo grafo...")
                gm.exibir_grafo()
            else:
                print("Nenhum grafo carregado. Baixe ou carregue um grafo primeiro.")

        elif opcao == "4":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
