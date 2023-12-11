import random
from typing import Literal

import networkx

from ranged_int.ranged_int import ClampedInt, OverflowInt
from torus_creation.shared.line_utils import nodes_between_overflow
from torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


def create_random_2d_grid_network_constant_lines_increase(
    width: int,
    height: int,
    num_distinct_information: int,
    num_lines: int,
    line_radius: int,
    int_mode: Literal["clamped"] | Literal["overflow"] = "clamped",
) -> networkx.Graph:
    """
    Erstellt einen 2D-Gitter-Graphen mit relativ zufällig verteilten Informationen. Dabei wird ein Graph erstellt,
    in dem zusammengehörige Informationen auch nebeneinander liegen (in Clustern). Dabei wird die folgende Strategie verwendet:

    Die Strategie ist wie bei create_random_2d_grid_network_constant_blob_increase, nur dass hier statt
    einem Ausgangspunkt für einen Kreis (Blob) eine ganze Linie von einem Knoten zu einem anderen inkrementiert wird.

    Args:
        width (int): Die Breite des Graphen.
        height (int): Die Höhe des Graphen.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        num_lines (int): Die Anzahl der Linien, die erstellt werden sollen.
        line_radius (int): Der Radius der Linien, die erstellt werden sollen.
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

    for j in range(num_lines):
        random_node_begin = random.choice(list(g.nodes()))
        random_node_end = random.choice(
            list([x for x in g.nodes() if x != random_node_begin])
        )

        # Calculate nodes between random_node_begin and random_node_end with scikit-image
        # skimage.draw.line

        nodes_already_visited = []

        nodes_to_visit_in_next_round = nodes_between_overflow(
            random_node_begin, random_node_end, width, height
        )

        for i in range(line_radius):
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
