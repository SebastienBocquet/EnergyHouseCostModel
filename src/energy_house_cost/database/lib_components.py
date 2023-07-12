from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energetic_components import ProductorComponent


class Mock(EnergeticComponent):

    UNCERTAIN_PARAMETERS = {"param1": 10.}

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0.):
        super().__init__(name, initial_install_cost, maintenance_cost, True)

    def compute(self, energy_value: float, is_produced: bool):
        return self._uncertain_parameters[f"{self.name}.param1"].value


class PV(ProductorComponent):

    from energy_house_cost.uncertain import UncertainParameter
    UNCERTAIN_PARAMETERS = {"auto_consumption_ratio": UncertainParameter(
        name="pv.auto_consumption_ratio",
        value=0.45,
        min_value=0.35,
        max_value=0.5
    )}

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0.):
        super().__init__(name, initial_install_cost, maintenance_cost, True)

        self.produced_energy_kwh = 4800.

    def compute(self, energy_value: float, is_produced: bool):
        # TODO take into account variation of power per season
        return -self._uncertain_parameters[f"{self.name}.auto_consumption_ratio"].value * self.produced_energy_kwh

    def injected_energy(self):
        return (1 - self._uncertain_parameters[f"{self.name}.auto_consumption_ratio"].value) * self.produced_energy_kwh

