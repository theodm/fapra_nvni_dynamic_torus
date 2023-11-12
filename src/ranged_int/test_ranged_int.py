import pytest

from src.ranged_int.ranged_int import OverflowInt, ClampedInt


def test_overflow_int_init():
    # Fehler wenn range_min > range_max
    with pytest.raises(ValueError):
        OverflowInt(4, 4, range_min=5)
    # Fehler wenn value < range_min
    with pytest.raises(ValueError):
        OverflowInt(-1, 10)
    # Fehler wenn value >= range_max
    with pytest.raises(ValueError):
        OverflowInt(10, 10)


def test_overflow_int_add():
    # Simpler Test innerhalb der Grenzen
    assert OverflowInt(1, 10) + OverflowInt(2, 10) == OverflowInt(3, 10)
    # Test mit Überlauf nach oben
    assert OverflowInt(9, 10) + OverflowInt(2, 10) == OverflowInt(1, 10)

    # Simpler Test innerhalb der Grenzen mit int
    assert OverflowInt(1, 10) + 2 == OverflowInt(3, 10)
    # Test mit Überlauf nach oben mit int
    assert OverflowInt(9, 10) + 2 == OverflowInt(1, 10)
    # Test mit doppeltem Überlauf nach oben mit int
    assert OverflowInt(8, 10) + 20 == OverflowInt(8, 10)

    # Test mit gesetzem range_min
    assert OverflowInt(11, 20, range_min=10) + 2 == OverflowInt(13, 20, range_min=10)
    # Test mit Überlauf nach oben und gesetzem range_min
    assert OverflowInt(19, 20, range_min=10) + 2 == OverflowInt(11, 20, range_min=10)
    # Test mit doppeltem Überlauf nach oben und gesetzem range_min
    assert OverflowInt(18, 20, range_min=10) + 20 == OverflowInt(18, 20, range_min=10)

    # Fehler wenn inkompatibler Typ
    with pytest.raises(ValueError):
        OverflowInt(1, 10) + ClampedInt(1, 10)
    # Fehler wenn range_max nicht gleich
    with pytest.raises(ValueError):
        OverflowInt(1, 10) + OverflowInt(1, 20)
    # Fehler wenn range_min nicht gleich
    with pytest.raises(ValueError):
        OverflowInt(1, 10, range_min=0) + OverflowInt(1, 10, range_min=1)


def test_overflow_int_sub():
    # Simpler Test innerhalb der Grenzen
    assert OverflowInt(5, 10) - OverflowInt(2, 10) == OverflowInt(3, 10)
    # Test mit Überlauf nach unten
    assert OverflowInt(1, 10) - OverflowInt(2, 10) == OverflowInt(9, 10)

    # Simpler Test innerhalb der Grenzen mit int
    assert OverflowInt(5, 10) - 2 == OverflowInt(3, 10)
    # Test mit Überlauf nach unten mit int
    assert OverflowInt(1, 10) - 2 == OverflowInt(9, 10)
    # Test mit doppeltem Überlauf nach unten mit int
    assert OverflowInt(1, 10) - 20 == OverflowInt(1, 10)

    # Test mit gesetzem range_min
    assert OverflowInt(15, 20, range_min=10) - 2 == OverflowInt(13, 20, range_min=10)
    # Test mit Überlauf nach unten und gesetzem range_min
    assert OverflowInt(11, 20, range_min=10) - 2 == OverflowInt(19, 20, range_min=10)
    # Test mit doppeltem Überlauf nach unten und gesetzem range_min
    assert OverflowInt(11, 20, range_min=10) - 20 == OverflowInt(11, 20, range_min=10)

    # Fehler wenn inkompatibler Typ
    with pytest.raises(ValueError):
        OverflowInt(1, 10) - ClampedInt(1, 10)
    # Fehler wenn range_max nicht gleich
    with pytest.raises(ValueError):
        OverflowInt(1, 10) - OverflowInt(1, 20)
    # Fehler wenn range_min nicht gleich
    with pytest.raises(ValueError):
        OverflowInt(1, 10, range_min=0) - OverflowInt(1, 10, range_min=1)


def test_overflow_overflow():
    assert OverflowInt(0, 10).overflow(0) == 0
    assert OverflowInt(0, 10).overflow(-1) == 9
    assert OverflowInt(0, 10).overflow(-2) == 8
    assert OverflowInt(0, 10).overflow(-3) == 7
    assert OverflowInt(0, 10).overflow(-4) == 6
    assert OverflowInt(0, 10).overflow(-5) == 5
    assert OverflowInt(0, 10).overflow(-6) == 4
    assert OverflowInt(0, 10).overflow(-7) == 3
    assert OverflowInt(0, 10).overflow(-8) == 2
    assert OverflowInt(0, 10).overflow(-9) == 1
    assert OverflowInt(0, 10).overflow(-10) == 0
    assert OverflowInt(0, 10).overflow(-11) == 9


def test_overflow_int_sub_special():
    assert OverflowInt(6, 10) - 16 == OverflowInt(0, 10)


def test_overflow_to_int():
    assert int(OverflowInt(1, 10)) == 1
    assert int(OverflowInt(11, 20, range_min=10)) == 11


def test_overflow_to_str():
    assert str(OverflowInt(1, 10)) == "1"
    assert str(OverflowInt(11, 20, range_min=10)) == "11"


def test_overflow_eq():
    assert OverflowInt(1, 10) == 1
    assert OverflowInt(11, 20, range_min=10) == 11
    assert OverflowInt(1, 10) != 2
    assert OverflowInt(11, 20, range_min=10) != 12


def test_clamped_int_init():
    # Fehler wenn range_min > range_max
    with pytest.raises(ValueError):
        ClampedInt(4, 4, range_min=5)
    # Fehler wenn value < range_min
    with pytest.raises(ValueError):
        ClampedInt(-1, 10)
    # Fehler wenn value >= range_max
    with pytest.raises(ValueError):
        ClampedInt(10, 10)


def test_clamped_int_add():
    # Simpler Test innerhalb der Grenzen
    assert ClampedInt(1, 10) + ClampedInt(2, 10) == ClampedInt(3, 10)
    # Test mit Überlauf nach oben
    assert ClampedInt(9, 10) + ClampedInt(2, 10) == ClampedInt(9, 10)

    # Simpler Test innerhalb der Grenzen mit int
    assert ClampedInt(1, 10) + 2 == ClampedInt(3, 10)
    # Test mit Überlauf nach oben mit int
    assert ClampedInt(9, 10) + 2 == ClampedInt(9, 10)

    # Test mit gesetzem range_min
    assert ClampedInt(11, 20, range_min=10) + 2 == ClampedInt(13, 20, range_min=10)
    # Test mit Überlauf nach oben und gesetzem range_min
    assert ClampedInt(19, 20, range_min=10) + 2 == ClampedInt(19, 20, range_min=10)

    # Fehler wenn inkompatibler Typ
    with pytest.raises(ValueError):
        ClampedInt(1, 10) + OverflowInt(1, 10)
    # Fehler wenn range_max nicht gleich
    with pytest.raises(ValueError):
        ClampedInt(1, 10) + ClampedInt(1, 20)
    # Fehler wenn range_min nicht gleich
    with pytest.raises(ValueError):
        ClampedInt(1, 10, range_min=0) + ClampedInt(1, 10, range_min=1)


def test_clamped_int_sub():
    # Simpler Test innerhalb der Grenzen
    assert ClampedInt(5, 10) - ClampedInt(2, 10) == ClampedInt(3, 10)
    # Test mit Überlauf nach unten
    assert ClampedInt(1, 10) - ClampedInt(2, 10) == ClampedInt(0, 10)

    # Simpler Test innerhalb der Grenzen mit int
    assert ClampedInt(5, 10) - 2 == ClampedInt(3, 10)
    # Test mit Überlauf nach unten mit int
    assert ClampedInt(1, 10) - 2 == ClampedInt(0, 10)

    # Test mit gesetzem range_min
    assert ClampedInt(15, 20, range_min=10) - 2 == ClampedInt(13, 20, range_min=10)
    # Test mit Überlauf nach unten und gesetzem range_min
    assert ClampedInt(11, 20, range_min=10) - 2 == ClampedInt(10, 20, range_min=10)

    # Fehler wenn inkompatibler Typ
    with pytest.raises(ValueError):
        ClampedInt(1, 10) - OverflowInt(1, 10)
    # Fehler wenn range_max nicht gleich
    with pytest.raises(ValueError):
        ClampedInt(1, 10) - ClampedInt(1, 20)
    # Fehler wenn range_min nicht gleich
    with pytest.raises(ValueError):
        ClampedInt(1, 10, range_min=0) - ClampedInt(1, 10, range_min=1)


def test_clamped_to_int():
    assert int(ClampedInt(1, 10)) == 1
    assert int(ClampedInt(11, 20, range_min=10)) == 11


def test_clamped_to_str():
    assert str(ClampedInt(1, 10)) == "1"
    assert str(ClampedInt(11, 20, range_min=10)) == "11"


def test_clamped_eq():
    assert ClampedInt(1, 10) == 1
    assert ClampedInt(11, 20, range_min=10) == 11
    assert ClampedInt(1, 10) != 2
    assert ClampedInt(11, 20, range_min=10) != 12
