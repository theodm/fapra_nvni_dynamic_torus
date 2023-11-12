import random
from typing import Literal

import networkx

from src.ranged_int.ranged_int import ClampedInt, OverflowInt
from src.torus_creation.shared.line_utils import nodes_between_overflow
from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


def create_random_2d_grid_network_information_lines(
    width: int,
    height: int,
    num_distinct_information: int,
    num_lines: int,
    information_lines: list[int],
    line_radius: int,
    line_radius_decrease_factor: int = 1,
    int_mode: Literal["clamped"] | Literal["overflow"] = "clamped",
) -> networkx.Graph:
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
        random_information = random.choice(information_lines)

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
                    create_int(random_information) - (i * line_radius_decrease_factor)
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
