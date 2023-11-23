from src.plot.colormap import colormap_for_information


def generate_html_for_colormap(colors: list):
    # Ein kleiner Helfer um sicherzustellen, dass
    # die Farben auch wirklich richtig sind.
    html = "<html><body><table><tr>"
    for color in colors:
        html += f'<td style="background-color:{color}">{color}</td>'
    html += "</tr></table></body></html>"
    return html


def test_colormap_for_information_2_default_inferno():
    assert colormap_for_information(2) == ["#000004", "#bc3754"]


def test_colormap_for_information_10_default_inferno():
    print(generate_html_for_colormap(colormap_for_information(10)))
    assert colormap_for_information(10) == [
        "#000004",
        "#1a0a4a",
        "#3b0f40",
        "#5c1436",
        "#7d1a2c",
        "#9e1f22",
        "#bf2408",
        "#e02a00",
        "#ff6e00",
        "#ffab00",
    ]


def test_colormap_for_information_10_default_viridis():
    print(generate_html_for_colormap(colormap_for_information(10, color_map="viridis")))
    assert colormap_for_information(10, color_map="viridis") == [
        "#440154",
        "#482475",
        "#414487",
        "#355f8d",
        "#2a788e",
        "#21918c",
        "#22a884",
        "#44bf70",
        "#7ad151",
        "#bddf26",
    ]
