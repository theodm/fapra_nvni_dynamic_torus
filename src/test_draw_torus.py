from src.draw_torus import get_line_points_from_edge_to_edge


def draw_lines_between_points(points, width, height):
    # draw with matplotlib
    import matplotlib.pyplot as plt

    plt.gca().invert_yaxis()

    for x in range(width):
        for y in range(height):
            plt.plot(x, y, "bo")

    # plot line between two points
    for i in range(len(points) - 1):
        plt.plot(
            [points[i][0], points[i + 1][0]], [points[i][1], points[i + 1][1]], "r-"
        )

    plt.show()


def test_get_line_points_from_edge_to_edge_special():
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((4, 25), (27, 9), 30, 30), 30, 30
    )


def test_get_line_points_from_edge_to_edge():
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((0, 0), (2, 2), 3, 3), 3, 3
    )
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((2, 2), (0, 0), 3, 3), 3, 3
    )

    draw_lines_between_points(
        get_line_points_from_edge_to_edge((1, 0), (1, 2), 3, 3), 3, 3
    )
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((1, 2), (1, 0), 3, 3), 3, 3
    )

    draw_lines_between_points(
        get_line_points_from_edge_to_edge((2, 0), (0, 2), 3, 3), 3, 3
    )
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((0, 2), (2, 0), 3, 3), 3, 3
    )

    draw_lines_between_points(
        get_line_points_from_edge_to_edge((0, 1), (2, 1), 3, 3), 3, 3
    )
    draw_lines_between_points(
        get_line_points_from_edge_to_edge((2, 1), (0, 1), 3, 3), 3, 3
    )

    # links oben und rechts unten
    assert get_line_points_from_edge_to_edge((0, 0), (2, 2), 3, 3) == [
        (0, 0),
        (0.5, 0.5),
        (1.5, 0.5),
        (1.5, 1.5),
        (2, 2),
    ]
    assert get_line_points_from_edge_to_edge((2, 2), (0, 0), 3, 3) == [
        (0, 0),
        (0.5, 0.5),
        (1.5, 0.5),
        (1.5, 1.5),
        (2, 2),
    ]

    # oben mitte und unten mitte
    assert get_line_points_from_edge_to_edge((1, 0), (1, 2), 3, 3) in [
        [
            (1, 0),
            (1.5, 0),
            (1.5, 2),
            (1, 2),
        ],
        [
            (1, 0),
            (0.5, 0),
            (0.5, 2),
            (1, 2),
        ],
    ]
    assert get_line_points_from_edge_to_edge((1, 2), (1, 0), 3, 3) in [
        [
            (1, 0),
            (1.5, 0),
            (1.5, 2),
            (1, 2),
        ],
        [
            (1, 0),
            (0.5, 0),
            (0.5, 2),
            (1, 2),
        ],
    ]

    # oben rechts und unten links
    assert get_line_points_from_edge_to_edge((2, 0), (0, 2), 3, 3) == [
        (0, 2),
        (0.5, 1.5),
        (1.5, 1.5),
        (1.5, 0.5),
        (2, 0),
    ]
    assert get_line_points_from_edge_to_edge((0, 2), (2, 0), 3, 3) == [
        (0, 2),
        (0.5, 1.5),
        (1.5, 1.5),
        (1.5, 0.5),
        (2, 0),
    ]

    # rechts mitte und links mitte
    assert get_line_points_from_edge_to_edge((0, 1), (2, 1), 3, 3) in [
        [(0, 1), (0, 0.5), (2, 0.5), (2, 1)],
        [(0, 1), (0, 1.5), (2, 1.5), (2, 1)],
    ]
    assert get_line_points_from_edge_to_edge((2, 1), (0, 1), 3, 3) in [
        [(0, 1), (0, 0.5), (2, 0.5), (2, 1)],
        [(0, 1), (0, 1.5), (2, 1.5), (2, 1)],
    ]
