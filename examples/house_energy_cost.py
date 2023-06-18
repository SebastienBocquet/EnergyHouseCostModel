from gemseo.core.discipline import MDODiscipline

from energy_house_cost.database.energy_scenario import EnergyItem
from energy_house_cost.database.energy_scenario import EnergyScenario
from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energetic_components import PV
from energy_house_cost.energy_cost import EnergyCostProjection
from energy_house_cost.uncertain import get_uncertain_parameters
from energy_house_cost.database import DB_PATH




if __name__ == "__main__":

    DURATION_YEARS = 15
    BOILER_EFFICIENCY = 0.6
    HEAT_PUMP_COP = 2.
    CONSUMED_KWH_PER_YEAR_HEATING = 3400.
    PRODUCED_KWH_PER_YEAR_HEATING = CONSUMED_KWH_PER_YEAR_HEATING * BOILER_EFFICIENCY
    CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.

    electricity_cost = EnergyCostProjection(DB_PATH / "electricity_cost.json", DURATION_YEARS)
    electricity_cost.plot(DURATION_YEARS, show=False)

    gas_cost = EnergyCostProjection(DB_PATH / "gas_cost.json", DURATION_YEARS)
    gas_cost.plot(DURATION_YEARS, show=False)

    heat_pump = EnergeticComponent("heat pump", 15000., 200., HEAT_PUMP_COP)
    hot_water_tank = EnergeticComponent("hot water tank", 1000., 0.)
    boiler = EnergeticComponent("boiler", 7000., 100., BOILER_EFFICIENCY)
    pv = PV("pv", 5000., 0.)

    energy_items_1 = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
        EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost),
        EnergyItem(0., pv, electricity_cost, is_produced=True)]

    # TODO add uncertain params as defualt_inputs.
    input_data = {}
    for name, param in get_uncertain_parameters(energy_items_1).items():
        input_data.update({name: param.value})

    scenario = EnergyScenario(energy_items_1, DURATION_YEARS)
    scenario.execute(input_data)
    input_data["electricity_cost.slope"] = 0.12
    scenario.execute(input_data)
    input_data["gas_cost.slope"] = 0.12
    scenario.execute(input_data)
