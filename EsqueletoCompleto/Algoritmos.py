import networkx as nx

def a_estrela(grafo, origem, destino):
    """
    Calcula o caminho mais curto usando A*.
    """
    try:
        caminho = nx.astar_path(grafo, origem, destino, weight='length')
        return caminho
    except nx.NetworkXNoPath:
        print("Nenhum caminho encontrado pelo A*.")
        return []

def dijkstra(grafo, origem, destino):
    """
    Calcula o caminho mais curto usando Dijkstra.
    """
    try:
        caminho = nx.dijkstra_path(grafo, origem, destino, weight='length')
        return caminho
    except nx.NetworkXNoPath:
        print("Nenhum caminho encontrado pelo Dijkstra.")
        return []
