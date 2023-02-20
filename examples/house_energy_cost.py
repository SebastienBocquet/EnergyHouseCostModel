import numpy as np
from matplotlib import pyplot as plt

from EnergyHouseCostModel.energetic_components import Component, EnergyItem
from EnergyHouseCostModel.energy_cost import EnergyCostProjection, compute_cost

if __name__ == "__main__":

    DURATION_YEARS = 15
    BOILER_EFFICIENCY = 0.6
    HEAT_PUMP_COP = 2.
    CONSUMED_KWH_PER_YEAR_HEATING = 3400.
    PRODUCED_KWH_PER_YEAR_HEATING = 3400. * BOILER_EFFICIENCY
    CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.
    CURRENT_ELECTRICITY_COST_ONE_KWH = 0.2062
    CURRENT_GAS_COST_ONE_KWH = 0.1043

    electricity_cost_axis = np.array([0.22, 0.25, 0.28])
    year_axis = np.array([1., 5., DURATION_YEARS])
    electricity_cost = EnergyCostProjection("electricity", CURRENT_ELECTRICITY_COST_ONE_KWH, "curve", curve=(year_axis, electricity_cost_axis))
    electricity_cost.plot(DURATION_YEARS, show=False)

    gas_cost = EnergyCostProjection("gas", CURRENT_GAS_COST_ONE_KWH, "power", percentage_of_increase_per_year=10.)
    gas_cost.plot(DURATION_YEARS, show=False)

    heat_pump = Component("heat pump", 15000., 200., HEAT_PUMP_COP)
    hot_water_tank = Component("hot water tank", 1000., 0.)
    boiler = Component("boiler", 7000., 100., BOILER_EFFICIENCY)

    energy_items_1 = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
                  EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost)]

    total_cost_1 = compute_cost(energy_items_1, DURATION_YEARS, show=False)

    energy_items_2 = [EnergyItem(PRODUCED_KWH_PER_YEAR_HEATING, heat_pump, electricity_cost, is_produced=True),
                       EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost)]

    compute_cost(energy_items_2, DURATION_YEARS, show=False)

    # Compare scenarios
    compute_cost(energy_items_1 + energy_items_2, DURATION_YEARS)
