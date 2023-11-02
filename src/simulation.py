# %%
from dataclasses import dataclass
import networkx
import random
from create import create_random_2d_grid_network, create_farbtupfer_2d_grid_network
from loguru import logger
from main import draw_torus
from typing import Deque, Literal
from collections import deque


class RandomWalker:
    # Wahrscheinlichkeit, dass der Random Walker einen zufälligen Schritt macht
    random_probability: float
    # Wahrscheinlichkeit, dass der Random Walker eine Kante hinzufügt
    random_probability_of_adding_edge: float = 0.005
    # Länge des Gedächtnisses
    length_of_memory: int = 150

    name: str
    g: networkx.Graph
    searched_information: int

    last_nodes: Deque[tuple]

    def __init__(
        self,
        name: str,
        g: networkx,
        searched_information: int,
        random_probability: float = 0.9,
        random_probability_of_adding_edge: float = 0.005,
        length_of_memory: int = 150,
    ):
        self.name = name
        self.g = g
        self.searched_information = searched_information
        self.random_probability = random_probability
        self.random_probability_of_adding_edge = random_probability_of_adding_edge
        self.length_of_memory = length_of_memory

        self.last_nodes = deque([], length_of_memory)

        # Zufälliger Startknoten
        self.last_nodes.appendleft(random.choice(list(self.g.nodes())))

        # logger.info(f"RandomWalker {self.name} started at {self.current_node}")

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

            # logger.debug(f"searched information: {self.searched_information}")
            # logger.debug(f"current node information: {current_node_information}")
            # logger.debug(f"neighbor informations: {[self.g.nodes[x]['information'] for x in sorted_neighbors]}")

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


def simulate(
    graph_strategy: Literal["random"] | Literal["farbtupfer"],
    grid_width: int,
    grid_height: int,
    num_distinct_information: int,
    num_random_walker: int,
    rw_random_probability: float,
    rw_random_probability_of_adding_edge: float,
    rw_length_of_memory: int,
    searched_information: int,
    max_steps: int,
):
    # Erstelle das Netzwerk
    if graph_strategy == "random":
        g = create_random_2d_grid_network(
            grid_width, grid_height
        )
    elif graph_strategy == "farbtupfer":
        g = create_farbtupfer_2d_grid_network(grid_width, grid_height)
    else:
        raise Exception("invalid graph strategy")

    # Erstelle die Random Walker
    random_walkers = []
    for i in range(num_random_walker):
        random_walkers.append(
            RandomWalker(
                f"Random Walker {i}",
                g,
                5,
                rw_random_probability,
                rw_random_probability_of_adding_edge,
                rw_length_of_memory,
            )
        )


    # Wie oft gibt es die gesuchte Information im Netzwerk?
    # Damit wir wissen, wann wir die Simulation beenden können.
    searched_information_count = 0
    for n in g.nodes():
        if g.nodes[n]["information"] == searched_information:
            searched_information_count += 1

    found_nodes = []

    step_to_number_of_found_nodes = {}

    # Führe die Simulation durch
    step = 1
    while True:
        edges_to_add = []
        for rw in random_walkers:
            edges_to_add_rw = rw.walk()
            
            for edge in edges_to_add_rw:
                if not g.has_edge(edge[0], edge[1]):
                    edges_to_add.append(edge)

            if len(edges_to_add_rw) > 0:
                logger.info(
                    f"[{step}]] {rw.name} added {edges_to_add_rw} to the graph"
                )

            edges_to_add.extend(edges_to_add_rw)

        # Neue Kanten fügen wir tatsächlich erst dann hinzu,
        # wenn alle Random Walker ihren Schritt gemacht haben
        for edge in edges_to_add:
            if not g.has_edge(edge[0], edge[1]):
                g.add_edge(edge[0], edge[1])

        for rw in random_walkers:
            # Wenn der Random Walker die gesuchte Information gefunden hat,
            # füge sie zu den gefundenen Knoten hinzu
            if (
                rw.g.nodes[rw.current_node()]["information"] == searched_information
                and rw.current_node() not in found_nodes
            ):
                found_nodes.append(rw.current_node())
                logger.info(f"[{step}] RandomWalker {rw.name} found the searched information at {rw.current_node()} [{len(found_nodes)}/{searched_information_count}]")

        # Speichere die Anzahl der gefundenen Knoten nach jedem Schritt
        step_to_number_of_found_nodes[step] = len(found_nodes)

        if len(found_nodes) == searched_information_count:
            break
            
        if step >= max_steps:
            break
            
        step += 1

    
    colors = [
        "#e6194b",
        "#3cb44b",
        "#ffe119",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#46f0f0",
        "#f032e6",
        "#bcf60c",
        "#fabebe",
    ]
    draw_torus(g, colors)

    # draw diagram with matplotlib
    import matplotlib.pyplot as plt

    plt.plot(
        list(step_to_number_of_found_nodes.keys()),
        list(step_to_number_of_found_nodes.values()),
    )
    pass

simulate(
    graph_strategy="random",
    grid_width=5,
    grid_height=10,
    num_distinct_information=10,
    num_random_walker=2,
    rw_random_probability=0.9,
    rw_random_probability_of_adding_edge=0.000,
    rw_length_of_memory=150,
    searched_information=5,
    max_steps=100000,)

# g = create_farbtupfer_2d_grid_network(100, 100)

# colors = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
#             "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe"]

# # draw_torus(g, colors)

# searched_information = 5

# # Wie oft gibt es die gesuchte Information im Netzwerk?
# searched_information_count = 0
# for n in g.nodes():
#     if g.nodes[n]['information'] == searched_information:
#         searched_information_count += 1

# # Random Walker erzeugen
# rw1 = RandomWalker("rw1", g, searched_information)

# found_nodes = []

# current_step = 1

# step_to_number_of_found_nodes = {}

# while len(found_nodes) < searched_information_count and current_step < 200000:
#     edges_to_add = rw1.walk()

#     # Füge die Kanten zu dem Graphen hinzu
#     if edges_to_add:
#         logger.info(f"[{current_step}]] Random Walker {rw1.name} added {edges_to_add} to the graph")
    
#         for edge in edges_to_add:
#             if not g.has_edge(edge[0], edge[1]):
#                 g.add_edge(edge[0], edge[1])

#     # Wenn der Random Walker die gesuchte Information gefunden hat,
#     # füge sie zu den gefundenen Knoten hinzu
#     if rw1.g.nodes[rw1.current_node()]['information'] == searched_information and rw1.current_node() not in found_nodes:
#         found_nodes.append(rw1.current_node())
#         #logger.info(f"[{current_step}] RandomWalker {rw1.name} found the searched information at {rw1.current_node()} [{len(found_nodes)}/{searched_information_count}]")
    
#     # Speichere die Anzahl der gefundenen Knoten nach jedem Schritt
#     step_to_number_of_found_nodes[current_step] = len(found_nodes)

#     current_step += 1

# draw_torus(g, colors)

# # draw diagram with matplotlib 
# import matplotlib.pyplot as plt

# plt.plot(list(step_to_number_of_found_nodes.keys()), list(step_to_number_of_found_nodes.values()))







# %%
