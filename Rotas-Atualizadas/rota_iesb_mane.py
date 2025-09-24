import osmnx as ox
import networkx as nx
import time
from matplotlib.lines import Line2D

# ==============================
# 1) FUNÇÕES AUXILIARES
# ==============================
def remover_avenidas(grafo):
    """Remove avenidas rápidas para forçar Dijkstra a usar ruas locais."""
    banir = {"motorway", "motorway_link", "trunk", "trunk_link",
             "primary", "primary_link"}
    G_local = grafo.copy()
    to_remove = []
    for u, v, k, data in G_local.edges(keys=True, data=True):
        hw = data.get("highway")
        if isinstance(hw, (list, set, tuple)):
            if any(h in banir for h in hw):
                to_remove.append((u, v, k))
        elif hw in banir:
            to_remove.append((u, v, k))
    for u, v, k in to_remove:
        if G_local.has_edge(u, v, k):
            G_local.remove_edge(u, v, k)
    return G_local


def resumo_rotas(dijkstra, astar):
    """Mostra comparativo em formato de tabela."""
    print("\n===== Comparativo =====")
    print(f"{'Algoritmo':<12}{'Distância (km)':<20}{'Tempo estimado (min)':<25}{'Nós no caminho'}")
    print(f"{'Dijkstra':<12}{dijkstra['dist']/1000:<20.2f}{'-':<25}{dijkstra['n_nos']}")
    print(f"{'A*':<12}{astar['dist']/1000:<20.2f}{astar['tempo']/60:<25.1f}{astar['n_nos']}")


# ==============================
# 2) BAIXAR MAPA
# ==============================
print("Baixando mapa reduzido (≈ 4 km em volta do centro IESB↔Mané)...")
center_point = (-15.82, -47.90)
G_full = ox.graph_from_point(center_point, dist=4000, network_type="drive")

# adicionar velocidades e tempos
G_full = ox.add_edge_speeds(G_full)
G_full = ox.add_edge_travel_times(G_full)

# ==============================
# 3) DEFINIR ORIGEM E DESTINO
# ==============================
orig_node = ox.distance.nearest_nodes(G_full, X=-47.9121, Y=-15.8309)   # IESB Asa Sul
dest_node = ox.distance.nearest_nodes(G_full, X=-47.8925, Y=-15.7835)   # Mané Garrincha

# ==============================
# 4) DIJKSTRA (grafo sem avenidas)
# ==============================
print("\nCalculando Dijkstra (ruas locais)...")
G_local = remover_avenidas(G_full)
t0 = time.time()
route_dijkstra = nx.shortest_path(G_local, orig_node, dest_node, weight="length", method="dijkstra")
dt_dijkstra = time.time() - t0
dist_dijkstra = nx.path_weight(G_local, route_dijkstra, weight="length")

dijkstra = {"dist": dist_dijkstra, "tempo_exec": dt_dijkstra, "n_nos": len(route_dijkstra)}

# ==============================
# 5) A* (grafo completo, menor tempo)
# ==============================
print("Calculando A* (vias rápidas)...")
t0 = time.time()
route_astar = nx.astar_path(G_full, orig_node, dest_node, weight="travel_time")
dt_astar = time.time() - t0
time_astar_total = nx.path_weight(G_full, route_astar, weight="travel_time")
dist_astar = nx.path_weight(G_full, route_astar, weight="length")

astar = {"dist": dist_astar, "tempo_exec": dt_astar, "tempo": time_astar_total, "n_nos": len(route_astar)}

# ==============================
# 6) RESUMO NO TERMINAL
# ==============================
resumo_rotas(dijkstra, astar)

# ==============================
# 7) PLOTAR E SALVAR MAPA
# ==============================
print("\nDesenhando rotas...")
fig, ax = ox.plot_graph_routes(
    G_full,
    [route_dijkstra, route_astar],
    route_colors=["r", "g"],  # vermelho = Dijkstra, verde = A*
    route_linewidth=3,
    node_size=0,
    show=False, close=False
)

legend_elements = [
    Line2D([0], [0], color='r', lw=3, label='Dijkstra (distância, ruas internas)'),
    Line2D([0], [0], color='g', lw=3, label='A* (tempo, vias rápidas)')
]
ax.legend(handles=legend_elements, loc='lower right')

fig.savefig("rota_iesb_mane_melhorado.png", dpi=300, bbox_inches="tight")
print("Mapa salvo como 'rota_iesb_mane_melhorado.png'")

# ==============================
# 8) SALVAR RESUMO EM TXT
# ==============================
with open("resumo_rotas.txt", "w") as f:
    f.write("Comparativo de rotas IESB → Mané Garrincha\n")
    f.write("="*40 + "\n")
    f.write(f"Dijkstra → Distância: {dijkstra['dist']/1000:.2f} km | Nós: {dijkstra['n_nos']} | Tempo exec.: {dijkstra['tempo_exec']:.4f} s\n")
    f.write(f"A*       → Distância: {astar['dist']/1000:.2f} km | Tempo: {astar['tempo']/60:.1f} min | Nós: {astar['n_nos']} | Tempo exec.: {astar['tempo_exec']:.4f} s\n")
print("Resumo salvo em 'resumo_rotas.txt'")
