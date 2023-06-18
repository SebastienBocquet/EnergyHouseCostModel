from energy_house_cost.energy_cost import Component


class EnergeticComponent(Component):

    #TODO add init args as uncertain parameters
    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0., production_over_consumption_ratio: float | None = None):
        super().__init__()
        self.name = name
        self.initial_install_cost = initial_install_cost
        self.maintenance_cost_per_year = maintenance_cost
        self.production_over_consumption_ratio = production_over_consumption_ratio

    def energy_consumption(self, energy_value: float, is_produced: bool):
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

    def injected_energy(self):
        return 0.

    def __repr__(self):
        return self.name



class PV(EnergeticComponent):

    from energy_house_cost.uncertain import UncertainParameter
    UNCERTAIN_PARAMETERS = {"auto_consumption_ratio": UncertainParameter(
        name = "pv.auto_consumption_ratio",
        value=0.,
        min_value=0.,
        max_value=0.
    )}

    def __init__(self, name: str, initial_install_cost: float = 0., maintenance_cost: float = 0.):
        super().__init__(name, initial_install_cost, maintenance_cost, 1.)
        self._name = name
        self._uncertain_parameters = {}
        for k, v in self.UNCERTAIN_PARAMETERS.items():
            self._uncertain_parameters[f"{self._name}.{k}"] = self.UNCERTAIN_PARAMETERS[k]

        sunny_hours = 7.
        max_power_kw = 3.
        self.produced_energy_kwh = sunny_hours * max_power_kw * 365

    def energy_consumption(self, energy_value: float, is_produced: bool):
        # TODO take into account variation of power per season
        return -self._uncertain_parameters[f"{self._name}.auto_consumption_ratio"].value * self.produced_energy_kwh

    def injected_energy(self):
        return (1 - self._uncertain_parameters[f"{self._name}.auto_consumption_ratio"].value) * self.produced_energy_kwh