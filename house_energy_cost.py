from dataclasses import dataclass
import numpy as np
from energetic_components import Component, EnergyItem
from energy_cost import EnergyCostProjection, compute_cost
import logging

if __name__ == "__main__":

    DURATION_YEARS = 15
    BOILER_EFFICIENCY = 0.6
    HEAT_PUMP_COP = 2.
    CONSUMED_KWH_PER_YEAR_HEATING = 3400.
    PRODUCED_KWH_PER_YEAR_HEATING = 3400. * BOILER_EFFICIENCY
    CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.
    CURRENT_ELECTRICITY_COST_ONE_KWH = 0.174
    CURRENT_GAS_COST_ONE_KWH = 0.088

    electricity_cost_axis = np.array([0.18, 0.19, 0.2, 0.21])
    year_axis = np.linspace(1, DURATION_YEARS, len(electricity_cost_axis))
    electricity_cost = EnergyCostProjection("electricity", CURRENT_ELECTRICITY_COST_ONE_KWH, "curve", curve=(year_axis, electricity_cost_axis))

    gas_cost = EnergyCostProjection("gas", CURRENT_GAS_COST_ONE_KWH, "linear", slope=0.03)

    heat_pump = Component("heat pump", 15000., 200., HEAT_PUMP_COP)
    hot_water_tank = Component("hot water tank", 1000., 0.)
    boiler = Component("boiler", 7000., 100., BOILER_EFFICIENCY)

    energy_items = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
                    EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost)]

    total_cost = compute_cost(energy_items, DURATION_YEARS)
    print(f"Integrated cost for \n{[i for i in energy_items]} \nis {total_cost} euros over {DURATION_YEARS} years")

    energy_items_2 = [EnergyItem(PRODUCED_KWH_PER_YEAR_HEATING, heat_pump, electricity_cost, "produced"),
                      EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost)]

    total_cost = compute_cost(energy_items_2, DURATION_YEARS)
    print(f"Integrated cost for \n{[i for i in energy_items_2]} \nis {total_cost} euros over {DURATION_YEARS} years")

    petrol_car = Component("petrol car", 21000., 500.)
    electric_car = Component("electric car", 21000., 200.)
    CAR_LITER_OF_PETROL_PER_100_KM = 7.
    DISTANCE_KM_PER_YEAR = 15000.
    KWH_PETROL_PER_LITER = 0.
    PETROL_MOTOR_EFFICIENCY = 0.2
    CONSUMED_LITER_OF_PETROL_PER_YEAR = CAR_LITER_OF_PETROL_PER_100_KM * DISTANCE_KM_PER_YEAR
    PRODUCED_KWH_PER_YEAR_BY_CAR = CONSUMED_LITER_OF_PETROL_PER_YEAR * KWH_PETROL_PER_LITER * PETROL_MOTOR_EFFICIENCY
    energy_items = [EnergyItem(CONSUMED_LITER_OF_PETROL_PER_YEAR, petrol_car, petrol_cost)]
    energy_items_2 = [EnergyItem(PRODUCED_KWH_PER_YEAR_BY_CAR, electric_car, electricity_cost)]
