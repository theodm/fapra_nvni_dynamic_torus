import networkx
import random

from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


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
