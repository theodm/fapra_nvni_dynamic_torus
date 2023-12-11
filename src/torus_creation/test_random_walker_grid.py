from torus_creation.random_walker_grid import find_increase_path_with_overflow


def test_find_increase_path_with_overflow():
    assert find_increase_path_with_overflow(0, 0, 5) == 0
    assert find_increase_path_with_overflow(1, 0, 5) == 1
    assert find_increase_path_with_overflow(2, 0, 5) == 1
    assert find_increase_path_with_overflow(3, 0, 5) == -1
    assert find_increase_path_with_overflow(4, 0, 5) == -1

    assert find_increase_path_with_overflow(0, 1, 5) == -1
    assert find_increase_path_with_overflow(1, 1, 5) == 0
    assert find_increase_path_with_overflow(2, 1, 5) == 1
    assert find_increase_path_with_overflow(3, 1, 5) == 1
    assert find_increase_path_with_overflow(4, 1, 5) == -1

    assert find_increase_path_with_overflow(0, 2, 5) == -1
    assert find_increase_path_with_overflow(1, 2, 5) == -1
    assert find_increase_path_with_overflow(2, 2, 5) == 0
    assert find_increase_path_with_overflow(3, 2, 5) == 1
    assert find_increase_path_with_overflow(4, 2, 5) == 1

    assert find_increase_path_with_overflow(0, 3, 5) == 1
    assert find_increase_path_with_overflow(1, 3, 5) == -1
    assert find_increase_path_with_overflow(2, 3, 5) == -1
    assert find_increase_path_with_overflow(3, 3, 5) == 0
    assert find_increase_path_with_overflow(4, 3, 5) == 1

    assert find_increase_path_with_overflow(0, 4, 5) == 1
    assert find_increase_path_with_overflow(1, 4, 5) == 1
    assert find_increase_path_with_overflow(2, 4, 5) == -1
    assert find_increase_path_with_overflow(3, 4, 5) == -1
    assert find_increase_path_with_overflow(4, 4, 5) == 0
