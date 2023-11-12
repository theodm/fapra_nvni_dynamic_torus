import random
from typing import Literal

import networkx

from src.ranged_int.ranged_int import ClampedInt, OverflowInt
from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


def find_increase_path_with_overflow(
    target_information: int,
    current_information: int,
    num_distinct_information: int,
) -> int:
    if current_information == target_information:
        return 0

    target_a = target_information

    if current_information < target_information:
        target_b = target_information - num_distinct_information
    else:
        target_b = target_information + num_distinct_information

    diff_a = abs(current_information - target_a)
    diff_b = abs(current_information - target_b)

    if diff_a < diff_b:
        return 1 if current_information < target_a else -1
    else:
        return 1 if current_information < target_b else -1


class RandomWalker:
    current_node: tuple[int, int]
    target_information: int
    radius_min: int
    radius_max: int
    target_information: int
    special_radius_min: int
    special_radius_max: int
    num_distinct_information: int
    int_mode: Literal["clamped"] | Literal["overflow"] = "clamped"

    increase_multiplier: int
    special_probability: float
    is_greedy: bool

    def __init__(
        self,
        start_node: tuple[int, int],
        radius_min: int,
        radius_max: int,
        target_information: int,
        special_radius_min: int,
        special_radius_max: int,
        num_distinct_information: int,
        increase_multiplier: int,
        special_probability: float,
        int_mode: Literal["clamped"] | Literal["overflow"],
        is_greedy: bool,
    ):
        self.current_node = start_node

        self.radius_min = radius_min
        self.radius_max = radius_max
        self.target_information = target_information
        self.special_radius_min = special_radius_min
        self.special_radius_max = special_radius_max
        self.num_distinct_information = num_distinct_information
        self.int_mode = int_mode
        self.increase_multiplier = increase_multiplier
        self.special_probability = special_probability
        self.is_greedy = is_greedy

    def step(self, g: networkx.Graph):
        # sort nearest neighbor by difference to current information
        nearest_neighbors = sorted(
            g.neighbors(self.current_node),
            key=lambda x: abs(g.nodes[x]["information"] - self.target_information),
        )

        if self.is_greedy:
            rand = random.random()
            if rand < 0.5:
                self.current_node = nearest_neighbors[-1]
            elif rand < 0.75:
                self.current_node = nearest_neighbors[-2]
            elif rand < 0.875:
                self.current_node = nearest_neighbors[-3]
            else:
                self.current_node = nearest_neighbors[-4]
        else:
            self.current_node = random.choice(nearest_neighbors)

        def create_int(value: int):
            if self.int_mode == "clamped":
                return ClampedInt(value, self.num_distinct_information)
            elif self.int_mode == "overflow":
                return OverflowInt(value, self.num_distinct_information)
            else:
                raise ValueError(f"Unknown int_mode: {self.int_mode}")

        radius = random.randint(self.radius_min, self.radius_max)

        # if special
        if random.random() < self.special_probability:
            radius = random.randint(self.special_radius_min, self.special_radius_max)

        nodes_already_visited = []

        nodes_to_visit_in_next_round = [self.current_node]
        for i in range(radius):
            nodes_to_visit_this_round = nodes_to_visit_in_next_round.copy()
            nodes_to_visit_in_next_round = []

            for node in nodes_to_visit_this_round:
                nodes_already_visited.append(node)

                if self.int_mode == "clamped":
                    if g.nodes[node]["information"] < self.target_information:
                        g.nodes[node]["information"] = int(
                            create_int(g.nodes[node]["information"])
                            + random.randint(1, self.increase_multiplier)
                        )
                    elif g.nodes[node]["information"] > self.target_information:
                        g.nodes[node]["information"] = int(
                            create_int(g.nodes[node]["information"])
                            - random.randint(1, self.increase_multiplier)
                        )
                else:
                    g.nodes[node]["information"] = int(
                        create_int(self.target_information)
                        + (
                            find_increase_path_with_overflow(
                                self.target_information,
                                g.nodes[node]["information"],
                                self.num_distinct_information,
                            )
                            * random.randint(1, self.increase_multiplier)
                        )
                    )

                for neighbor in g.neighbors(node):
                    if neighbor in nodes_already_visited:
                        continue
                    if neighbor in nodes_to_visit_in_next_round:
                        continue
                    if neighbor in nodes_to_visit_this_round:
                        continue

                    nodes_to_visit_in_next_round.append(neighbor)


def create_random_2d_grid_random_walkers(
    width: int,
    height: int,
    num_distinct_information: int,
    num_random_walkers: int,
    num_steps: int,
    radius_min: int = 3,
    radius_max: int = 5,
    special_radius_min: int = 10,
    special_radius_max: int = 20,
    int_mode: Literal["clamped"] | Literal["overflow"] = "clamped",
    increase_multiplier: int = 3,
    special_probability: float = 0.005,
    random_start_location: bool = True,
    greedy_quote: float = 0.75,
) -> networkx.Graph:
    g = networkx.grid_2d_graph(width, height, periodic=True)

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]

        if random_start_location:
            # Zufällige Information
            g.nodes[node]["information"] = random.randrange(0, num_distinct_information)
        else:
            g.nodes[node]["information"] = 0

    random_walkers = []
    for i in range(num_random_walkers):
        random_node = random.choice(list(g.nodes()))
        random_walkers.append(
            RandomWalker(
                random_node,
                radius_min,
                radius_max,
                random.randrange(0, num_distinct_information),
                special_radius_min,
                special_radius_max,
                num_distinct_information,
                increase_multiplier,
                special_probability,
                int_mode,
                random.random() < greedy_quote,
            )
        )

    for i in range(num_steps):
        for walker in random_walkers:
            walker.step(g)

    return g
