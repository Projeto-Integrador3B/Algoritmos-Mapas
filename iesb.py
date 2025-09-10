import osmnx as ox
import networkx as nx
import time

# ==============================
# 1. BAIXAR O MAPA DO PLANO PILOTO
# ==============================
print("Baixando mapa do Plano Piloto (pode demorar um pouco)...")
G = ox.graph_from_place("Plano Piloto, Brasília, Brazil", network_type="drive")

# ==============================
# 2. DEFINIR ORIGEM E DESTINO
# ==============================
# Origem: IESB Asa Sul
orig_node = ox.distance.nearest_nodes(G, X=-47.9121, Y=-15.8309)

# Destino: McDonald's 604 Sul
dest_node = ox.distance.nearest_nodes(G, X=-47.9147, Y=-15.8375)

print(f"Nó de origem (IESB Asa Sul): {orig_node}")
print(f"Nó de destino (McDonald's 604 Sul): {dest_node}")

# ==============================
# 3. ALGORITMO DE DIJKSTRA
# ==============================
start_time = time.time()
route_dijkstra = nx.shortest_path(G, orig_node, dest_node,
                                  weight="length", method="dijkstra")
time_dijkstra = time.time() - start_time
length_dijkstra = nx.path_weight(G, route_dijkstra, weight="length")

print(f"\n[Dijkstra]")
print(f"Tempo: {time_dijkstra:.6f} segundos")
print(f"Distância total: {length_dijkstra:.2f} metros")
print(f"Nós no caminho: {len(route_dijkstra)}")

# ==============================
# 4. ALGORITMO A*
# ==============================
start_time = time.time()
route_astar = nx.astar_path(G, orig_node, dest_node, weight="length")
time_astar = time.time() - start_time
length_astar = nx.path_weight(G, route_astar, weight="length")

print(f"\n[A*]")
print(f"Tempo: {time_astar:.6f} segundos")
print(f"Distância total: {length_astar:.2f} metros")
print(f"Nós no caminho: {len(route_astar)}")

# ==============================
# 5. VISUALIZAÇÃO
# ==============================
print("\nDesenhando rotas...")
fig, ax = ox.plot_graph_routes(
    G, [route_dijkstra, route_astar],
    route_colors=['r', 'g'],  # vermelho = Dijkstra, verde = A*
    route_linewidth=3,
    node_size=0
)

