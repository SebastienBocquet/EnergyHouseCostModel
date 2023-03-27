import numpy as np
from matplotlib import pyplot as plt

from EnergyHouseCostModel.energetic_components import Component, EnergyItem
from EnergyHouseCostModel.energetic_components import PV
from EnergyHouseCostModel.energy_cost import EnergyCostProjection, compute_cost
from EnergyHouseCostModel.lib_energy_cost import electricity_cost, gas_cost

if __name__ == "__main__":

    DURATION_YEARS = 15
    BOILER_EFFICIENCY = 0.6
    HEAT_PUMP_COP = 2.
    CONSUMED_KWH_PER_YEAR_HEATING = 3400.
    PRODUCED_KWH_PER_YEAR_HEATING = 3400. * BOILER_EFFICIENCY
    CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.
    CURRENT_GAS_COST_ONE_KWH = 0.1043

    electricity_cost = electricity_cost(DURATION_YEARS)
    gas_cost = gas_cost(DURATION_YEARS)

    heat_pump = Component("heat pump", 15000., 200., HEAT_PUMP_COP)
    hot_water_tank = Component("hot water tank", 1000., 0.)
    boiler = Component("boiler", 7000., 100., BOILER_EFFICIENCY)
    pv = PV("pv", 5000., 0.)

    energy_items_1 = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
        EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost),
        EnergyItem(0., pv, electricity_cost, is_produced=True)]

    total_cost_1 = compute_cost(energy_items_1, DURATION_YEARS, show=True)

    # energy_items_2 = [EnergyItem(PRODUCED_KWH_PER_YEAR_HEATING, heat_pump, electricity_cost, is_produced=True),
    #                    EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost)]
    #
    # compute_cost(energy_items_2, DURATION_YEARS, show=False)
    #
    # # Compare scenarios
    # compute_cost(energy_items_1 + energy_items_2, DURATION_YEARS)
