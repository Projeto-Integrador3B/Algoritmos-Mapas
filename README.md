# Algoritmos-Mapas 🗺️

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OSMnx](https://img.shields.io/badge/OSMnx-Latest-green.svg)](https://osmnx.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Sobre o Projeto

Sistema de análise e cálculo de rotas em mapas reais utilizando dados do OpenStreetMap (OSM). O projeto implementa algoritmos clássicos de grafos (Dijkstra e A*) para encontrar caminhos ótimos em malhas viárias urbanas, com foco em Brasília-DF.

Desenvolvido como Projeto Integrador, este sistema permite:
- Download e processamento de mapas reais do OpenStreetMap
- Cálculo de rotas otimizadas por distância (Dijkstra) ou tempo (A*)
- Visualização gráfica das rotas calculadas
- Análise comparativa entre diferentes algoritmos de pathfinding

## 🎯 Objetivos

- Implementar algoritmos clássicos de busca em grafos (Dijkstra e A*)
- Aplicar conceitos de estruturas de dados em problemas reais de roteamento
- Trabalhar com dados geográficos reais do OpenStreetMap
- Comparar performance e resultados entre diferentes estratégias de busca
- Desenvolver sistema interativo para cálculo de rotas urbanas

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.8+
- **Bibliotecas principais:**
  - `osmnx`: Download e manipulação de mapas do OpenStreetMap
  - `networkx`: Implementação de algoritmos de grafos
  - `matplotlib`: Visualização de mapas e rotas
  - `shapely`: Manipulação de geometrias espaciais
- **Estruturas de Dados:** Grafos ponderados direcionados
- **Algoritmos:** 
  - **Dijkstra** (menor distância)
  - **A*** (menor tempo de viagem com heurística)

## 📁 Estrutura do Projeto

```
Algoritmos-Mapas/
│
├── Esqueleto-Inicial/          # Versão básica do projeto
│   ├── GrafoManager.py         # Classe para gerenciar grafos (com pickle)
│   ├── Visualizador.py         # Classe para visualização básica
│   └── main.py                 # Menu principal básico
│
├── EsqueletoCompleto/         # ⭐ VERSÃO PRINCIPAL E MAIS COMPLETA
│   ├── GrafoManager.py         # Gerenciamento avançado de grafos
│   ├── Visualizador.py         # Visualização de rotas comparativas
│   └── main.py                 # Interface interativa completa
│
├── Rotas-Atualizadas/           # Exemplos de casos de uso específicos
│   ├── rota_iesb_mane.py       # Rota IESB → Estádio Mané Garrincha
│   ├── rota_iesb_mane_melhorado.py  # Versão otimizada
│   └── rota_iesb_scn.py        # Rota IESB → Setor Comercial Norte
│
└── README.md                   # Este arquivo
```

## 💻 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Projeto-Integrador3B/Algoritmos-Mapas.git
cd Algoritmos-Mapas
```

2. Instale as dependências:
```bash
pip install osmnx networkx matplotlib shapely
```

### Executando o Projeto Principal

A versão mais completa está na pasta `EsqueletoCompleto`:

```bash
cd EsqueletoCompleto
python main.py
```

### Menu de Opções

O sistema oferece um menu interativo:

```
=== MENU ===
1 - Baixar grafo
2 - Carregar grafo
3 - Mostrar grafo
4 - Calcular rotas (A* e Dijkstra)
5 - Sair
```

**Opção 1 - Baixar grafo:** Baixa um mapa do OpenStreetMap
- Informe latitude e longitude do ponto central
- Defina o raio de busca em metros
- O grafo é salvo em formato GraphML

**Opção 2 - Carregar grafo:** Carrega um grafo previamente salvo

**Opção 3 - Mostrar grafo:** Visualiza o mapa carregado

**Opção 4 - Calcular rotas:** Calcula e compara rotas
- Informe coordenadas de origem e destino
- O sistema calcula automaticamente:
  - Rota de menor distância (Dijkstra)
  - Rota de menor tempo (A*)
- Exibe comparação visual e métricas

## 📖 Algoritmos Implementados

### 1. Dijkstra (Menor Distância)
- **Descrição:** Encontra o caminho de menor distância entre dois pontos
- **Peso utilizado:** Comprimento das vias (`length`)
- **Complexidade:** O((V + E) log V) onde V = vértices, E = arestas
- **Uso:** Ideal para rotas que priorizam menor quilometragem
- **Cor na visualização:** Vermelho

### 2. A* (Menor Tempo)
- **Descrição:** Encontra o caminho de menor tempo de viagem usando heurística
- **Peso utilizado:** Tempo de viagem (`travel_time`)
- **Heurística:** Distância haversine dividida pela velocidade máxima
- **Complexidade:** O(E log V) no melhor caso
- **Uso:** Ideal para rotas que priorizam chegada mais rápida
- **Cor na visualização:** Azul

### Cálculo de Tempo de Viagem

O sistema calcula o tempo de viagem considerando:
- Velocidades padrão por tipo de via:
  - Motorway (rodovias): 120 km/h
  - Trunk (vias expressas): 90 km/h
  - Primary (vias primárias): 60 km/h
  - Secondary (vias secundárias): 40 km/h
  - Tertiary (vias terciárias): 30 km/h
  - Residential (ruas residenciais): 20 km/h × 0.7
  - Service (vias de serviço): 15 km/h
- Limite de velocidade da via quando disponível (`maxspeed`)
- Comprimento das vias em metros

Fórmula: `tempo = distância / velocidade`

## 📝 Exemplos de Uso

### Exemplo 1: Rota no Plano Piloto de Brasília (EsqueletoCompleto)

Execute o sistema principal:
```bash
cd EsqueletoCompleto
python main.py
```

Usando o menu interativo (siga os passos):

**Passo 1 - Baixar ou carregar o grafo:**
```
Opção 1: Baixar mapa do Plano Piloto
  Latitude do ponto central: -15.7942
  Longitude do ponto central: -47.8822
  Raio: 3000

OU

Opção 2: Carregar grafo salvo (se já baixou anteriormente)
```

**Passo 2 (Opcional) - Visualizar o mapa:**
```
Opção 3: Mostrar grafo (para visualizar a área carregada)
```

**Passo 3 - Calcular rotas:**
```
Opção 4: Calcular rotas
  Origem: IESB Asa Sul
    Latitude: -15.8309
    Longitude: -47.9121
  Destino: Estádio Mané Garrincha
    Latitude: -15.7835
    Longitude: -47.8925
```

**⚠️ Importante:** Você precisa executar a **Opção 1 ou 2** primeiro para carregar o grafo antes de calcular rotas (Opção 4).

**Resultado esperado:**
- Dijkstra: Rota mais curta em distância (passa por vias locais)
- A*: Rota mais rápida (pode usar vias expressas)

### Exemplo 2: Executando Scripts Específicos

```bash
cd Rotas-Atualizadas
python rota_iesb_mane_melhorado.py
```

Este script:
1. Baixa mapa de 4km ao redor da região
2. Calcula rotas IESB → Mané Garrincha
3. Remove avenidas rápidas para Dijkstra (força uso de ruas locais)
4. Salva imagem comparativa em `rota_iesb_mane_melhorado.png`
5. Gera arquivo de resumo `resumo_rotas.txt`

## 🎨 Características Principais

### GrafoManager (EsqueletoCompleto)

**Métodos principais:**
- `baixar_grafo(ponto_central, distancia)`: Download de mapas do OSM
- `carregar_grafo(arquivo)`: Carrega grafo salvo em GraphML
- `adicionar_tempo_ao_grafo()`: Calcula tempo de viagem para cada via
- `obter_no_mais_proximo(lat, lon)`: Encontra nó mais próximo de coordenadas
- `calcular_rotas(origem, destino)`: Calcula rotas com Dijkstra e A*

**Funcionalidades especiais:**
- Sanitização automática de pontos geográficos
- Parsing robusto de limites de velocidade
- Cálculo de distância haversine para heurística A*
- Suporte a múltiplos formatos de entrada de coordenadas

### Visualizador

**Métodos principais:**
- `exibir_grafo(grafo)`: Mostra o mapa completo
- `exibir_rotas(grafo, rota_dist, rota_tempo)`: Compara rotas visualmente

**Recursos visuais:**
- Cores diferenciadas para cada algoritmo
- Legenda explicativa automática
- Exportação em alta resolução (150 DPI)
- Métricas exibidas no console

## 🔍 Comparação de Algoritmos

| Aspecto | Dijkstra | A* |
|---------|----------|-----|
| **Objetivo** | Menor distância | Menor tempo |
| **Peso** | `length` (metros) | `travel_time` (segundos) |
| **Heurística** | Não usa | Distância haversine / v_max |
| **Velocidade** | Explora mais nós | Mais direcionado ao destino |
| **Resultado** | Caminho mais curto | Caminho mais rápido |
| **Uso prático** | Economizar combustível | Chegar mais rápido |

## 🧪 Análise de Performance

O sistema fornece métricas detalhadas:
- **Distância total** (em metros e quilômetros)
- **Tempo estimado** (em segundos e minutos)
- **Número de nós no caminho** (quantidade de interseções)
- **Tempo de execução do algoritmo** (performance computacional)

Exemplo de saída:
```
--- Métricas ---
Dijkstra (distância) → 45 nós no caminho | 3250.50 m | 285.40 s
A* (tempo)           → 38 nós no caminho | 3580.20 m | 245.10 s
```

## ⚙️ Configurações e Personalização

### Ajustar Área de Download
No `main.py` ou scripts específicos, modifique:
```python
raio = 5000  # Raio em metros (5km)
```

### Modificar Velocidades Padrão
No `GrafoManager.py`, ajuste o dicionário:
```python
velocidades = {
    "motorway": 120,    # Altere conforme necessário
    "primary": 60,
    # ...
}
```

### Alterar Cores das Rotas
No `Visualizador.py`:
```python
route_colors=["red", "blue"]  # Dijkstra, A*
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

### Sugestões de Melhorias
- Implementar algoritmo de Bellman-Ford
- Adicionar suporte a múltiplos pontos de parada (TSP)
- Criar interface gráfica (GUI) com Tkinter/PyQt
- Implementar cache de grafos para downloads recorrentes
- Adicionar cálculo de consumo de combustível
- Suporte a diferentes perfis de veículos (carro, bicicleta, pedestre)

## 👥 Equipe

Projeto desenvolvido por estudantes como parte do Projeto Integrador.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📚 Referências

- **OSMnx Documentation:** https://osmnx.readthedocs.io/
- **NetworkX Documentation:** https://networkx.org/documentation/
- **OpenStreetMap:** https://www.openstreetmap.org/
- **CORMEN, T.H. et al.** *Algoritmos: Teoria e Prática*. 3ª edição.
- **ZIVIANI, N.** *Projeto de Algoritmos com Implementações em Pascal e C*
- **Hart, P. E.; Nilsson, N. J.; Raphael, B.** "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" (A* Algorithm)

## 🐛 Problemas Conhecidos e Soluções

### Erro ao baixar grafo
- Verifique sua conexão com a internet
- Reduza o raio de busca se a área for muito grande
- Certifique-se de que as coordenadas estão no formato correto

### Grafo não carrega
- Verifique se o arquivo `grafo_brasilia.graphml` existe
- Tente baixar o grafo novamente (opção 1 do menu)

### Rota não encontrada
- Verifique se origem e destino estão dentro da área do grafo
- Aumente o raio de download do mapa
- Certifique-se de que as coordenadas estão corretas

## 📧 Contato

Para dúvidas, sugestões ou contribuições:
- **Issues:** [https://github.com/Projeto-Integrador3B/Algoritmos-Mapas/issues](https://github.com/Projeto-Integrador3B/Algoritmos-Mapas/issues)
- **Pull Requests:** [https://github.com/Projeto-Integrador3B/Algoritmos-Mapas/pulls](https://github.com/Projeto-Integrador3B/Algoritmos-Mapas/pulls)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!**

🗺️ *Desenvolvido com Python, OSMnx e muito café* ☕
