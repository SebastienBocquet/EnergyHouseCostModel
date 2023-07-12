from energy_house_cost.energy_cost import Component


class EnergeticComponent():

    UNCERTAIN_PARAMETERS = None

    #TODO add init args as uncertain parameters
    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0., production_over_consumption_ratio: float | None = None):
        self.name = name
        self.initial_install_cost = initial_install_cost
        self.maintenance_cost_per_year = maintenance_cost
        self.production_over_consumption_ratio = production_over_consumption_ratio
        self._uncertain_parameters = {}
        if self.UNCERTAIN_PARAMETERS is not None:
            for k, v in self.UNCERTAIN_PARAMETERS.items():
                self._uncertain_parameters[f"{self.name}.{k}"] = self.UNCERTAIN_PARAMETERS[k]
        else:
            self._uncertain_parameters = {}

    def compute(self, energy_value: float, is_produced: bool):
        """Computes the energy consumed based on the energy produced.

        Args:
            energy_value: energy produced in kWh per year.
            is_produced: if True the energy is considered produced by the component.
            It is practical since in general, we know the energy produced and
            the efficiency (i.e. :attr:`production_over_consumption_ratio`.
            Otherwise it is considered as consumed by the component.

        Returns: energy consumed in kWh per year.

        """
        if is_produced:
            if self.production_over_consumption_ratio is None:
                raise ValueError("production_over_consumption_ratio must be defined as a float.")
            return energy_value / self.production_over_consumption_ratio
        else:
            return energy_value

    def get_summary(self, energy_value):
        return f"consumed {energy_value} kWh on the grid"

    @property
    def parameters(self):
        return self._uncertain_parameters


class ProductorComponent(EnergeticComponent):

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0.,
    can_inject_energy = False):
        super().__init__(name, initial_install_cost, maintenance_cost, None)
        self.can_inject_energy = can_inject_energy

    def injected_energy(self):
        return 0.

    def get_summary(self, energy_value):
        if self.can_inject_energy:
            inject_energy_msg = f" and sold {self.injected_energy()} kWh"
        else:
            inject_energy_msg = ""
        return f"saved {energy_value} kWh from the grid{inject_energy_msg}"
