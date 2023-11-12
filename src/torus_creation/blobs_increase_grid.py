import random
from typing import Literal

import networkx

from src.ranged_int.ranged_int import ClampedInt, OverflowInt
from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


def create_random_2d_grid_network_constant_blob_increase(
    width: int,
    height: int,
    num_distinct_information: int,
    num_blobs: int,
    blob_radius: int,
    int_mode: Literal["clamped"] | Literal["overflow"] = "clamped",
) -> networkx.Graph:
    """
    Erstellt einen 2D-Gitter-Graphen mit relativ zufällig verteilten Informationen. Dabei wird ein Graph erstellt,
    in dem zusammengehörige Informationen auch nebeneinander liegen (in Clustern). Dabei wird die folgende Strategie verwendet:

    Zufällig werden Kreise mit einem bestimmten Radius auf dem Graphen erstellt (Blobs), welche die Informationen in diesem Bereich um
    einen bestimmten Betrag erhöhen. Dadurch entstehen Cluster, die sich überlappen können.

    Args:
        width (int): Die Breite des Graphen.
        height (int): Die Höhe des Graphen.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        num_blobs (int): Die Anzahl der Kreise (Blobs), die erstellt werden sollen.
        blob_radius (int): Der Radius der Kreise (Blobs), die erstellt werden sollen.
        int_mode (Literal["clamped"] | Literal["overflow"], optional): Soll eine Information bei erreichen von num_distinct_information
        dort bleibt und nicht weiter erhöht wird (clamped) oder soll sie dann wieder bei 0 anfangen (overflow). Defaults to "clamped".
    """
    g = networkx.grid_2d_graph(width, height, periodic=True)

    def create_int(value: int):
        if int_mode == "clamped":
            return ClampedInt(value, num_distinct_information)
        elif int_mode == "overflow":
            return OverflowInt(value, num_distinct_information)
        else:
            raise ValueError(f"Unknown int_mode: {int_mode}")

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]

        # Initiale Information ist 0
        g.nodes[node]["information"] = 0

    for j in range(num_blobs):
        random_node = random.choice(list(g.nodes()))

        nodes_already_visited = []

        nodes_to_visit_in_next_round = [random_node]
        for i in range(blob_radius):
            nodes_to_visit_this_round = nodes_to_visit_in_next_round.copy()
            nodes_to_visit_in_next_round = []

            for node in nodes_to_visit_this_round:
                nodes_already_visited.append(node)

                g.nodes[node]["information"] = int(
                    create_int(g.nodes[node]["information"]) + 1
                )

                for neighbor in g.neighbors(node):
                    if neighbor in nodes_already_visited:
                        continue
                    if neighbor in nodes_to_visit_in_next_round:
                        continue
                    if neighbor in nodes_to_visit_this_round:
                        continue

                    nodes_to_visit_in_next_round.append(neighbor)

    return g
