import networkx
import skimage

from torus_creation.shared.torus_utils import map_2d_point_to_3d_torus


def create_2d_grid_from_image(
    width: int, height: int, num_distinct_information: int, image_filename: str
) -> networkx.Graph:
    """
    Erstellt eine 2D-Gitter-Graphen aus einem Bild. Dabei wird das Bild auf die
    Größe width x height skaliert und in Graustufen konvertiert. Die Information
    jedes Knotens wird dann auf den Grauwert des entsprechenden Pixels gesetzt.

    Die Idee dahinter: In einem Bild wird es Cluster-Bildungen geben, die durch
    die Graustufen repräsentiert werden. Diese Cluster-Bildungen sollen dann
    auch im Graphen repräsentiert werden.

    Args:
        width (int): Die Breite des Graphen.
        height (int): Die Höhe des Graphen.
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        image_filename (str): Der Dateiname des Bildes, das verwendet werden soll (innerhalb des ../images/-Ordner).
    """
    # load image with ski-image from file
    image = skimage.io.imread("../images/" + image_filename)

    # resize image to width and height
    image = skimage.transform.resize(image, (width, height))

    # convert to grayscale
    image = skimage.color.rgb2gray(image)

    # create graph
    g = networkx.grid_2d_graph(width, height, periodic=True)

    # add information to nodes
    for node in g.nodes():
        # get pixel value from image
        pixel_value = image[node[0]][node[1]]

        # convert pixel value to information
        information = int(pixel_value * num_distinct_information)

        # set information
        g.nodes[node]["information"] = information

        # set 3D position
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]

    return g
