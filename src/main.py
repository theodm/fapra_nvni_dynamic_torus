#%%

import plotly.express as px
import plotly.graph_objects as go
import networkx
from math import pi, cos, sin
import random

def map_2d_point_to_3d_torus(x: int, y: int, width: int, height: int, R1: float = 5.0, R2: float = 3.0):
    """
    Bildet einen Punkt einer zweidimensionalen Matrix auf einen Torus im 3D-Raum ab.

    Args:
        x (int): X-Koordinate des Punkts.
        y (int): Y-Koordinate des Punkts.
        width (int): Breite der zweidimensionalen Matrix.
        height (int): Höhe der zweidimensionalen Matrix.
        R1 (float, optional): Radius des Torus. Defaults to 5.0.
        R2 (float, optional): Radius des Rohrs. Defaults to 3.0.

    Returns:
        tuple: Die Koordinaten des Punkts auf dem Torus. (x, y, z)
    """
    u = 2 * pi * x / width
    v = 2 * pi * y / height

    x = (R1 + R2 * cos(v)) * cos(u)
    y = (R1 + R2 * cos(v)) * sin(u)
    z = R2 * sin(v) 

    return (x, y, z)


def create_random_2d_grid_network(height: int, width: int) -> networkx.Graph:
    """
    Erstellt einen Graphen in Form eines Netzes mit den angegebenen Höhen- und Breitenmaßen. Dabei
    erhalten die Knoten zufällige Informationen zwischen 1 und 10. Die Koordinaten der Knoten in einem Torus
    werden als Attribut gespeichert.

    Args:
        height (int): Die Höhe des Torus.
        width (int): Die Breite des Torus.

    Returns:
        networkx.Graph: Der erstellte Graph.
    """
    
    g = networkx.grid_2d_graph(height, width, periodic=True)

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]['x_pos'] = t_pos[0]
        g.nodes[node]['y_pos'] = t_pos[1]
        g.nodes[node]['z_pos'] = t_pos[2]

        # Zufällige Information (1-10)
        g.nodes[node]['information'] = random.randint(1, 10)

    return g


g = create_random_2d_grid_network(40, 40)

def draw_torus(g: networkx.Graph, colors: list):
    x_nodes = [g.nodes[node]['x_pos'] for node in g.nodes()]
    y_nodes = [g.nodes[node]['y_pos'] for node in g.nodes()]
    z_nodes = [g.nodes[node]['z_pos'] for node in g.nodes()]

    x_edges = []
    y_edges = []
    z_edges = []

    for edge in g.edges():
        # format: [beginning,ending,None]
        x_coords = [g.nodes[edge[0]]['x_pos'], g.nodes[edge[1]]['x_pos'], None]
        x_edges += x_coords

        y_coords = [g.nodes[edge[0]]['y_pos'], g.nodes[edge[1]]['y_pos'], None]
        y_edges += y_coords

        z_coords = [g.nodes[edge[0]]['z_pos'], g.nodes[edge[1]]['z_pos'], None]
        z_edges += z_coords

    trace_edges = go.Scatter3d(x=x_edges,
                               y=y_edges,
                               z=z_edges,
                               mode='lines',
                               line=dict(color='black', width=2),
                               hoverinfo='none')

    trace_nodes = go.Scatter3d(x=x_nodes,
                               y=y_nodes,
                               z=z_nodes,
                               mode='markers',
                               marker=dict(symbol='circle',
                                           size=4,
                                           # color the nodes according to their community
                                           color=[g.nodes[n]["information"] - 1 for n in g.nodes()],
                                           # either green or mageneta
                                           colorscale=colors,
                                           line=dict(color='black', width=0.5)),
                               text=[g.nodes[n]["information"] for n in g.nodes()],
                               hoverinfo='text')

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    layout = go.Layout(title="",
                       width=650,
                       height=625,
                       showlegend=False,
                       scene=dict(xaxis=dict(axis),
                                  yaxis=dict(axis),
                                  zaxis=dict(axis),
                                  ),
                       margin=dict(t=100),
                       hovermode='closest')

    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    fig.show()

colors = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
            "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe"]

draw_torus(g, colors)
