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


def create_farbtupfer_2d_grid_network(height: int, width: int) -> networkx.Graph:
    g = networkx.grid_2d_graph(height, width, periodic=True)

    # 1/10 aller Knoten erhalten die gesuchte Information
    searched_information_count = 15

    # Zufällige Knoten auswählen
    searched_information_nodes = random.sample(list(g.nodes()), searched_information_count)

    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]['x_pos'] = t_pos[0]
        g.nodes[node]['y_pos'] = t_pos[1]
        g.nodes[node]['z_pos'] = t_pos[2]

        g.nodes[node]['information'] = 0

    for node in searched_information_nodes:
        radius = 2

        def sub_width_overflow(a, b):
            if a - b < 0:
                return width + (a - b)
            
            return a - b

        def sub_height_overflow(a, b):
            if a - b < 0:
                return height + (a - b)
            
            return a - b
        
        def add_width_overflow(a, b):
            if a + b >= width:
                return (a + b) - width
            
            return a + b
        
        def add_height_overflow(a, b):
            if a + b >= height:
                return (a + b) - height
            
            return a + b
        
        # Alle Knoten in einem Radius von 2 erhalten die gesuchte Information
        for x in range(sub_width_overflow(node[0], radius), add_width_overflow(node[0], radius) + 1):
            for y in range(sub_height_overflow(node[1], radius), add_height_overflow(node[1], radius) + 1):
                g.nodes[(x, y)]['information'] = 5


    

    return g
        
        

    
