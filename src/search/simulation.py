
from dataclasses import dataclass
import networkx
import random
from loguru import logger
from src.plot.draw_torus import draw_torus_2d
from src.search.strategy.random_walker_1 import RandomWalker1, RandomWalker1StrategyParams
from typing import Deque, Literal

from src.torus_creation.random_grid import create_random_2d_grid_network
import plotly.graph_objects as go

#define graph types (random) for typings
GraphStrategy = Literal["random"]

# define Graph strategy mapping
graph_strategy_mapping = {
    "random": create_random_2d_grid_network
}

RandomWalkerStrategy = Literal["random_walker_1"]
# define Random Walker strategy mapping
random_walker_strategy_mapping = {
    "random_walker_1": RandomWalker1
}

RandomWalkerStrategyParams = RandomWalker1StrategyParams


def count_searched_information_in_graph(g: networkx.Graph, searched_information: int):
    count = 0

    for n in g.nodes():
        if g.nodes[n]["information"] == searched_information:
            count += 1

    return count

def simulate(
    # Grundsätzliche Strategie um den Graphen / Torus 
    # zu erstellen (wie werden die Informationen darauf verteilt)
    graph_strategy: GraphStrategy,

    # Größe des Graphen / Torus
    grid_width: int,
    grid_height: int,

    # Anzahl der unterschiedlichen Informationen 
    # die auf dem Graphen / Torus verteilt werden
    num_distinct_information: int,
    
    random_walker_strategy: RandomWalkerStrategy,
    random_walker_strategy_params: RandomWalkerStrategyParams,

    num_random_walker: int,
    
    searched_information: int,
    max_steps: int,
):
    # Die jeweiligen Funktionen zum Erstellen des Graphen und der Random Walker,
    # später müssen wir sie nurnoch nutzen.
    fn_graph_strategy = graph_strategy_mapping[graph_strategy]
    fn_random_walker_strategy = random_walker_strategy_mapping[random_walker_strategy]

    if not fn_random_walker_strategy:
        raise Exception("invalid random walker strategy: " + random_walker_strategy)
    
    if not fn_graph_strategy:
        raise Exception("invalid graph strategy: " + graph_strategy)

    g = fn_graph_strategy(
        grid_width, grid_height, num_distinct_information
    )

    # Wir wollen zunächst herausfinden, wieviele der gesuchten Informationen
    # es im Netzwerk überhaupt gibt. Denn dann brechen wir den Lauf vorzeitig
    # ab, wenn alle gefunden wurden.
    searched_information_count = count_searched_information_in_graph(g, searched_information)

    # Erstelle die Random Walker    
    random_walkers = []
    for i in range(num_random_walker):
        random_walkers.append(
            fn_random_walker_strategy.withParams(
                f"RW{i}",
                g,
                searched_information,
                random_walker_strategy_params
            )
        )

    # Mapping von dem Schritt der Simulation 
    # zu der bis zu diesem Zeitpunkt gefundenen Anzahl an Knoten
    # damit können wir später ein hübesches Diagramm erstellen
    step_to_number_of_found_nodes = {}

    # Bereits gefundene Knoten
    found_nodes = []

    # Führe die Simulation durch und
    # starten mit dem ersten Simulationsschritt (hier wird nicht mit 0 begonnen)
    step = 1
    while True:
        # Wir lassen erst jeden Random Walker seinen Schritt machen
        # und danach werden wir die neuen Kanten, die er nach dem Schritt
        # erstellen möchte hinzufügen. Damit vermeiden wir das ein Random Walker
        # eine Kante besucht, die im gleichen Schritt (durch einen anderen Random Walker)
        # erstellt wurde.
        edges_to_add = []

        for rw in random_walkers:
            edges_to_add_rw = rw.walk()
            
            # Bestehende Kanten nehmen wir nicht an und
            # ignorieren entsprechende Aufforderungen zum hinzufügen.
            for edge in edges_to_add_rw:
                if not g.has_edge(edge[0], edge[1]):
                    edges_to_add.append(edge)

            # Wenn nach der Dublettenprüfung tatsächlich noch Kanten übrig sind,
            # dann loggen wir das zum Debuggen.
            if len(edges_to_add_rw) > 0:
                logger.info(
                    f"[{step}]] {rw.name} added {edges_to_add_rw} to the graph"
                )

            edges_to_add.extend(edges_to_add_rw)

        # Und nun: tatsächlich die Kanten hinzufügen
        for edge in edges_to_add:
            if not g.has_edge(edge[0], edge[1]):
                g.add_edge(edge[0], edge[1])

        # Hier werten wir den aktuell gemachten Schritt aus:
        # - Hat der Random Walker eine neue Information gefunden?
        # - Ist die Simulation zu Ende?
        # - Wir aktualisieren unsere Status-Werte!
        for rw in random_walkers:
            # Informationen können nicht "mehrfach" gefunden werden, bzw. das ignorieren wir
            if (
                g.nodes[rw.current_node()]["information"] == searched_information
                and rw.current_node() not in found_nodes
            ):
                found_nodes.append(rw.current_node())

                logger.info(f"[{step}] RandomWalker {rw.name} found the searched information at {rw.current_node()} [{len(found_nodes)}/{searched_information_count}]")
            
        # Speichere die Anzahl der gefundenen Knoten nach jedem Schritt
        step_to_number_of_found_nodes[step] = len(found_nodes)

        # Wir brechen ab, wenn alle gesuchten Informationen des Graphen gefunden wurden
        if len(found_nodes) == searched_information_count:
            break
            
        # Wir brechen ab, wenn wir die maximale Anzahl an Schritten erreicht haben. :-(
        if step >= max_steps:
            break
            
        step += 1

    # An dieser Stelle soll das Ergebnis der Simulation
    # zusammen mit den Parametern der Simulation gespeichert werden,
    # um die Ergebnisse einfacher auswerten zu können. (Wir können dann den Generierungsschritt und den Analyseschritt trennen)
    # Der Generierungsschritt könnte beispielsweise sehr lange dauern und wir wollen die Ergebnisse nicht verlieren.

    # Bisher geben wir die Ergebnisse einfach nur zurück.    

    return { 
        # Die Parameter der Simulation
        "width": grid_width,
        "height": grid_height,
        "num_distinct_information": num_distinct_information,

        "step_to_number_of_found_nodes": step_to_number_of_found_nodes,

        # Ist die Simulation zu Ende, weil alle gesuchten Informationen gefunden wurden 
        # oder weil die maximale Anzahl an Schritten erreicht wurde?
        "break_type": "max_steps" if step >= max_steps else "all_found",

        # Wieviele Schritte wurden wirklich durchgeführt
        "num_steps": step,

        # Wieviele Knoten wurden gefunden?
        "num_found_nodes": len(found_nodes),

        # Wieviele Knoten wurden gesucht?
        "num_searched_nodes": searched_information_count,

        # Wie sieht der Graph nun aus?
        "graph": g
    }

def plot_single_result(result_obj):
    # Den Graphen zeichnen um zu sehen,
    # welche Kanten sich gebildet haben.
    # draw_torus_2d(
    #     result_obj["graph"],
    #     result_obj["num_distinct_information"],
    #     result_obj["width"],
    #     result_obj["height"]
    # )

    # Die Anzahl der gefundenen Knoten über die Schritte hinweg
    # in einem Diagramm darstellen. (plotly, line chart)
    fig = go.Figure()

    # add the line with the numbe of nodes with the searched information
    fig.add_trace(
        go.Scatter(
            x=list(result_obj["step_to_number_of_found_nodes"].keys()),
            y=[result_obj["num_searched_nodes"]] * len(result_obj["step_to_number_of_found_nodes"]),
            mode="lines",
            name="Anzahl der gesuchten Knoten"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list(result_obj["step_to_number_of_found_nodes"].keys()),
            y=list(result_obj["step_to_number_of_found_nodes"].values()),
            mode="lines+markers",
            name="Anzahl der gefundenen Knoten"
        )
    )

    fig.update_layout(
        title="Anzahl der gefundenen Knoten über die Schritte hinweg",
        xaxis_title="Schritt",
        yaxis_title="Anzahl der gefundenen Knoten",
    )


    fig.show()