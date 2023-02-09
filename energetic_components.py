from dataclasses import dataclass
from abc import ABC, abstractmethod
from energy_cost import EnergyCostProjection


class Component(ABC):

    def __init__(self, name, initial_install_cost=0., maintenance_cost=0., production_over_consumption_ratio=None):
        self.name = name
        self.initial_install_cost = initial_install_cost
        self.maintenance_cost_per_year = maintenance_cost
        self.production_over_consumption_ratio = production_over_consumption_ratio

    def energy_consumption(self, energy_item):
        """Computes the energy consumed based on the energy produced.

        Args:
            energy_item: energy produced in kWh per year.

        Returns: energy consumed in kWh per year.

        """
        if energy_item.energy_consumed_or_produced == "consumed":
            return energy_item.energy_value
        elif energy_item.energy_consumed_or_produced == "produced":
            if self.production_over_consumption_ratio is None:
                raise ValueError("production_over_consumption_ratio must be defined as a float.")
            return energy_item.energy_value / self.production_over_consumption_ratio
        else:
            raise ValueError("energy_item.energy_consumed_or_produced must be 'consumed' or 'produced'.")

    def injected_energy(self):
        return 0.

@dataclass
class EnergyItem:
    """An energy item. The energetic profile is defined as a list of energy items."""
    energy_value: float
    component: Component
    energy_cost: EnergyCostProjection
    energy_consumed_or_produced: str = "consumed"

    def __repr__(self):
        return f"{self.energy_consumed_or_produced} energy {self.energy_value} kWh of {self.energy_cost} by a {self.component}"


class PV(Component):

    def __init__(self):
        self.initial_install_cost = 5000.
        self.maintenance_cost = 0.

    def energy_consumption(self, energy_item):
        # TODO take into account variation of power per season
        auto_consumption_ratio = 0.4
        sunny_hours = 7.
        max_power_kw = 3.
        return -auto_consumption_ratio * max_power_kw * sunny_hours * 365
