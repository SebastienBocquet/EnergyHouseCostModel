from typing import List


class UncertainParameter():

    def __init__(self, default_value, min_value, max_value):
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value


def get_uncertain_parameters(energy_items): # List[EnergyItem]):
    uncertain_params = {}
    for e in energy_items:
        uncertain_params.update(e.component.UNCERTAIN_PARAMETERS)
        uncertain_params.update(e.energy_cost.UNCERTAIN_PARAMETERS)
    print("uncertain parameters", uncertain_params)
    return uncertain_params

#TODO prefix uncertain param name to make sure they are unique.
def set_uncertain_parameters(energy_items, input_data):
    for e in energy_items:
        for key, param in e.component.UNCERTAIN_PARAMETERS.items():
            param.value = input_data[key]
        for key, param in e.energy_cost.UNCERTAIN_PARAMETERS.items():
            param.value = input_data[key]
            e.energy_cost.update()
