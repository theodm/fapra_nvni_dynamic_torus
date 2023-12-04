from dataclasses import dataclass
import networkx
import random
from loguru import logger
from typing import Deque, Literal
from collections import deque

@dataclass
class RandomWalker1StrategyParams:
    random_probability: float
    random_probability_of_adding_edge: float
    length_of_memory: int

class RandomWalker1:
    # Wahrscheinlichkeit, dass der Random Walker einen zufälligen Schritt macht
    random_probability: float
    # Wahrscheinlichkeit, dass der Random Walker eine Kante hinzufügt
    random_probability_of_adding_edge: float = 0.005
    # Länge des Gedächtnisses
    length_of_memory: int = 150

    name: str
    g: networkx.Graph
    searched_information: int
    start_point: tuple

    last_nodes: Deque[tuple]

    @classmethod
    def withParams(
        cls,
        name: str,
        g: networkx.Graph,
        searched_information: int,
        start_point: tuple,
        random_walker_params: RandomWalker1StrategyParams,
    ):
        return cls(
            name,
            g,
            searched_information,
            start_point,
            random_walker_params.random_probability,
            random_walker_params.random_probability_of_adding_edge,
            random_walker_params.length_of_memory,
        )

    def __init__(
        self,
        name: str,
        g: networkx,
        searched_information: int,
        start_point: tuple,
        random_probability: float = 0.9,
        random_probability_of_adding_edge: float = 0.005,
        length_of_memory: int = 150,
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information
        self.start_point = start_point

        self.random_probability = random_probability
        self.random_probability_of_adding_edge = random_probability_of_adding_edge
        self.length_of_memory = length_of_memory

        self.last_nodes = deque([], length_of_memory)

        # Zufälliger Startknoten
        self.last_nodes.appendleft(start_point)

        logger.info(f"RandomWalker {self.name} started at {self.current_node}")

    def current_node(self):
        return self.last_nodes[0]

    def walk(self) -> list[tuple]:
        last_node = self.current_node()

        # Wenn ein Zufallswert erreicht ist, dann gehe zu einem zufälligen Knoten
        # ansonsten gehe zum Knoten, der die kleinste Differenz zur gesuchten Information hat
        if random.random() < self.random_probability:
            r = True

            # Wähle zufälligen Nachbarn
            self.last_nodes.appendleft(
                random.choice(list(self.g.neighbors(self.current_node())))
            )
        else:
            r = False

            # Wähle Nachbarn mit der kleinsten Differenz zur gesuchten Information
            current_node_information = self.g.nodes[self.current_node()]["information"]

            # Sortiere Nachbarn nach Differenz zur gesuchten Information
            sorted_neighbors = sorted(
                self.g.neighbors(self.current_node()),
                key=lambda x: abs(
                    self.g.nodes[x]["information"] - self.searched_information
                ),
            )

            logger.debug(f"searched information: {self.searched_information}")
            logger.debug(f"current node information: {current_node_information}")
            logger.debug(f"neighbor informations: {[self.g.nodes[x]['information'] for x in sorted_neighbors]}")

            # Wähle den ersten Nachbarn aus der Liste
            self.last_nodes.appendleft(sorted_neighbors[0])

        # logger.info(f"RandomWalker {self.name} walked from {last_node} [{self.g.nodes[last_node]['information']}] to {self.current_node} [{self.g.nodes[self.current_node]['information']}] (random: {r})")

        if random.random() < self.random_probability_of_adding_edge:
            # Wir verbinden die beiden Knoten in unserem Gedächtnis, die am nächsten zu unserer gesuchten Information liegen
            # Sortiere Gedächtnis nach Differenz zur gesuchten Information

            shuffled_last_nodes = list(self.last_nodes)

            random.shuffle(shuffled_last_nodes)
            sorted_last_nodes = sorted(
                shuffled_last_nodes,
                key=lambda x: abs(
                    self.g.nodes[x]["information"] - self.searched_information
                ),
            )

            if (
                sorted_last_nodes[0] == sorted_last_nodes[1]
                and sorted_last_nodes[0] != 5
            ):
                return []

            # logger.debug(f"sorted last nodes: {sorted_last_nodes}")
            return [(sorted_last_nodes[0], sorted_last_nodes[1])]

        return []