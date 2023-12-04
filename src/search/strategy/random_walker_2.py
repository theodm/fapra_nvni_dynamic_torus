import random
from collections import deque
from dataclasses import dataclass
from typing import Deque, Literal

import networkx

from src.search.strategy.shared_rw_utils import get_neigbor_with_nearest_information


@dataclass
class RandomWalker2StrategyParams:
    random_probability: float
    length_of_memory: int
    create_edge_strategy: Literal["OnlySearchedInformation"] | Literal["EveryXStepsLowestDistanceToSearchedInformation"] | Literal["EveryXStepsHighestDistanceToSearchedInformation"] | Literal["EveryXStepsToNearestToCurrentInformation"] | Literal["EveryXStepsRandomConnection"]

    # Only for EveryRandomStepsNearestToCurrentInformation and EveryRandomStepsLowestDistanceToSearchedInformation
    probability_to_create_edge: float = 1.0

class RandomWalker2:
    # Wahrscheinlichkeit, dass der Random Walker einen zufälligen Schritt macht
    random_probability: float
    # Länge des Gedächtnisses
    length_of_memory: int = 150
    # Strategie mit der Kanten erstellt werden
    create_edge_strategy: Literal["OnlySearchedInformation"] | Literal["EveryXStepsLowestDistanceToSearchedInformation"] | Literal["EveryXStepsHighestDistanceToSearchedInformation"] | Literal["EveryXStepsToNearestToCurrentInformation"] | Literal["EveryXStepsRandomConnection"]

    name: str
    g: networkx.Graph
    searched_information: int
    start_point: tuple

    probability_to_create_edge: float

    last_nodes: Deque[tuple]

    number_of_steps = 0

    @classmethod
    def withParams(
        cls,
        name: str,
        g: networkx.Graph,
        searched_information: int,
        start_point: tuple,
        random_walker_params: RandomWalker2StrategyParams,
    ):
        return cls(
            name,
            g,
            searched_information,
            start_point,
            random_walker_params.random_probability,
            random_walker_params.length_of_memory,
            random_walker_params.create_edge_strategy,
            random_walker_params.probability_to_create_edge
        )

    def __init__(
        self,
        name: str,
        g: networkx,
        searched_information: int,
        start_point: tuple,
        random_probability: float,
        length_of_memory: int,
        create_edge_strategy:  Literal["OnlySearchedInformation"] | Literal["EveryXStepsLowestDistanceToSearchedInformation"] | Literal["EveryXStepsHighestDistanceToSearchedInformation"] | Literal["EveryXStepsToNearestToCurrentInformation"] | Literal["EveryXStepsRandomConnection"],
        probability_to_create_edge: float
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information
        self.start_point = start_point

        self.random_probability = random_probability
        self.length_of_memory = length_of_memory
        self.create_edge_strategy = create_edge_strategy
        self.probability_to_create_edge = probability_to_create_edge

        self.last_nodes = deque([], length_of_memory)

        # Zufälliger Startknoten
        self.last_nodes.appendleft(start_point)

        # logger.info(f"RandomWalker {self.name} started at {self.current_node}")

    def current_node(self):
        return self.last_nodes[0]

    def walk(self) -> list[tuple]:
        # Don't visit nodes in history
        possible_nodes = list(self.g.neighbors(self.current_node()))
        possible_nodes = [node for node in possible_nodes if node not in self.last_nodes]

        # Wenn wir keine Nachbarn haben, die nicht schon besucht wurden,
        # dann müssen wir halt einen besuchen, den wir schon besucht haben.
        if len(possible_nodes) == 0:
            possible_nodes = list(self.g.neighbors(self.current_node()))

        # Zufälliger Schritt
        if random.random() < self.random_probability:
            next_node = random.choice(possible_nodes)
        else:
            next_node = get_neigbor_with_nearest_information(
                self.g, self.current_node(), self.searched_information
            )

        self.last_nodes.appendleft(next_node)
        self.number_of_steps += 1

        if self.create_edge_strategy == "OnlySearchedInformation":            
            # Wenn wir nun bei der gesuchten Information angekommen sind, dann
            # verbinden wir den aktuellen Knoten mit allen Knoten im Gedächtnis,
            # der auch die gesuchte Information hat. (Falls die Kante bereits existiert,
            # wird sie ohnehin nicht nochmal eingefügt.)
            if self.g.nodes[next_node]["information"] == self.searched_information:
                edges_to_add = []

                for node in self.last_nodes:
                    if node == self.current_node():
                        continue

                    if self.g.nodes[node]["information"] != self.searched_information:
                        continue

                    edges_to_add.append((self.current_node(), node))

                return edges_to_add
            return []
        elif self.create_edge_strategy == "EveryXStepsLowestDistanceToSearchedInformation":            
            X = self.length_of_memory
            if self.number_of_steps > 0 and self.number_of_steps % X == 0:
                # connect current node with the nearest distance node to searched information in the memory
                _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.searched_information))

                return [(self.current_node(), _last_nodes_without_current_sorted_by_dist[0])]

            return []
        elif self.create_edge_strategy == "EveryXStepsHighestDistanceToSearchedInformation":            
            X = self.length_of_memory
            if self.number_of_steps > 0 and self.number_of_steps % X == 0:
                # connect current node with the highest distance node to searched information in the memory
                _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.searched_information))

                return [(self.current_node(), _last_nodes_without_current_sorted_by_dist[-1])]

            return []
        elif self.create_edge_strategy == "EveryXStepsToNearestToCurrentInformation":            
            X = self.length_of_memory
            if self.number_of_steps > 0 and self.number_of_steps % X == 0:
                # connect current node with the nearest information node to current node
                _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]
                _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.g.nodes[self.current_node()]["information"]))

                return [(self.current_node(), _last_nodes_without_current_sorted_by_dist[0])]

            return []
        elif self.create_edge_strategy == "EveryXStepsRandomConnection":            
            X = self.length_of_memory
            if self.number_of_steps > 0 and self.number_of_steps % X == 0:
                # connect current node with a random node in the memory
                _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]

                return [(self.current_node(), random.choice(_last_nodes_without_current))]

            return []
        elif self.create_edge_strategy == "EveryRandomStepsNearestToCurrentInformation":
            if not random.random() < self.probability_to_create_edge:
                return []

            # connect current node with the nearest information node to current node
            _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]
            _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.g.nodes[self.current_node()]["information"]))

            return [(self.current_node(), _last_nodes_without_current_sorted_by_dist[0])]
        elif self.create_edge_strategy == "EveryRandomStepsLowestDistanceToSearchedInformation":
            if not random.random() < self.probability_to_create_edge:
                return []

            # connect current node with the nearest distance node to searched information in the memory
            _last_nodes_without_current = [node for node in self.last_nodes if node != self.current_node()]
            _last_nodes_without_current_sorted_by_dist = sorted(_last_nodes_without_current, key=lambda node: abs(self.g.nodes[node]["information"] - self.searched_information))

            return [(self.current_node(), _last_nodes_without_current_sorted_by_dist[0])]


            
        raise Exception("Unknown create_edge_strategy " + self.create_edge_strategy)






