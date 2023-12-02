from dataclasses import dataclass

import networkx
import random

from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus
import scipy.stats as stats
from loguru import logger


@dataclass
class RandomStrategyParams:
    # Keine Parameter
    pass


@dataclass
class RandomNormalStrategyParams:
    mean: float
    std_dev: float

    @staticmethod
    def default(num_distinct_information: int):
        return RandomNormalStrategyParams(
            mean=num_distinct_information / 2 - 1,
            std_dev=num_distinct_information / 8,
        )

    pass


def create_random_2d_grid_network_normal_with_params(
    width: int,
    height: int,
    num_distinct_information: int,
    params: RandomNormalStrategyParams,
) -> networkx.Graph:
    return create_random_2d_grid_network_normal(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
        mean=params.mean,
        std_dev=params.std_dev,
    )


def create_random_2d_grid_network_normal(
    width: int,
    height: int,
    num_distinct_information: int,
    mean: float,
    std_dev: float,
) -> networkx.Graph:
    """
    Erstellt einen Graphen in Form eines Netzes mit den angegebenen Höhen- und Breitenmaßen. Dabei
    erhalten die Knoten zufällige Informationen zwischen 1 und 10. Die Koordinaten der Knoten in einem Torus
    werden als Attribut gespeichert.

    Args:
        height (int): Die Höhe des Torus.
        width (int): Die Breite des Torus.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.

    Returns:
        networkx.Graph: Der erstellte Graph.
    """

    g = networkx.grid_2d_graph(width, height, periodic=True)

    # Hier wird die truncated Standardverteilung verwendet, da wir nur Werte zwischen 0 und num_distinct_information - 1
    # haben wollen. (siehe https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html
    lower = 0
    upper = num_distinct_information - 1

    mu = mean if mean else (num_distinct_information / 2 - 1)
    sigma = std_dev if std_dev else num_distinct_information / 8

    logger.debug("mu: {mu}, sigma: {sigma}", mu=mu, sigma=sigma)

    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

    # Wir erstellen die Zufallswerte vorab,
    # dann verwenden wir sie
    random_information = X.rvs(width * height).tolist()

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]

        # Zufällige Information
        g.nodes[node]["information"] = int(random_information.pop())

    return g


def create_random_2d_grid_network_with_params(
    width: int,
    height: int,
    num_distinct_information: int,
    params: RandomStrategyParams,
) -> networkx.Graph:
    return create_random_2d_grid_network(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
    )


def create_random_2d_grid_network(
    width: int, height: int, num_distinct_information: int
) -> networkx.Graph:
    """
    Erstellt einen Graphen in Form eines Netzes mit den angegebenen Höhen- und Breitenmaßen. Dabei
    erhalten die Knoten zufällige Informationen zwischen 1 und 10. Die Koordinaten der Knoten in einem Torus
    werden als Attribut gespeichert.

    Args:
        height (int): Die Höhe des Torus.
        width (int): Die Breite des Torus.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.

    Returns:
        networkx.Graph: Der erstellte Graph.
    """

    g = networkx.grid_2d_graph(width, height, periodic=True)

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]

        # Zufällige Information
        g.nodes[node]["information"] = random.randrange(0, num_distinct_information)

    return g
