import numpy as np

from EnergyHouseCostModel.energy_cost import EnergyCostProjection
from EnergyHouseCostModel.uncertain import UncertainParameter


def electricity_cost(duration_years):

    UNCERTAIN_PARAMETERS = {"electricity_cost_axis": UncertainParameter()}
    CURRENT_ELECTRICITY_COST_ONE_KWH = 0.2062

    electricity_cost_axis = np.array([0.22, 0.25, 0.28])
    year_axis = np.array([1., 5., duration_years])
    electricity_cost = EnergyCostProjection(
        "electricity",
        CURRENT_ELECTRICITY_COST_ONE_KWH,
        "curve", curve=(year_axis, electricity_cost_axis),
        injected_price_per_kwh=0.10)
    electricity_cost.plot(duration_years, show=False)
    return electricity_cost


def gas_cost(duration_years):
    CURRENT_GAS_COST_ONE_KWH = 0.1043

    gas_cost = EnergyCostProjection("gas", CURRENT_GAS_COST_ONE_KWH, "power", percentage_of_increase_per_year=10.)
    gas_cost.plot(duration_years, show=False)
    return gas_cost
