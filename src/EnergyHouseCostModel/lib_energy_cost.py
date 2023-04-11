import numpy as np

from EnergyHouseCostModel.uncertain import UncertainParameter
from EnergyHouseCostModel.energy_cost import EnergyCostProjection, EnergyCost



class ElectricityCost(EnergyCost):

    CURRENT_ELECTRICITY_COST_ONE_KWH = 0.2062
    UNCERTAIN_PARAMETERS = {"electricity_cost_axis_1": UncertainParameter(0.22,
    0.18, 0.25)}

    def __init__(
        self,
        duration_years: int,
        ):
        self.duration_years = duration_years
        self.update()
        self.cost.plot(duration_years, show=False)

    def update(self):
        electricity_cost_axis = np.array([self.UNCERTAIN_PARAMETERS["electricity_cost_axis_1"].value, 0.25, 0.28])
        year_axis = np.array([1., 5., self.duration_years])
        self.cost = EnergyCostProjection(
            "electricity",
            self.CURRENT_ELECTRICITY_COST_ONE_KWH,
            "curve", curve=(year_axis, electricity_cost_axis),
            injected_price_per_kwh=0.10)


class GasCost(EnergyCost):

    CURRENT_GAS_COST_ONE_KWH = 0.1043
    UNCERTAIN_PARAMETERS = {"percentage_increase": UncertainParameter(10., 7., 15.)}

    def __init__(
        self,
        duration_years: int,
        ):
        self.duration_years = duration_years
        self.update()
        self.cost.plot(duration_years, show=False)

    # TODO cost could be a property, which calls update()
    def update(self):
        self.cost = EnergyCostProjection("gas", self.CURRENT_GAS_COST_ONE_KWH, "power",
            percentage_of_increase_per_year=self.UNCERTAIN_PARAMETERS["percentage_increase"].value)
