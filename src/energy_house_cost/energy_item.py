from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint
from typing import Iterable
from typing import Mapping

from numpy._typing import NDArray

from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energy_cost import EnergyCostProjection


@dataclass
class EnergyItem:
    """An energy item.

    The energetic profile is defined as a list of energy items.
    """

    energy_value: float
    component: EnergeticComponent
    energy_cost: EnergyCostProjection
    is_produced: bool = False
    integrated_cost: float = 0.0

    def __repr__(self):
        energy_value = self.component.compute(self.energy_value, self.is_produced)
        year_averaged_cost = self.integrated_cost / self.energy_cost.duration_years
        return (
            f"{self.component.name} "
            f"{self.component.get_summary(energy_value)}"
            f" of {self.energy_cost.name}\n"
            f" which represents {year_averaged_cost:.0f}"
            f" euros (average per year, including initial cost and maintenance)\n"
        )


def get_uncertain_parameters(energy_items: Iterable[EnergyItem]):
    uncertain_params = {}
    for e in energy_items:
        uncertain_params.update(e.component._uncertain_parameters)
        uncertain_params.update(e.energy_cost._uncertain_parameters)
    print("Scenario parameters")
    pprint(uncertain_params)
    return uncertain_params


# TODO prefix uncertain param name to make sure they are unique.
def set_uncertain_parameters(
    energy_items: Iterable[EnergyItem], input_data: Mapping[str : NDArray[float]]
):
    for e in energy_items:
        for key, param in e.component._uncertain_parameters.items():
            param.value = input_data[key][0]
        for key, param in e.energy_cost._uncertain_parameters.items():
            param.value = input_data[key][0]
