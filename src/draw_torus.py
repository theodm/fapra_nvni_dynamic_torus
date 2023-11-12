# %%
from typing import Literal

import plotly.express as px
import plotly.graph_objects as go
import networkx
from math import pi, cos, sin
import random

from src.colormap import colormap_for_information
from src.ranged_int.ranged_int import ClampedInt, OverflowInt
from src.torus_creation.blobs_increase_grid import (
    create_random_2d_grid_network_constant_blob_increase,
)
from src.torus_creation.image_grid import create_2d_grid_from_image
from src.torus_creation.information_blobs_grid import (
    create_random_2d_grid_network_information_blobs,
)
from src.torus_creation.information_lines_grid import (
    create_random_2d_grid_network_information_lines,
)
from src.torus_creation.lines_increase_grid import (
    create_random_2d_grid_network_constant_lines_increase,
)
from src.torus_creation.random_walker_grid import create_random_2d_grid_random_walkers


def draw_torus(
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

    def get_text_for_node(node):
        """
        Gibt den Text zurück, der beim Hovern über einen Knoten angezeigt werden soll.
        """
        return f"{g.nodes[node]['information']} ({node[0]},{node[1]})"

    def get_color(node):
        """
        Gibt die Farbe zurück, die für den Knoten verwendet werden soll. Wird anhand
        der Parameter color_mode und target_information bestimmt.
        """
        if color_mode == "normal":
            return colors[g.nodes[node]["information"]]
        elif color_mode == "distance_to_target":
            return colors[abs(g.nodes[node]["information"] - target_information)]
        else:
            raise ValueError(f"Unknown color_mode: {color_mode}")

    trace_nodes = go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode="markers",
        marker=dict(
            symbol="circle",
            size=4,
            color=[get_color(n) for n in g.nodes()],
            line=dict(color="black", width=0.5),
        ),
        text=[get_text_for_node(n) for n in g.nodes()],
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
