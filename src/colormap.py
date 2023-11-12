from math import log

import matplotlib


def colormap_for_information(num_distinct_information: int, color_map="inferno"):
    """
    Erstellt eine Liste von Farben, die für die unterschiedlichen Informationen
    verwendet werden können. Es wird ein Farbverlauf verwendet, der von der
    Farbkarte abhängt.

    Args:
        num_distinct_information (int): Die Anzahl der unterschiedlichen Informationen.
        color_map (str): Der Name der Farbkarte, die verwendet werden soll. Aus matplotlib.

    Returns:
        list: Eine Liste von Farben, die für die unterschiedlichen Informationen
                verwendet werden können. (z.B. ['#000004', '#bc3754'])
    """
    cmap = matplotlib.cm.get_cmap(color_map)

    colors = []

    for i in range(num_distinct_information):
        # Gibt die Farbe in folgendem Format zurück: (r, g, b, alpha)
        # z.B. (0.0, 0.0, 0.0, 1.0) für schwarz
        #      (1.0, 1.0, 1.0, 1.0) für weiß
        # color_in_floats_with_alpha = cmap((i**10) / (num_distinct_information**10))
        color_in_floats_with_alpha = cmap(i / num_distinct_information)

        # Den Alpha-Wert entfernen
        color_in_floats = color_in_floats_with_alpha[:3]

        # Und dann einen hexadezimalen Wert
        # z.B. #000000 für schwarz
        #      #ffffff für weiß
        color_in_hex = matplotlib.colors.rgb2hex(color_in_floats)

        colors.append(color_in_hex)

    return colors
