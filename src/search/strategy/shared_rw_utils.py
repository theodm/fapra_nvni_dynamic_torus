


def get_neigbor_with_nearest_information(graph, current_node, searched_information, neighbor_list):
    """
    Gibt den Nachbarn dessen Information am nächsten an der gesuchten Information ist zurück.
    """
    # Wähle Nachbarn mit der kleinsten Differenz zur gesuchten Information
    diff = 100000
    next_node = None
    for neighbor in neighbor_list:
        if neighbor == current_node:
            continue

        neighbor_information = graph.nodes[neighbor]["information"]

        if abs(neighbor_information - searched_information) < diff:
            diff = abs(neighbor_information - searched_information)
            next_node = neighbor

    return next_node

