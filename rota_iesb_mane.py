import osmnx as ox
import networkx as nx
import time
from matplotlib.lines import Line2D

# ==============================
# 1) MAPA REDUZIDO
# ==============================
print("Baixando mapa reduzido (≈ 4 km em volta do centro IESB↔Mané)...")
center_point = (-15.82, -47.90)          # centro aproximado entre IESB e Mané Garrincha
G_full = ox.graph_from_point(center_point, dist=4000, network_type="drive")

# Velocidades/tempo (para A*)
G_full = ox.add_edge_speeds(G_full)
G_full = ox.add_edge_travel_times(G_full)

# ==============================
# 2) ORIGEM/DESTINO
# ==============================
# IESB Asa Sul
orig_lon, orig_lat = -47.9121, -15.8309
# Estádio Mané Garrincha
dest_lon, dest_lat = -47.8925, -15.7835

orig_full = ox.distance.nearest_nodes(G_full, X=orig_lon, Y=orig_lat)
dest_full = ox.distance.nearest_nodes(G_full, X=dest_lon, Y=dest_lat)

print(f"Origem (nó no grafo completo): {orig_full}")
print(f"Destino (nó no grafo completo): {dest_full}")

# ==============================
# 3) CRIAR UM GRAFO “LOCAL” (SEM AVENIDAS RÁPIDAS)
#    para o Dijkstra priorizar ruas internas/curtas
# ==============================
G_local = G_full.copy()

banir = {"motorway", "motorway_link", "trunk", "trunk_link",
         "primary", "primary_link"}

# remove arestas de vias rápidas
to_remove = []
for u, v, k, data in G_local.edges(keys=True, data=True):
    hw = data.get("highway")
    # 'highway' pode ser lista em alguns casos
    if isinstance(hw, (list, set, tuple)):
        if any(h in banir for h in hw):
            to_remove.append((u, v, k))
    elif hw in banir:
        to_remove.append((u, v, k))

for u, v, k in to_remove:
    if G_local.has_edge(u, v, k):
        G_local.remove_edge(u, v, k)

# Reaproveitamos os mesmos nós (costuma funcionar pois nós continuam no grafo);
# se não houver caminho, faremos fallback mais abaixo.
orig_local, dest_local = orig_full, dest_full

# ==============================
# 4) DIJKSTRA (MENOR DISTÂNCIA) NO GRAFO LOCAL
# ==============================
print("\nCalculando Dijkstra (menor distância) em grafo local...")
try:
    t0 = time.time()
    route_dijkstra = nx.shortest_path(
        G_local, orig_local, dest_local, weight="length", method="dijkstra"
    )
    dt_dijkstra = time.time() - t0
    dist_dijkstra = nx.path_weight(G_local, route_dijkstra, weight="length")
except nx.NetworkXNoPath:
    # Fallback: se remover avenidas cortou a conectividade,
    # faz Dijkstra no grafo completo (ainda mostraremos diferença pelo A*)
    print("Sem caminho no grafo local; usando grafo completo para Dijkstra.")
    t0 = time.time()
    route_dijkstra = nx.shortest_path(
        G_full, orig_full, dest_full, weight="length", method="dijkstra"
    )
    dt_dijkstra = time.time() - t0
    dist_dijkstra = nx.path_weight(G_full, route_dijkstra, weight="length")

print(f"DIJKSTRA → distância: {dist_dijkstra/1000:.2f} km | tempo exec.: {dt_dijkstra:.4f}s | nós: {len(route_dijkstra)}")

# ==============================
# 5) A* (MENOR TEMPO) NO GRAFO COMPLETO
# ==============================
print("Calculando A* (menor tempo) em grafo completo...")
t0 = time.time()
route_astar = nx.astar_path(G_full, orig_full, dest_full, weight="travel_time")
dt_astar = time.time() - t0
time_astar_s = nx.path_weight(G_full, route_astar, weight="travel_time")
dist_astar = nx.path_weight(G_full, route_astar, weight="length")

print(f"A*       → tempo: {time_astar_s/60:.1f} min | distância: {dist_astar/1000:.2f} km | tempo exec.: {dt_astar:.4f}s | nós: {len(route_astar)}")

# ==============================
# 6) PLOT (MESMO BACKGROUND, 2 ROTAS DIFERENTES)
# ==============================
print("\nDesenhando rotas...")
fig, ax = ox.plot_graph_routes(
    G_full,
    [route_dijkstra, route_astar],
    route_colors=["r", "g"],     # vermelho = Dijkstra (ruas locais), verde = A* (avenidas)
    route_linewidth=3,
    node_size=0,
    show=False, close=False
)

# legenda simples
legend_elements = [
    Line2D([0], [0], color='r', lw=3, label='Dijkstra (menor distância, ruas internas)'),
    Line2D([0], [0], color='g', lw=3, label='A* (menor tempo, vias rápidas)')
]
ax.legend(handles=legend_elements, loc='lower right')

fig.savefig("rota_iesb_mane_divergente.png", dpi=300, bbox_inches="tight")
print("Mapa salvo como 'rota_iesb_mane_divergente.png'")
