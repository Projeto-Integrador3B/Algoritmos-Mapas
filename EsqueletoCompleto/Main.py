from GrafoManager import GrafoManager
from Visualizador import Visualizador

def menu():
    print("\n=== MENU ===")
    print("1 - Baixar grafo")
    print("2 - Carregar grafo")
    print("3 - Mostrar grafo")
    print("4 - Calcular rotas (A* e Dijkstra)")
    print("5 - Sair")
    return input("Escolha uma opção: ")

if __name__ == "__main__":
    gm = GrafoManager()
    vis = Visualizador()

    while True:
        opcao = menu()

        if opcao == "1":
            lat = float(input("Latitude do ponto central: "))
            lon = float(input("Longitude do ponto central: "))
            raio = int(input("Raio de busca em metros: "))
            gm.baixar_grafo(ponto_central=(lat, lon), distancia=raio)

        elif opcao == "2":
            gm.carregar_grafo()

        elif opcao == "3":
            if gm.grafo:
                vis.exibir_grafo(gm.grafo)
            else:
                print("Carregue ou baixe o grafo primeiro!")

        elif opcao == "4":
            if gm.grafo:
                lat_origem = float(input("Latitude da origem: "))
                lon_origem = float(input("Longitude da origem: "))
                lat_destino = float(input("Latitude do destino: "))
                lon_destino = float(input("Longitude do destino: "))

                no_origem = gm.obter_no_mais_proximo(lat_origem, lon_origem)
                no_destino = gm.obter_no_mais_proximo(lat_destino, lon_destino)

                rota_distancia, rota_tempo, m_d, m_a = gm.calcular_rotas(no_origem, no_destino)

                if rota_distancia and rota_tempo:
                    vis.exibir_rotas(
                        gm.grafo,
                        rota_distancia,
                        rota_tempo,
                        m_d,
                        m_a,
                        salvar_em="rotas.png"
                        
                        
                    )
                else:
                    print("Não foi possível calcular as rotas!")
            else:
                print("Carregue ou baixe o grafo primeiro!")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")
