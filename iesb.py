import osmnx as ox
import networkx as nx
import time

# ==============================
# 1. BAIXAR O MAPA DO PLANO PILOTO
# ==============================
print("Baixando mapa do Plano Piloto (pode demorar um pouco)...")
G = ox.graph_from_place("Plano Piloto, Brasília, Brazil", network_type="drive")

# ==============================
# 2. ADICIONAR VELOCIDADES E TEMPO DE VIAGEM
# ==============================
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# ==============================
# 3. DEFINIR ORIGEM E DESTINO
# ==============================
# Origem: IESB Asa Sul
orig_node = ox.distance.nearest_nodes(G, X=-47.9121, Y=-15.8309)

# Destino: Quadra 313 Norte
dest_node = ox.distance.nearest_nodes(G, X=-47.8826, Y=-15.7455)

print(f"Nó de origem (IESB Asa Sul): {orig_node}")
print(f"Nó de destino (Quadra 313 Norte): {dest_node}")

# ==============================
# 4. ALGORITMO DE DIJKSTRA (distância)
# ==============================
start_time = time.time()
route_dijkstra = nx.shortest_path(G, orig_node, dest_node,
                                  weight="length", method="dijkstra")
time_dijkstra = time.time() - start_time
length_dijkstra = nx.path_weight(G, route_dijkstra, weight="length")

print(f"\n[Dijkstra - Distância]")
print(f"Tempo de execução: {time_dijkstra:.6f} segundos")
print(f"Distância total: {length_dijkstra/1000:.2f} km")
print(f"Nós no caminho: {len(route_dijkstra)}")

# ==============================
# 5. ALGORITMO A* (tempo de viagem)
# ==============================
start_time = time.time()
route_astar = nx.astar_path(G, orig_node, dest_node, weight="travel_time")
time_astar = time.time() - start_time
time_astar_total = nx.path_weight(G, route_astar, weight="travel_time")
length_astar = nx.path_weight(G, route_astar, weight="length")

print(f"\n[A* - Tempo de viagem]")
print(f"Tempo de execução: {time_astar:.6f} segundos")
print(f"Tempo estimado de viagem: {time_astar_total/60:.1f} minutos")
print(f"Distância total: {length_astar/1000:.2f} km")
print(f"Nós no caminho: {len(route_astar)}")

# ==============================
# 6. VISUALIZAÇÃO
# ==============================
print("\nDesenhando rotas...")
fig, ax = ox.plot_graph_routes(
    G,
    [route_dijkstra, route_astar],
    route_colors=['r', 'g'],   # vermelho = Dijkstra, verde = A*
    route_linewidth=3,
    node_size=0
)

