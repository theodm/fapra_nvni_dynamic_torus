import random
from collections import deque
from dataclasses import dataclass
from typing import Deque, Literal

import networkx

from src.search.strategy.shared_rw_utils import get_neigbor_with_nearest_information


@dataclass
class RandomWalker3StrategyParams:
    random_probability: float
    length_of_memory: int
    create_edge_strategy: str

    random_probability_to_create_edge: float = 1.0

class RandomWalker3:
    # Wahrscheinlichkeit, dass der Random Walker einen zufälligen Schritt macht
    random_probability: float
    # Länge des Gedächtnisses
    length_of_memory: int = 150
    # Strategie mit der Kanten erstellt werden
    create_edge_strategy: str

    name: str
    g: networkx.Graph
    searched_information: int
    start_point: tuple

    probability_to_create_edge: float
    random_probability_to_create_edge: float

    last_nodes: Deque[tuple]


    @classmethod
    def withParams(
        cls,
        name: str,
        g: networkx.Graph,
        searched_information: int,
        start_point: tuple,
        random_walker_params: RandomWalker3StrategyParams,
    ):
        return cls(
            name,
            g,
            searched_information,
            start_point,
            random_walker_params.random_probability,
            random_walker_params.length_of_memory,
            random_walker_params.create_edge_strategy,
            random_walker_params.random_probability_to_create_edge
        )

    def __init__(
        self,
        name: str,
        g: networkx,
        searched_information: int,
        start_point: tuple,
        random_probability: float,
        length_of_memory: int,
        create_edge_strategy: str,
        random_probability_to_create_edge: float
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information
        self.start_point = start_point

        self.random_probability = random_probability
        self.length_of_memory = length_of_memory
        self.create_edge_strategy = create_edge_strategy
        self.random_probability_to_create_edge = random_probability_to_create_edge

        self.last_nodes = deque([], length_of_memory)

        # Zufälliger Startknoten
        self.last_nodes.appendleft(start_point)
        #self.last_nodes_without_current = deque([], length_of_memory - 1)

        # logger.info(f"RandomWalker {self.name} started at {self.current_node}")

    def current_node(self):
        return self.last_nodes[0]

    def walk(self) -> list[tuple]:
        # Don't visit nodes in history
        current_node = self.current_node()

        neighbor_list = list(self.g.neighbors(current_node))

        # Performance: Set statt Liste (O(1) statt O(n))
        last_nodes_set = set(self.last_nodes)
        possible_nodes = set(neighbor_list) - last_nodes_set

        # Wenn wir keine Nachbarn haben, die nicht schon besucht wurden,
        # dann müssen wir halt einen besuchen, den wir schon besucht haben.
        if len(possible_nodes) == 0:
            possible_nodes = neighbor_list

        # Zufälliger Schritt
        if random.random() < self.random_probability:
            next_node = random.choice(list(possible_nodes))
        else:
            next_node = get_neigbor_with_nearest_information(
                self.g, current_node, self.searched_information, possible_nodes
            )

        self.last_nodes.appendleft(next_node)

        if random.random() > self.random_probability_to_create_edge:
            return []

        current_node = self.current_node()

        _last_nodes_without_current = [node for node in self.last_nodes if node != current_node]
        #_last_nodes_without_current_set = self.last_nodes_without_current
        try:
            if self.create_edge_strategy == "dynamic_similar_to_searched":
                # connect current node with the nearest distance node to searched information in the memory
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.searched_information))

                return [(current_node, _last_nodes_without_current_sorted_by_dist[0])]

            elif self.create_edge_strategy == "dynamic_least_similar_to_searched":
                # connect current node with the highest distance node to searched information in the memory
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.searched_information))

                return [(current_node, _last_nodes_without_current_sorted_by_dist[-1])]

            elif self.create_edge_strategy == "dynamic_similar":
                # connect current node with the nearest information node to current node
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.g.nodes[
                    current_node]["information"]))

                return [(current_node, _last_nodes_without_current_sorted_by_dist[0])]
            elif self.create_edge_strategy == "dynamic_random":
                # connect current node with a random node in the memory
                return [(current_node, random.choice(_last_nodes_without_current))]


            raise Exception("Unknown create_edge_strategy " + self.create_edge_strategy)
        finally:
            #self.last_nodes_without_current.appendleft(current_node)
            pass





