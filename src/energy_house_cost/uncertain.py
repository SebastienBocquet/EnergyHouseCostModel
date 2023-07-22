from __future__ import annotations

from numpy import inf


class UncertainParameter:
    def __init__(self, name, value=0.0, min_value=None, max_value=None):
        self.name = name
        self.default_value = value
        self.is_uncertain = False if (min_value is None or max_value is None) else True
        self.min_value = min_value if min_value is not None else -inf
        self.max_value = max_value if max_value is not None else inf
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: float):
        if v > self.max_value or v < self.min_value:
            raise ValueError(
                f"Parameter {self.name} is out of bounds: value {v}"
                f" should be in [{self.min_value, self.max_value}]"
            )
        self._value = v

    def __repr__(self):
        if self.is_uncertain:
            range_msg = f" ranging in [{self.min_value}, {self.max_value}]"
        else:
            range_msg = ""
        return f"value = {self.value}{range_msg}"
