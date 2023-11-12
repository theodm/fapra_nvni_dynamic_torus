from src.torus_creation.shared.line_utils import nodes_between_overflow


def test_nodes_between_overflow():
    #
    # Overflow
    #

    # 1 0 0
    # 0 0 0
    # 0 0 2
    # kürzester Pfad (mit overflow): (0,0) -> (2,2)
    assert nodes_between_overflow((0, 0), (2, 2), 3, 3) == [(0, 0), (2, 2)]

    # 0 1 0
    # 0 0 0
    # 0 2 0
    # kürzester Pfad (mit overflow): (0,1) -> (2,1)
    assert nodes_between_overflow((0, 1), (2, 1), 3, 3) == [(0, 1), (2, 1)]

    # 0 0 1
    # 0 0 0
    # 2 0 0
    # kürzester Pfad (mit overflow): (2,0) -> (0,2)
    assert nodes_between_overflow((2, 0), (0, 2), 3, 3) == [(2, 0), (0, 2)]

    # 0 0 0
    # 2 0 1
    # 0 0 0
    # kürzester Pfad (mit overflow): (2,1) -> (0,1)
    assert nodes_between_overflow((2, 1), (0, 1), 3, 3) == [(2, 1), (0, 1)]

    # 2 0 0
    # 0 0 0
    # 0 0 1
    # kürzester Pfad (mit overflow): (2,2) -> (0,0)
    assert nodes_between_overflow((2, 2), (0, 0), 3, 3) == [(2, 2), (0, 0)]

    # 0 2 0
    # 0 0 0
    # 0 1 0
    # kürzester Pfad (mit overflow): (1,2) -> (1,0)
    assert nodes_between_overflow((1, 2), (1, 0), 3, 3) == [(1, 2), (1, 0)]

    # 0 0 2
    # 0 0 0
    # 1 0 0
    # kürzester Pfad (mit overflow): (0,2) -> (2,0)
    assert nodes_between_overflow((0, 2), (2, 0), 3, 3) == [(0, 2), (2, 0)]

    # 0 0 0
    # 1 0 2
    # 0 0 0
    # kürzester Pfad (mit overflow): (0,1) -> (1,2)
    assert nodes_between_overflow((0, 1), (1, 2), 3, 3) == [(0, 1), (1, 2)]

    #
    # Kein Overflow
    #

    # 1 0 0
    # 0 2 0
    # 0 0 0
    # kürzester Pfad (kein overflow): (0,0) -> (1,1)
    assert nodes_between_overflow((0, 0), (1, 1), 3, 3) == [(0, 0), (1, 1)]

    # 0 1 0
    # 0 2 0
    # 0 0 0
    # kürzester Pfad (kein overflow): (0,1) -> (1,1)
    assert nodes_between_overflow((0, 1), (1, 1), 3, 3) == [(0, 1), (1, 1)]

    # 0 0 1
    # 0 2 0
    # 0 0 0
    # kürzester Pfad (kein overflow): (0,2) -> (1,1)
    assert nodes_between_overflow((0, 2), (1, 1), 3, 3) == [(0, 2), (1, 1)]

    # 0 0 0
    # 0 2 1
    # 0 0 0
    # kürzester Pfad (kein overflow): (2,1) -> (1,1)
    assert nodes_between_overflow((2, 1), (1, 1), 3, 3) == [(2, 1), (1, 1)]

    # 0 0 0
    # 0 2 0
    # 0 0 1
    # kürzester Pfad (kein overflow): (2,2) -> (1,1)
    assert nodes_between_overflow((2, 2), (1, 1), 3, 3) == [(2, 2), (1, 1)]

    # 0 0 0
    # 0 2 0
    # 0 1 0
    # kürzester Pfad (kein overflow): (1,2) -> (1,1)
    assert nodes_between_overflow((1, 2), (1, 1), 3, 3) == [(1, 2), (1, 1)]

    # 0 0 0
    # 0 2 0
    # 1 0 0
    # kürzester Pfad (kein overflow): (0,2) -> (1,1)
    assert nodes_between_overflow((0, 2), (1, 1), 3, 3) == [(0, 2), (1, 1)]

    # 0 0 0
    # 1 2 0
    # 0 0 0
    # kürzester Pfad (kein overflow): (0,1) -> (1,1)
    assert nodes_between_overflow((0, 1), (1, 1), 3, 3) == [(0, 1), (1, 1)]
