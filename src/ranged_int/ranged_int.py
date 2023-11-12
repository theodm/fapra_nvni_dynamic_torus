class OverflowInt:
    """
    Repräsentiert einen Integer, der bei Überlauf wieder bei 0 bzw. bei range_min anfängt.

    z.B. OverflowInt(10, 20) + OverflowInt(15, 20) == OverflowInt(5, 20)
    """

    range_min: int
    range_max: int
    value: int

    def __init__(self, value: int, range_max: int, range_min: int = 0):
        self.range_min = range_min
        self.range_max = range_max
        self.value = value

        if self.range_min > self.range_max:
            raise ValueError(
                "range_min must be smaller than range_max (was: "
                + str(self.range_min)
                + " and "
                + str(self.range_max)
                + ")"
            )

        if self.value < self.range_min:
            raise ValueError(
                "value must be greater than range_min (was: "
                + str(self.value)
                + " and "
                + str(self.range_min)
                + ")"
            )

        if self.value >= self.range_max:
            raise ValueError(
                "value must be smaller than range_max (was: "
                + str(self.value)
                + " and "
                + str(self.range_max)
                + ")"
            )

    def overflow(self, value: int) -> int:
        """
        Berechnet den Wert, der bei Überlauf entsteht. (z.B. 10 + 15 = 5 [range_max=20])

        Private Methode!
        """
        normalized_value = value - self.range_min
        normalized_range_max = self.range_max - self.range_min

        if normalized_value < 0:
            ret = (
                normalized_range_max - (abs(normalized_value) % normalized_range_max)
            ) % normalized_range_max
        else:
            ret = normalized_value % normalized_range_max

        return ret + self.range_min

    def raise_if_incompatible(self, other):
        if isinstance(other, ClampedInt):
            raise ValueError("OverflowInt + ClampedInt is not supported")

        if not isinstance(other, OverflowInt):
            raise ValueError(
                "other must be of type OverflowInt (was: " + str(type(other)) + ")"
            )

        if other.range_max != self.range_max:
            raise ValueError(
                "range_max must be the same (was: "
                + str(other.range_max)
                + " and "
                + str(self.range_max)
                + ")"
            )

        if other.range_min != self.range_min:
            raise ValueError(
                "range_min must be the same (was: "
                + str(other.range_min)
                + " and "
                + str(self.range_min)
                + ")"
            )

    def __add__(self, other):
        if isinstance(other, int):
            return OverflowInt(
                self.overflow(self.value + other), self.range_max, self.range_min
            )

        self.raise_if_incompatible(other)

        return OverflowInt(
            self.overflow(self.value + other.value), self.range_max, self.range_min
        )

    def __sub__(self, other):
        if isinstance(other, int):
            return OverflowInt(
                self.overflow(self.value - other), self.range_max, self.range_min
            )

        self.raise_if_incompatible(other)

        return OverflowInt(
            self.overflow(self.value - other.value), self.range_max, self.range_min
        )

    #
    # def __mul__(self, other):
    #     if isinstance(other, int):
    #         return OverflowInt(self.value * other, self.range_max, self.range_min)
    #
    #     self.raise_if_incompatible(other)
    #
    #     return OverflowInt(self.overflow(self.value * other.value), self.range_max, self.range_min)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, OverflowInt):
            return self.value == other.value

        return False

    def __int__(self):
        return self.value

    def __repr__(self):
        return str(self.value)


class ClampedInt:
    """
    Repräsentiert einen Integer, der bei Überlauf bei range_min bzw. bei range_max aufhört.
    """

    range_min: int
    range_max: int
    value: int

    def __init__(self, value: int, range_max: int, range_min: int = 0):
        self.range_min = range_min
        self.range_max = range_max
        self.value = value

        if self.range_min > self.range_max:
            raise ValueError(
                "range_min must be smaller than range_max (was: "
                + str(self.range_min)
                + " and "
                + str(self.range_max)
                + ")"
            )

        if self.value < self.range_min:
            raise ValueError(
                "value must be greater than range_min (was: "
                + str(self.value)
                + " and "
                + str(self.range_min)
                + ")"
            )

        if self.value >= self.range_max:
            raise ValueError(
                "value must be smaller than range_max (was: "
                + str(self.value)
                + " and "
                + str(self.range_max)
                + ")"
            )

    def clamp(self, value: int) -> int:
        return max(min(value, self.range_max - 1), self.range_min)

    def raise_if_incompatible(self, other):
        if isinstance(other, OverflowInt):
            raise ValueError("ClampedInt + OverflowInt is not supported")

        if not isinstance(other, ClampedInt):
            raise ValueError(
                "other must be of type ClampedInt (was: " + str(type(other)) + ")"
            )

        if other.range_max != self.range_max:
            raise ValueError(
                "range_max must be the same (was: "
                + str(other.range_max)
                + " and "
                + str(self.range_max)
                + ")"
            )

        if other.range_min != self.range_min:
            raise ValueError(
                "range_min must be the same (was: "
                + str(other.range_min)
                + " and "
                + str(self.range_min)
                + ")"
            )

    def __add__(self, other):
        if isinstance(other, int):
            return ClampedInt(
                self.clamp(self.value + other), self.range_max, self.range_min
            )

        self.raise_if_incompatible(other)

        return ClampedInt(
            self.clamp(self.value + other.value), self.range_max, self.range_min
        )

    def __sub__(self, other):
        if isinstance(other, int):
            return ClampedInt(
                self.clamp(self.value - other), self.range_max, self.range_min
            )

        self.raise_if_incompatible(other)

        return ClampedInt(
            self.clamp(self.value - other.value), self.range_max, self.range_min
        )

    #
    # def __mul__(self, other):
    #     if isinstance(other, int):
    #         return ClampedInt(self.clamp(self.value * other), self.range_max, self.range_min)
    #
    #     self.raise_if_incompatible(other)
    #
    #     return ClampedInt(self.clamp(self.value * other.value), self.range_max, self.range_min)

    def __int__(self):
        return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, ClampedInt):
            return self.value == other.value

        return False


RangedInt = OverflowInt | ClampedInt
