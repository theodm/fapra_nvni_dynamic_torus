
from dataclasses import dataclass
import random
from typing import Deque

from loguru import logger
import networkx


@dataclass
class OnlyRandomWalkerStrategyParams:
    pass

class OnlyRandomWalker:
    '''
    Dieser Random Walker macht nur zufällige Schritte und dient nur zum Vergleichen. Er erstellt
    auch niemals neue Kanten und verändert den Graphen nicht.
    '''
    name: str
    g: networkx.Graph
    searched_information: int

    _current_node: tuple

    @classmethod
    def withParams(
        cls,
        name: str,
        g: networkx.Graph,
        searched_information: int,
        random_walker_params: OnlyRandomWalkerStrategyParams,
    ):
        return cls(
            name,
            g,
            searched_information
        )

    def __init__(
        self,
        name: str,
        g: networkx,
        searched_information: int
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information

        # Zufälliger Startknoten
        self._current_node = random.choice(list(self.g.nodes()))

        logger.trace(f"RandomWalker {self.name} started at {self.current_node}")

    def current_node(self):
        return self._current_node

    def walk(self) -> list[tuple]:
        # Zufälliger Schritt
        self._current_node = random.choice(list(self.g.neighbors(self._current_node)))

        # Kein Rückgabewert, dieser Random Walker gibt niemals
        # eine neue Kante zurück. Er dient nur zum Vergleichen.
        return []