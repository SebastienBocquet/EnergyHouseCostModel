from __future__ import annotations

from energy_house_cost.database import DB_PATH
from energy_house_cost.database.lib_components import PV
from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energy_cost import EnergyCostProjection
from energy_house_cost.energy_scenario import compute_cost
from energy_house_cost.energy_scenario import EnergyItem
from energy_house_cost.energy_scenario import EnergyScenario
from energy_house_cost.energy_scenario import plot_integrated_cost_per_component

DURATION_YEARS = 15
BOILER_EFFICIENCY = 0.6
HEAT_PUMP_COP = 2.0
CONSUMED_KWH_PER_YEAR_HEATING = 3400.0
PRODUCED_KWH_PER_YEAR_HEATING = CONSUMED_KWH_PER_YEAR_HEATING * BOILER_EFFICIENCY
CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.0

electricity_cost = EnergyCostProjection(
    DB_PATH / "electricity_cost.json", DURATION_YEARS
)
electricity_cost.plot(DURATION_YEARS, show=False, save=True)

gas_cost = EnergyCostProjection(DB_PATH / "gas_cost.json", DURATION_YEARS)
gas_cost.plot(DURATION_YEARS, show=False, save=True)

# heat_pump = EnergeticComponent("heat pump", 15000., 200., HEAT_PUMP_COP)
hot_water_tank = EnergeticComponent("hot water tank", 1000.0, 0.0)
boiler = EnergeticComponent("boiler", 7000.0, 100.0, BOILER_EFFICIENCY)
pv = PV(
    "pv",
    5000.0,
    0.0,
)

energy_items_1 = [
    EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
    EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost),
    EnergyItem(0.0, pv, electricity_cost, is_produced=True),
]
# EnergyItem(PRODUCED_KWH_PER_YEAR_HEATING, heat_pump, electricity_cost, is_produced=True)

scenario = EnergyScenario(energy_items_1, DURATION_YEARS)


if __name__ == "__main__":
    scenario.execute()
    output_data = scenario.get_output_data()
    total_cost = output_data["total_cost"][0]

    # Cost per component is not an output of the scenario (due to grammar validation problem
    # since it is an array of array). So it is obtained by calling directly compute_cost.
    _, cost_per_year_per_component = compute_cost(energy_items_1, DURATION_YEARS)
    component_names = []
    for item in energy_items_1:
        component_names.append(item.component.name)
    plot_integrated_cost_per_component(
        component_names, cost_per_year_per_component, DURATION_YEARS
    )
