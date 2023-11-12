from math import pi, cos, sin


def map_2d_point_to_3d_torus(
    x: int, y: int, width: int, height: int, R1: float = 5.0, R2: float = 3.0
):
    """
    Bildet einen Punkt einer zweidimensionalen Matrix auf einen Torus im 3D-Raum ab.

    Args:
        x (int): X-Koordinate des Punkts.
        y (int): Y-Koordinate des Punkts.
        width (int): Breite der zweidimensionalen Matrix.
        height (int): Höhe der zweidimensionalen Matrix.
        R1 (float, optional): Radius des Torus. Defaults to 5.0.
        R2 (float, optional): Radius des Rohrs. Defaults to 3.0.

    Returns:
        tuple: Die Koordinaten des Punkts auf dem Torus. (x, y, z)
    """
    u = 2 * pi * x / width
    v = 2 * pi * y / height

    x = (R1 + R2 * cos(v)) * cos(u)
    y = (R1 + R2 * cos(v)) * sin(u)
    z = R2 * sin(v)

    return (x, y, z)
