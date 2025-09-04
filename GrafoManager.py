import osmnx as ox
import pickle

class GrafoManager:
    def __init__(self):
        self.grafo = None

    def baixar_grafo(self, arquivo):
        ponto_central = (-15.7942, -47.8822)  # Coordenadas do Plano Piloto
        dist = 2000  # Distância em metros

        try:
            print("Baixando grafo do OSM...")
            self.grafo = ox.graph_from_point(
                ponto_central,
                dist=dist,
                network_type="drive",
                simplify=True
            )
            # Salvar grafo usando pickle
            with open(arquivo, "wb") as f:
                pickle.dump(self.grafo, f)
            print(f"Grafo salvo em {arquivo} com sucesso!")
        except Exception as e:
            print("Erro ao baixar ou salvar o grafo:", e)

    def carregar_grafo(self, arquivo):
        try:
            with open(arquivo, "rb") as f:
                self.grafo = pickle.load(f)
            print("Grafo carregado com sucesso!")
        except Exception as e:
            print("Erro ao carregar o grafo:", e)

    def exibir_grafo(self):
        if self.grafo is None:
            print("Nenhum grafo para exibir.")
            return
        try:
            ox.plot_graph(self.grafo)
        except Exception as e:
            print("Erro ao exibir o grafo:", e)


