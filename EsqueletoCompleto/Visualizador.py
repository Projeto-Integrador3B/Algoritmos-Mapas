import osmnx as ox
import matplotlib.pyplot as plt

class Visualizador:
    def exibir_grafo(self, grafo, salvar_em=None):
        fig, ax = ox.plot_graph(
            grafo,
            node_size=0,
            edge_color="gray",
            show=False,
            close=False
        )
        if salvar_em:
            plt.savefig(salvar_em, dpi=150)
            print(f"Grafo salvo em {salvar_em}")
        plt.show()

    def exibir_rotas(self, grafo, rota_distancia, rota_tempo, m_d=None, m_a=None, salvar_em="rotas.png"):
        """Exibe apenas as rotas (Dijkstra e A*) sem mostrar os nós visitados."""
        fig, ax = ox.plot_graph_routes(
            grafo,
            routes=[rota_distancia, rota_tempo],
            route_colors=["red", "blue"],
            route_linewidth=3,
            node_size=0,
            show=False,
            close=False
        )

        # legenda
        red = plt.Line2D([0], [0], color="red", lw=3, label="Menor distância (Dijkstra)")
        blue = plt.Line2D([0], [0], color="blue", lw=3, label="Menor tempo (A*)")
        ax.legend(handles=[red, blue], loc="upper left", fontsize=9, frameon=True)

        if salvar_em:
            plt.savefig(salvar_em, dpi=150)
            print(f"Imagem salva em {salvar_em}")
        plt.show()

        # imprime métricas no console
        if m_d and m_a:
            print("\n--- Métricas ---")
            print(f"Dijkstra (distância) → {m_d['nós rota']} nós no caminho | {m_d['distância']:.2f} m | {m_d['tempo']:.2f} s")
            print(f"A* (tempo)           → {m_a['nós rota']} nós no caminho | {m_a['distância']:.2f} m | {m_a['tempo']:.2f} s")
