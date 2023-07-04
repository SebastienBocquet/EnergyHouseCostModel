from pprint import pprint
from typing import List

from numpy import inf


class UncertainParameter():

    def __init__(self, name, value=0., min_value=None, max_value=None):
        self.name = name
        self.default_value = value
        self.is_uncertain = False if (min_value is None or max_value is None) else True
        self.min_value = min_value if min_value is not None else -inf
        self.max_value = max_value if max_value is not None else inf
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v > self.max_value or v < self.min_value:
            raise ValueError(f"Parameter {self.name} is out of bounds: value {v}"
                             f" should be in [{self.min_value, self.max_value}]")
        self._value = v

    def __repr__(self):
        if self.is_uncertain:
            range_msg = f" ranging in [{self.min_value}, {self.max_value}]"
        else:
            range_msg = ""
        return f"value = {self.value}{range_msg}"


def get_uncertain_parameters(energy_items): # List[EnergyItem]):
    uncertain_params = {}
    for e in energy_items:
        uncertain_params.update(e.component._uncertain_parameters)
        uncertain_params.update(e.energy_cost._uncertain_parameters)
    print("Scenario parameters")
    pprint(uncertain_params)
    return uncertain_params

#TODO prefix uncertain param name to make sure they are unique.
def set_uncertain_parameters(energy_items, input_data):
    for e in energy_items:
        for key, param in e.component._uncertain_parameters.items():
            param.value = input_data[key]
        for key, param in e.energy_cost._uncertain_parameters.items():
            param.value = input_data[key]
