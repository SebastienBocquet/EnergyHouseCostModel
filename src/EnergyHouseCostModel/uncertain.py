from typing import List

from EnergyHouseCostModel.energetic_components import EnergyItem


class UncertainParameter():

    def __init__(self, name, default_value, min_value, max_value):
        self.name = name
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value


def get_uncertain_parameters(energy_items: List[EnergyItem]):
    uncertain_params = {}
    for e in energy_items:
        uncertain_params.update(e.component.UNCERTAIN_PARAMETERS)
    for e in energy_items:
        uncertain_params.update(e.energy_cost.UNCERTAIN_PARAMETERS)
    print("uncertain parameters", uncertain_params)
