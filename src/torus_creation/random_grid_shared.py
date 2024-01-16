import networkx as nx
import numpy as np
import plotly.graph_objects as go
import random

from scipy import stats

from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus

def _add_random_edge(graph, node, width, height):
    node_x, node_y = node

    distances = [
        sum(
            [
                min(abs(other_node_x - node_x), width - abs(other_node_x - node_x)) ** 2,  
                min(abs(other_node_y - node_y), height - abs(other_node_y - node_y)) ** 2, 
            ]
        )
        + 1e-6
        for other_node_x, other_node_y in graph.nodes() - node
    ]

    probabilities = np.reciprocal(distances)
    probabilities /= np.sum(probabilities)

    v = random.choices(list(graph.nodes()), weights=probabilities, k=1)[0]

    graph.add_edge(node, v)


def _add_random_edges_to_all_nodes(graph, width, height, p = 1.0):
    sorted_nodes = sorted(graph.nodes(), key=lambda x: (x[1], x[0]))

    for node in sorted_nodes:
        if random.random() < p:
            _add_random_edge(graph, node, width, height)
    
    graph.remove_edges_from(nx.selfloop_edges(graph))

def _add_random_normal_information_to_all_nodes(g, width, height, num_distinct_information, mean, std_dev):
    # Hier wird die truncated Standardverteilung verwendet, da wir nur Werte zwischen 0 und num_distinct_information - 1
    # haben wollen. (siehe https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html
    lower = 0
    upper = num_distinct_information - 1

    mu = mean if mean else (num_distinct_information / 2 - 1)
    sigma = std_dev if std_dev else num_distinct_information / 8

    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

    # Wir erstellen die Zufallswerte vorab,
    # dann verwenden wir sie
    random_information = X.rvs(width * height).tolist()

    for node in g.nodes():
        # Zufällige Information
        g.nodes[node]["information"] = int(random_information.pop())

def _add_random_information_to_all_nodes(g, num_distinct_information):
    for node in g.nodes():
        # Zufällige Information
        g.nodes[node]["information"] = random.randrange(0, num_distinct_information)

    return g


def sh_create_random_2d_grid_network(
    width: int, 
    height: int,
    num_distinct_information: int,
    small_world: bool
) -> nx.Graph:
    """
    Erstellt einen Graphen in Form eines Netzes mit den angegebenen Höhen- und Breitenmaßen. Dabei
    erhalten die Knoten zufällige Informationen zwischen 1 und 10. Die Koordinaten der Knoten in einem Torus
    werden als Attribut gespeichert.

    Wenn small_world=True, dann werden zufällige Kanten zwischen allen Knoten hinzugefügt. (Kleinberg-Modell)

    Args:
        height (int): Die Höhe des Torus.
        width (int): Die Breite des Torus.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        small_world (bool): Wenn True, dann werden zufällige Kanten zwischen allen Knoten hinzugefügt. (Kleinberg-Modell)

    Returns:
        networkx.Graph: Der erstellte Graph.
    """

    g = nx.grid_2d_graph(width, height, periodic=True)

    _add_random_information_to_all_nodes(g, num_distinct_information)

    if small_world:
        _add_random_edges_to_all_nodes(g, width, height, p)

    return g

def sh_create_random_normal_2d_grid_network(
    width: int, 
    height: int,
    num_distinct_information: int,
    mean: float,
    std_dev: float,
    small_world: bool
) -> nx.Graph:
    """
    Erstellt einen Graphen in Form eines Netzes mit den angegebenen Höhen- und Breitenmaßen. Dabei
    erhalten die Knoten zufällige Informationen zwischen 1 und 10. Die Koordinaten der Knoten in einem Torus
    werden als Attribut gespeichert.

    Wenn small_world=True, dann werden zufällige Kanten zwischen allen Knoten hinzugefügt. (Kleinberg-Modell)

    Args:
        height (int): Die Höhe des Torus.
        width (int): Die Breite des Torus.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        mean (float): Der Mittelwert der normalverteilten Zufallswerte.
        std_dev (float): Die Standardabweichung der normalverteilten Zufallswerte.
        small_world (bool): Wenn True, dann werden zufällige Kanten zwischen allen Knoten hinzugefügt. (Kleinberg-Modell)

    Returns:
        networkx.Graph: Der erstellte Graph.
    """

    g = nx.grid_2d_graph(width, height, periodic=True)

    _add_random_normal_information_to_all_nodes(g, width, height, num_distinct_information, mean, std_dev)

    if small_world:
        _add_random_edges_to_all_nodes(g, width, height)

    return g

