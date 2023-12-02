from collections import deque
from dataclasses import dataclass
import random
from typing import Deque

from loguru import logger
import networkx


@dataclass
class OnlyRandomWalkerStrategyParams:
    length_of_memory: int = 1
    pass


class OnlyRandomWalker:
    """
    Dieser Random Walker macht zufällige Schritte und hat ein Gedächtnis von
    Knoten, welche er versucht zu vermeiden. Er erstellt
    niemals neue Kanten und verändert den Graphen nicht.
    """

    name: str
    g: networkx.Graph
    searched_information: int

    length_of_memory: int

    last_nodes: Deque[tuple]

    @classmethod
    def withParams(
        cls,
        name: str,
        g: networkx.Graph,
        searched_information: int,
        random_walker_params: OnlyRandomWalkerStrategyParams,
    ):
        return cls(name, g, searched_information, random_walker_params.length_of_memory)

    def __init__(
        self, name: str, g: networkx, searched_information: int, length_of_memory: int
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information
        self.length_of_memory = length_of_memory

        self.last_nodes = deque([], length_of_memory)

        # Zufälliger Startknoten
        self.last_nodes.appendleft(random.choice(list(self.g.nodes())))

        logger.trace(f"RandomWalker {self.name} started at {self.current_node}")

    def current_node(self):
        return self.last_nodes[0]

    def walk(self) -> list[tuple]:
        # Don't visit nodes in history
        possible_nodes = list(self.g.neighbors(self.current_node()))
        possible_nodes = [
            node for node in possible_nodes if node not in self.last_nodes
        ]

        # Wenn wir keine Nachbarn haben, die nicht schon besucht wurden,
        # dann müssen wir halt einen besuchen, den wir schon besucht haben.
        if len(possible_nodes) == 0:
            possible_nodes = list(self.g.neighbors(self.current_node()))

        next_node = random.choice(possible_nodes)

        self.last_nodes.appendleft(next_node)

        # Kein Rückgabewert, dieser Random Walker gibt niemals
        # eine neue Kante zurück. Er dient nur zum Vergleichen.
        return []
