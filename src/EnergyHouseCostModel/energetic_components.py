from dataclasses import dataclass
from abc import ABC, abstractmethod
from EnergyHouseCostModel.energy_cost import EnergyCostProjection
from EnergyHouseCostModel.uncertain import UncertainParameter


class Component(ABC):

    UNCERTAIN_PARAMETERS = {}

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0., production_over_consumption_ratio: float | None = None):
        self.name = name
        self.initial_install_cost = initial_install_cost
        self.maintenance_cost_per_year = maintenance_cost
        self.production_over_consumption_ratio = production_over_consumption_ratio

    def energy_consumption(self, energy_value: float, is_produced: bool):
        """Computes the energy consumed based on the energy produced.

        Args:
            energy_value: energy produced in kWh per year.
            is_produced: if True the energy is considered produced by the component.
            Otherwise it is considered as consumed by the component.

        Returns: energy consumed in kWh per year.

        """
        if is_produced:
            if self.production_over_consumption_ratio is None:
                raise ValueError("production_over_consumption_ratio must be defined as a float.")
            return energy_value / self.production_over_consumption_ratio
        else:
            return energy_value

    def injected_energy(self):
        return 0.

    def __repr__(self):
        return self.name


@dataclass
class EnergyItem:
    """An energy item. The energetic profile is defined as a list of energy items."""
    energy_value: float
    component: Component
    energy_cost: EnergyCostProjection
    is_produced: bool = False

    def __repr__(self):
        energy_consumed = self.component.energy_consumption(self.energy_value, self.is_produced)
        energy_produced_or_consumed = "Consumed"
        if self.is_produced:
            energy_produced_or_consumed = "Produced"
        return f"{energy_produced_or_consumed} {energy_consumed} kWh of {self.energy_cost} by a {self.component}"





class PV(Component):

    UNCERTAIN_PARAMETERS = {"auto_consumption_ratio": UncertainParameter(
        "auto_consumption_ratio",
        default_value=0.4,
        min_value=0.3,
        max_value=0.5
    )}

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0.):
        super().__init__(name, initial_install_cost, maintenance_cost, 1.)

        sunny_hours = 7.
        max_power_kw = 3.
        self.produced_energy_kwh = sunny_hours * max_power_kw * 365
        self.auto_consumption_ratio = self.UNCERTAIN_PARAMETERS["auto_consumption_ratio"].value

    def energy_consumption(self, energy_value: float, is_produced: bool):
        # TODO take into account variation of power per season
        return -self.auto_consumption_ratio * self.produced_energy_kwh

    def injected_energy(self):
        return (1 - self.auto_consumption_ratio) * self.produced_energy_kwh