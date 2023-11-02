#%%

import plotly.express as px
import plotly.graph_objects as go
import networkx
from math import pi, cos, sin
import random

from create import create_farbtupfer_2d_grid_network, create_random_2d_grid_network



# g = create_farbtupfer_2d_grid_network(200, 200)

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

# colors = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
#             "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe"]

# draw_torus(g, colors)

# # %%
