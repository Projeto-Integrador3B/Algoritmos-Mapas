import osmnx as ox

class Visualizador:
    @staticmethod
    def plotar_grafo(grafo):
        if grafo is not None:
            ox.plot_graph(grafo)
        else:
            print("Nenhum grafo para exibir.")
