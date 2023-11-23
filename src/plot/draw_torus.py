# %%
from typing import Literal

import plotly.graph_objects as go
import networkx
import random

from src.plot.colormap import colormap_for_information
from src.ranged_int.ranged_int import OverflowInt


def get_line_points_from_edge_to_edge(
    node1: tuple[int, int], node2: tuple[int, int], width: int, height: int
) -> list[tuple[float, float]]:
    """
    Gibt eine Liste von Punkten zurück, die eine Linie zwischen den beiden Knoten darstellt. Dabei wird
    die Linie so gewählt, dass es zu keinen visuellen Überschneidugnen zu anderen Knoten kommt.
    """
    a = node1
    b = node2

    # Wenn a und b gleich sein, Fehler, hier soll es keine Selbstverbindungen geben
    if a == b:
        raise ValueError("a and b must not be equal")

    x_diff = abs(b[0] - a[0])
    y_diff = abs(b[1] - a[1])

    # Wenn a und b Nachbarn sind oder diagonal sind, dann ist die Linie einfach die Verbindung zwischen den beiden Punkten
    if x_diff <= 1 and y_diff <= 1:
        return [(a[0], a[1]), (b[0], b[1])]

    # Wenn a und b auf gleicher Y-Koordinate liegen
    # dann gehen wir vom linken Knoten 1/2 Schritt hoch (oder runter)
    # dann nach rechts und dann 1/2 Schritt runter (oder hoch)
    #
    #  z.B.
    #  --------------------------------
    #  |                              |
    #  a                              b
    #
    #  z.B.
    #  a                              b
    #  |                              |
    #  --------------------------------
    if a[1] == b[1]:
        # Wenn a rechts von b liegt, dann tauschen wir die beiden
        # damit a immer links liegt.
        if a[0] > b[0]:
            a, b = b, a

        sign = random.choice([-1, 1])

        return [
            (a[0], a[1]),
            (a[0], a[1] + sign * 0.5),
            (b[0], b[1] + sign * 0.5),
            (b[0], b[1]),
        ]

    # Wenn a und b auf gleicher X-Koordinate liegen
    # dann analog zu oben, nur mit x und y vertauscht
    if a[0] == b[0]:
        # Wenn a unter b liegt, dann tauschen wir die beiden
        # damit a immer über b liegt.
        if a[1] > b[1]:
            a, b = b, a

        sign = random.choice([-1, 1])

        return [
            (a[0], a[1]),
            (a[0] + sign * 0.5, a[1]),
            (b[0] + sign * 0.5, b[1]),
            (b[0], b[1]),
        ]

    # Ansonsten liegen a und b schräg zueinander
    # Wir stellen sicher, dass a links von b liegt,
    # dann gibt es zwei verbleibende Fälle:
    # 1. a liegt links oben von b
    if a[0] > b[0]:
        a, b = b, a

    # 1. a liegt links oben von b
    if a[1] < b[1]:
        # a
        # 1/2 Schritt nach rechts und 1/2 Schritt nach unten
        # (b[0]-a[0]) Schritte nach rechts
        # (b[1]-a[1]) Schritte nach unten
        # 1/2 Schritt nach rechts und 1/2 Schritt nach unten
        # b

        return [
            (a[0], a[1]),
            (a[0] + 0.5, a[1] + 0.5),
            (a[0] + 0.5 + (x_diff - 1), a[1] + 0.5),
            (a[0] + 0.5 + (x_diff - 1), a[1] + 0.5 + (y_diff - 1)),
            (b[0], b[1]),
        ]

    # 2. a liegt links unten von b
    if a[1] > b[1]:
        # a
        # 1/2 Schritt nach rechts und 1/2 Schritt nach oben
        # (b[0]-a[0]) Schritte nach rechts
        # (a[1]-b[1]) Schritte nach oben
        # 1/2 Schritt nach rechts und 1/2 Schritt nach oben
        # b

        return [
            (a[0], a[1]),
            (a[0] + 0.5, a[1] - 0.5),
            (a[0] + 0.5 + (x_diff - 1), a[1] - 0.5),
            (a[0] + 0.5 + (x_diff - 1), a[1] - 0.5 - (y_diff - 1)),
            (b[0], b[1]),
        ]

    raise ValueError("This should never happen")


def _select_colors(
    color_mode: Literal["normal", "distance_to_target"],
    target_information: int | None,
    num_distinct_information: int,
    colormap: str,
):
    """
    Gibt die Palette zurück, die für die Knoten verwendet werden sollen. Wird anhand
    der Parameter color_mode und target_information bestimmt. Die Beschreibung wie color_mode
    und target_information Einfluss nehmen befindet sich in der Dokumentation zu draw_torus_2d und draw_torus_3d.
    """
    if color_mode == "normal":
        colors = colormap_for_information(num_distinct_information, colormap)
    elif color_mode == "distance_to_target":
        if target_information is None:
            raise ValueError(
                "target_information must be set if color_mode is 'distance_to_target'"
            )
        diff_to_max = abs(target_information - num_distinct_information)
        diff_to_min = abs(target_information - 0)

        colors = colormap_for_information(max(diff_to_max, diff_to_min) + 1, colormap)
        colors = colors[::-1]
    else:
        raise ValueError(f"Unknown color_mode: {color_mode}")

    return colors


def _get_color(
    g: networkx.Graph,
    colors: list[str],
    color_mode: Literal["normal", "distance_to_target"],
    target_information: int | None,
    node: tuple[int, int],
):
    """
    Gibt die Farbe zurück, die für den Knoten verwendet werden soll. Wird anhand
    der Parameter color_mode und target_information bestimmt. Muss in Kombination
    mit _select_colors verwendet werden.
    """
    if color_mode == "normal":
        return colors[g.nodes[node]["information"]]
    elif color_mode == "distance_to_target":
        return colors[abs(g.nodes[node]["information"] - target_information)]
    else:
        raise ValueError(f"Unknown color_mode: {color_mode}")


def _get_text_for_node(g, node):
    """
    Gibt den Text zurück, der beim Hovern über einen Knoten angezeigt werden soll.
    """
    return f"{g.nodes[node]['information']} ({node[0]},{node[1]})"


def draw_torus_2d(
    g: networkx.Graph,
    num_distinct_information: int,
    width: int,
    height: int,
    colormap: str = "inferno",
    color_mode: Literal["normal", "distance_to_target"] = "normal",
    target_information: int | None = None,
):
    """
    Gibt den Graphen mittels Plotly in 2D als Gitter aus.

    Die Knoten werden entsprechend ihrer Information eingefärbt. Falls der color_mode auf
    'distance_to_target' gesetzt ist, muss target_information gesetzt sein. Dann werden die Knoten
    entsprechend ihrer Distanz zur target_information eingefärbt. Ansonsten im 'normal' Modus
    entsprechend ihrer Information (von 0 bis num_distinct_information - 1).

    Args:
        g (networkx.Graph): Der Graph, der gezeichnet werden soll.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        colormap (str, optional): Die Farbpalette aus matplotlib, die verwendet werden soll. Defaults to "inferno".
        color_mode (Literal["normal", "distance_to_target"], optional): Der Modus, in dem die Knoten eingefärbt werden sollen. Defaults to "normal".
        target_information (int | None, optional): Die Information, die als Ziel gesetzt ist. Wird nur verwendet, wenn color_mode auf 'distance_to_target' gesetzt ist. Defaults to None.
    """
    colors = _select_colors(
        color_mode, target_information, num_distinct_information, colormap
    )

    x_nodes = [node[0] for node in g.nodes()]
    y_nodes = [node[1] for node in g.nodes()]

    def filter_edge_if_trivial(edge: tuple[tuple[int, int], tuple[int, int]]) -> bool:
        left = (int(OverflowInt(edge[0][0], width) - 1), edge[0][1])
        right = (int(OverflowInt(edge[0][0], width) + 1), edge[0][1])
        top = (edge[0][0], int(OverflowInt(edge[0][1], height) - 1))
        bottom = (edge[0][0], int(OverflowInt(edge[0][1], height) + 1))

        return edge not in [
            (edge[0], left),
            (edge[0], right),
            (edge[0], top),
            (edge[0], bottom),
        ]

    # Wir filtern nichttriviale Kanten heraus, das heißt solche die nicht direkt nebeneinander liegende
    # Knoten verbinden. Diese werden dann mit get_lines_from_edge_to_edge gezeichnet.
    non_trivial_edges = [
        (edge[0], edge[1]) for edge in g.edges() if filter_edge_if_trivial(edge)
    ]

    # Wir zeichnen nur die nichttrivialen Kanten. Dafür generieren wir zur Übersichtlichkeit
    # mehrere Linien zwischen den Knoten, die die Kante verbinden.
    line_points_edges = []
    for edge in non_trivial_edges:
        line_points_edges.append(
            get_line_points_from_edge_to_edge(edge[0], edge[1], None, None)
        )

    trace_nodes = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode="markers",
        marker=dict(
            symbol="circle",
            size=4,
            color=[
                _get_color(g, colors, color_mode, target_information, n)
                for n in g.nodes()
            ],
            line=dict(color="black", width=0.5),
        ),
        text=[_get_text_for_node(g, n) for n in g.nodes()],
        hoverinfo="text",
    )

    axis = dict(
        showbackground=False,
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    layout = go.Layout(
        title="",
        width=650,
        height=625,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(t=100),
        hovermode="closest",
    )

    data = [trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    for edge in line_points_edges:
        for i in range(len(edge) - 1):
            fig.add_shape(
                type="line",
                x0=edge[i][0],
                y0=edge[i][1],
                x1=edge[i + 1][0],
                y1=edge[i + 1][1],
                line=dict(color="rgba(0,0,0,0.25)", width=2),
            )

    fig.show()


def draw_torus_3d(
    g: networkx.Graph,
    num_distinct_information: int,
    colormap: str = "inferno",
    color_mode: Literal["normal", "distance_to_target"] = "normal",
    target_information: int | None = None,
):
    """
    Gibt den Graphen mittels Plotly in 3D aus. Dafür müssen die Knoten die Attribute
    x_pos, y_pos und z_pos haben, welche vorher mit map_2d_point_to_3d_torus berechnet werden können.
    Die Knoten werden entsprechend ihrer Information eingefärbt. Falls der color_mode auf
    'distance_to_target' gesetzt ist, muss target_information gesetzt sein. Dann werden die Knoten
    entsprechend ihrer Distanz zur target_information eingefärbt. Ansonsten im 'normal' Modus
    entsprechend ihrer Information (von 0 bis num_distinct_information - 1).

    Args:
        g (networkx.Graph): Der Graph, der gezeichnet werden soll.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        colormap (str, optional): Die Farbpalette aus matplotlib, die verwendet werden soll. Defaults to "inferno".
        color_mode (Literal["normal", "distance_to_target"], optional): Der Modus, in dem die Knoten eingefärbt werden sollen. Defaults to "normal".
        target_information (int | None, optional): Die Information, die als Ziel gesetzt ist. Wird nur verwendet, wenn color_mode auf 'distance_to_target' gesetzt ist. Defaults to None.
    """

    colors = _select_colors(
        color_mode, target_information, num_distinct_information, colormap
    )

    x_nodes = [g.nodes[node]["x_pos"] for node in g.nodes()]
    y_nodes = [g.nodes[node]["y_pos"] for node in g.nodes()]
    z_nodes = [g.nodes[node]["z_pos"] for node in g.nodes()]

    x_edges = []
    y_edges = []
    z_edges = []

    for edge in g.edges():
        # format: [beginning,ending,None]
        x_coords = [g.nodes[edge[0]]["x_pos"], g.nodes[edge[1]]["x_pos"], None]
        x_edges += x_coords

        y_coords = [g.nodes[edge[0]]["y_pos"], g.nodes[edge[1]]["y_pos"], None]
        y_edges += y_coords

        z_coords = [g.nodes[edge[0]]["z_pos"], g.nodes[edge[1]]["z_pos"], None]
        z_edges += z_coords

    trace_edges = go.Scatter3d(
        x=x_edges,
        y=y_edges,
        z=z_edges,
        mode="lines",
        line=dict(color="black", width=2),
        hoverinfo="none",
    )

    trace_nodes = go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode="markers",
        marker=dict(
            symbol="circle",
            size=4,
            color=[
                _get_color(g, colors, color_mode, target_information, n)
                for n in g.nodes()
            ],
            line=dict(color="black", width=0.5),
        ),
        text=[_get_text_for_node(g, n) for n in g.nodes()],
        hoverinfo="text",
    )

    axis = dict(
        showbackground=False,
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    layout = go.Layout(
        title="",
        width=650,
        height=625,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(t=100),
        hovermode="closest",
    )

    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    fig.show()
