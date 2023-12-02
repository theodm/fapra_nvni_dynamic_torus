


def get_neigbor_with_nearest_information(graph, current_node, searched_information):
    """
    Gibt den Nachbarn dessen Information am nächsten an der gesuchten Information ist zurück.
    """
    # Wähle Nachbarn mit der kleinsten Differenz zur gesuchten Information
    current_node_information = graph.nodes[current_node]["information"]

    # Sortiere Nachbarn nach Differenz zur gesuchten Information
    sorted_neighbors = sorted(
        graph.neighbors(current_node),
        key=lambda x: abs(
            graph.nodes[x]["information"] - searched_information
        ),
    )

    return sorted_neighbors[0]

