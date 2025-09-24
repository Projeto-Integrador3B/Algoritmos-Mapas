import osmnx as ox
import networkx as nx
import math
import re

class GrafoManager:
    def __init__(self, arquivo="grafo_brasilia.graphml"):
        self.grafo = None
        self.arquivo = arquivo

    # ------------------------
    # Sanitização de ponto
    # ------------------------
    def _sanitize_point(self, ponto):
        try:
            from shapely.geometry import Point as ShapelyPoint
        except Exception:
            ShapelyPoint = None

        if ShapelyPoint and isinstance(ponto, ShapelyPoint):
            return (float(ponto.y), float(ponto.x))

        if isinstance(ponto, (list, tuple)):
            if len(ponto) != 2:
                raise ValueError(f"ponto_central deve ter 2 elementos (lat, lon). Recebido: {ponto}")
            return float(ponto[0]), float(ponto[1])

        if isinstance(ponto, str):
            parts = re.split(r'[,\s]+', ponto.strip())
            if len(parts) >= 2:
                return float(parts[0]), float(parts[1])
            raise ValueError(f"String ponto_central inválida: {ponto}")

        raise TypeError(f"Tipo de ponto_central não suportado: {type(ponto)} -> {ponto}")

    # ------------------------
    # Baixar e carregar grafo
    # ------------------------
    def baixar_grafo(self, ponto_central, distancia=3000):
        try:
            ponto_central = self._sanitize_point(ponto_central)
            print(f"Ponto central usado: {ponto_central} | Distância: {distancia} m")
            G = ox.graph_from_point(ponto_central, dist=distancia, network_type="drive", simplify=True)
            self.adicionar_tempo_ao_grafo(G)
            ox.save_graphml(G, self.arquivo)
            self.grafo = G
            print("Grafo baixado e salvo com sucesso.")
        except Exception as e:
            print("Erro ao baixar ou salvar o grafo:", repr(e))

    def carregar_grafo(self, arquivo=None):
        arquivo = arquivo or self.arquivo
        try:
            G = ox.load_graphml(arquivo)
            self.adicionar_tempo_ao_grafo(G)
            self.grafo = G
            print("Grafo carregado com sucesso.")
        except Exception as e:
            print("Erro ao carregar o grafo:", repr(e))

    # ------------------------
    # Travel time
    # ------------------------
    def _parse_maxspeed(self, val):
        if val is None:
            return None
        try:
            if isinstance(val, (list, tuple)):
                val = val[0]
            if isinstance(val, str):
                m = re.search(r'(\d+)', val)
                if m:
                    return float(m.group(1))
                else:
                    return None
            return float(val)
        except Exception:
            return None

    def adicionar_tempo_ao_grafo(self, G=None):
        if G is None:
            G = self.grafo
        if G is None:
            return

        velocidades = {
            "motorway": 120,
            "trunk": 90,
            "primary": 60,
            "secondary": 40,
            "tertiary": 30,
            "residential": 20,
            "service": 15,
        }

        for u, v, k, data in G.edges(keys=True, data=True):
            comprimento = data.get("length", 0.0) or data.get("distance", 1.0)
            maxspeed = data.get("maxspeed")
            parsed = self._parse_maxspeed(maxspeed)

            hw = data.get("highway")
            if isinstance(hw, (list, tuple)):
                hw = hw[0]

            velocidade_kmh = parsed or velocidades.get(hw, 30)
            if hw == "residential":
                velocidade_kmh *= 0.7

            velocidade_m_s = max(velocidade_kmh * 1000.0 / 3600.0, 1.0)
            data["travel_time"] = comprimento / velocidade_m_s

    # ------------------------
    # Obter nó mais próximo
    # ------------------------
    def obter_no_mais_proximo(self, lat, lon):
        if self.grafo is None:
            raise RuntimeError("Grafo não carregado")
        return ox.distance.nearest_nodes(self.grafo, lon, lat)

    # ------------------------
    # Distância haversine
    # ------------------------
    def _haversine_m(self, u, v):
        G = self.grafo
        lat1, lon1 = float(G.nodes[u].get("y", G.nodes[u].get("lat"))), float(G.nodes[u].get("x", G.nodes[u].get("lon")))
        lat2, lon2 = float(G.nodes[v].get("y", G.nodes[v].get("lat"))), float(G.nodes[v].get("x", G.nodes[v].get("lon")))
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    # ------------------------
    # Calcular rotas
    # ------------------------
    def calcular_rotas(self, origem, destino):
        if self.grafo is None:
            print("Grafo não carregado!")
            return None, None, None, None
        try:
            # Dijkstra → menor distância
            rota_dist = nx.dijkstra_path(self.grafo, origem, destino, weight="length")
            dist_d = nx.path_weight(self.grafo, rota_dist, weight="length")
            tempo_d = nx.path_weight(self.grafo, rota_dist, weight="travel_time")

            # A* → menor tempo
            vmax_kmh = 120.0
            vmax_ms = vmax_kmh * 1000.0 / 3600.0
            def heur(u, v):
                return self._haversine_m(u, v) / vmax_ms

            rota_tempo = nx.astar_path(self.grafo, origem, destino, heuristic=heur, weight="travel_time")
            dist_a = nx.path_weight(self.grafo, rota_tempo, weight="length")
            tempo_a = nx.path_weight(self.grafo, rota_tempo, weight="travel_time")

            m_d = {
                "nós rota": len(rota_dist),
                "distância": dist_d,
                "tempo": tempo_d
            }
            m_a = {
                "nós rota": len(rota_tempo),
                "distância": dist_a,
                "tempo": tempo_a
            }

            return rota_dist, rota_tempo, m_d, m_a
        except Exception as e:
            print("Erro ao calcular rotas:", repr(e))
            return None, None, None, None
