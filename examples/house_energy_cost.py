from gemseo.core.discipline import MDODiscipline
from numpy import array

from EnergyHouseCostModel.energetic_components import Component, EnergyItem
from EnergyHouseCostModel.energetic_components import PV
from EnergyHouseCostModel.energy_cost import compute_cost
from EnergyHouseCostModel.lib_energy_cost import ElectricityCost
from EnergyHouseCostModel.lib_energy_cost import GasCost
from EnergyHouseCostModel.uncertain import get_uncertain_parameters
from EnergyHouseCostModel.uncertain import set_uncertain_parameters

class EnergyScenario(MDODiscipline):

    def __init__(self, duration_years):
        super().__init__("energy_scenario", grammar_type="SimpleGrammar")
        self.duration_years = duration_years

    def _run(self):
        set_uncertain_parameters(energy_items_1, input_data)
        total_cost, _ = compute_cost(energy_items_1, DURATION_YEARS, show=False)
        self.store_local_data(**{"total_cost": total_cost})

if __name__ == "__main__":

    DURATION_YEARS = 15
    BOILER_EFFICIENCY = 0.6
    HEAT_PUMP_COP = 2.
    CONSUMED_KWH_PER_YEAR_HEATING = 3400.
    PRODUCED_KWH_PER_YEAR_HEATING = CONSUMED_KWH_PER_YEAR_HEATING * BOILER_EFFICIENCY
    CONSUMED_KWH_PER_YEAR_HOT_WATER = 3 * 800.
    CURRENT_GAS_COST_ONE_KWH = 0.1043

    electricity_cost = ElectricityCost(DURATION_YEARS)
    gas_cost = GasCost(DURATION_YEARS)

    heat_pump = Component("heat pump", 15000., 200., HEAT_PUMP_COP)
    hot_water_tank = Component("hot water tank", 1000., 0.)
    boiler = Component("boiler", 7000., 100., BOILER_EFFICIENCY)
    pv = PV("pv", 5000., 0.)

    energy_items_1 = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
        EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost),
        EnergyItem(0., pv, electricity_cost, is_produced=True)]

    input_data = {}
    for name, param in get_uncertain_parameters(energy_items_1).items():
        input_data.update({name: param.value})

    scenario = EnergyScenario(DURATION_YEARS)
    # TODO set grammars in constructor. PAss energy_items to constructor and set as attribute.
    scenario.input_grammar.update_from_data(input_data)
    scenario.output_grammar.update({"total_cost": float})
    scenario.execute(input_data)
    print(scenario.get_output_data()["total_cost"])
    input_data["percentage_increase"] = 15.
    scenario.execute(input_data)
    print(scenario.get_output_data()["total_cost"])
