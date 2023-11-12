import skimage


def nodes_between(begin, end):
    """
    Gibt alle Knoten zwischen begin und end zurück. Dabei wird ein Algorithmus zur Zeichnung
    von Linien verwendet. Auch wenn wir in einem Graphen arbeiten ist das sinnvoll, da wir ja wissen,
    das unserer Graph eine besondere Struktur (ein Gitter) hat. Dadurch können wir die Knoten
    zwischen begin und end einfach berechnen, indem wir die Linie zwischen begin und end zeichnen. Das
    ist schneller als einen kürzesten Weg zu berechnen. Die Methode nodes_between allein kann den kürzesten Weg
    jedoch nicht ersetzen, da sie kürzere Wege, die wegen des Zusammenhängen des Gitters bestehen, nicht berücksichtigt.
    Dafür kann die Methode nodes_between_overflow verwendet werden.

    Args:
        begin (tuple): Der Startknoten.
        end (tuple): Der Endknoten.
    """
    result = skimage.draw.line(
        begin[0],
        begin[1],
        end[0],
        end[1],
    )

    nodes_between = []
    for i in range(len(result[0])):
        nodes_between.append((result[0][i], result[1][i]))

    return nodes_between


def nodes_between_overflow(begin, end, width, height):
    """
    Gibt alle Knoten zwischen begin und end zurück. Dabei wird ein Algorithmus zur Zeichnung
    von Linien verwendet. Auch wenn wir in einem Graphen arbeiten ist das sinnvoll, da wir ja wissen,
    das unserer Graph eine besondere Struktur (ein Gitter) hat. Dadurch können wir die Knoten
    zwischen begin und end einfach berechnen, indem wir die Linie zwischen begin und end zeichnen. Das
    ist schneller als einen kürzesten Weg zu berechnen.

    Im Gegensatz zur Methode nodes_between berücksichtigt diese Methode immer den kürzesten Weg, also auch
    über die Ränder des Gitters (Bedenke diese sind verbunden) hinweg.

    Args:
        begin (tuple): Der Startknoten.
        end (tuple): Der Endknoten.
        width (int): Die Breite des Gitters.
        height (int): Die Höhe des Gitters.
    """
    is_begin_lo_of_end = begin[0] <= end[0] and begin[1] <= end[1]
    is_begin_o_of_end = begin[0] == end[0] and begin[1] <= end[1]
    is_begin_ro_of_end = begin[0] >= end[0] and begin[1] <= end[1]
    is_begin_r_of_end = begin[0] >= end[0] and begin[1] == end[1]
    is_begin_ru_of_end = begin[0] >= end[0] and begin[1] >= end[1]
    is_begin_u_of_end = begin[0] == end[0] and begin[1] >= end[1]
    is_begin_lu_of_end = begin[0] <= end[0] and begin[1] >= end[1]
    is_begin_l_of_end = begin[0] <= end[0] and begin[1] == end[1]

    simple_path = (0, 0)
    path_l = (-width, 0)
    path_lo = (-width, -height)
    path_o = (0, -height)
    path_ro = (width, -height)
    path_r = (width, 0)
    path_ru = (width, height)
    path_u = (0, height)
    path_lu = (-width, height)

    path_offsets = [
        simple_path,
    ]

    if is_begin_lo_of_end:
        path_offsets.append(path_l)
        path_offsets.append(path_lo)
        path_offsets.append(path_o)
    if is_begin_o_of_end:
        path_offsets.append(path_lo)
        path_offsets.append(path_o)
        path_offsets.append(path_ro)
    if is_begin_ro_of_end:
        path_offsets.append(path_o)
        path_offsets.append(path_ro)
        path_offsets.append(path_r)
    if is_begin_r_of_end:
        path_offsets.append(path_ro)
        path_offsets.append(path_r)
        path_offsets.append(path_ru)
    if is_begin_ru_of_end:
        path_offsets.append(path_r)
        path_offsets.append(path_ru)
        path_offsets.append(path_u)
    if is_begin_u_of_end:
        path_offsets.append(path_ru)
        path_offsets.append(path_u)
        path_offsets.append(path_lu)
    if is_begin_lu_of_end:
        path_offsets.append(path_u)
        path_offsets.append(path_lu)
        path_offsets.append(path_l)
    if is_begin_l_of_end:
        path_offsets.append(path_lu)
        path_offsets.append(path_l)
        path_offsets.append(path_lo)

    shortest_path = None
    shortest_path_offset = None
    for offset in path_offsets:
        path = nodes_between(begin, (end[0] + offset[0], end[1] + offset[1]))

        if shortest_path is None or len(path) < len(shortest_path):
            shortest_path = path
            shortest_path_offset = offset

    def unoffset(n):
        new_x = n[0]
        if n[0] < 0 or n[0] >= width:
            new_x = n[0] - shortest_path_offset[0]

        new_y = n[1]
        if n[1] < 0 or n[1] >= height:
            new_y = n[1] - shortest_path_offset[1]

        return (new_x, new_y)

    shortest_path = [unoffset(n) for n in shortest_path]

    return shortest_path
