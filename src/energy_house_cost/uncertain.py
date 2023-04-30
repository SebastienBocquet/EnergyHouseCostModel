from typing import List

import numpy as np


class UncertainParameter():

    def __init__(self, default_value=0., min_value=None, max_value=None):
        self.default_value = default_value
        if min_value is None:
            self.min_value = default_value
        else:
            self.min_value = min_value
        if max_value is None:
            self.max_value = default_value
        else:
            self.max_value = max_value
        self.value = default_value

    # @setter
    # def value(self, v):
    #     assert v <= self.max_value
    #     assert v >= self.min_value
    #     self.value = v


def get_uncertain_parameters(energy_items): # List[EnergyItem]):
    uncertain_params = {}
    for e in energy_items:
        uncertain_params.update(e.component._uncertain_parameters)
        uncertain_params.update(e.energy_cost._uncertain_parameters)
    print("uncertain parameters", uncertain_params)
    return uncertain_params

#TODO prefix uncertain param name to make sure they are unique.
def set_uncertain_parameters(energy_items, input_data):
    for e in energy_items:
        for key, param in e.component._uncertain_parameters.items():
            param.value = input_data[key]
        for key, param in e.energy_cost._uncertain_parameters.items():
            param.value = input_data[key]
