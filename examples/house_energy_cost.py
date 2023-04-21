from gemseo.core.discipline import MDODiscipline
from numpy import array

from EnergyHouseCostModel.energetic_components import Component, EnergyItem
from EnergyHouseCostModel.energetic_components import PV
from EnergyHouseCostModel.energy_cost import EnergyCostProjection
from EnergyHouseCostModel.energy_cost import compute_cost
from EnergyHouseCostModel.uncertain import get_uncertain_parameters
from EnergyHouseCostModel.uncertain import set_uncertain_parameters

class EnergyScenario(MDODiscipline):

    def __init__(self, energy_items, duration_years):
        super().__init__("energy_scenario", grammar_type="SimpleGrammar")
        self.duration_years = duration_years
        input_data = {}
        for name, param in get_uncertain_parameters(energy_items).items():
            input_data.update({name: param.value})
        self.input_grammar.update_from_data(input_data)
        self.output_grammar.update({"total_cost": float})

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
    pv = PV("pv", 5000., 0.)

    energy_items_1 = [EnergyItem(CONSUMED_KWH_PER_YEAR_HEATING, boiler, gas_cost),
        EnergyItem(CONSUMED_KWH_PER_YEAR_HOT_WATER, hot_water_tank, electricity_cost),
        EnergyItem(0., pv, electricity_cost, is_produced=True)]

    input_data = {}
    for name, param in get_uncertain_parameters(energy_items_1).items():
        input_data.update({name: param.value})

    scenario = EnergyScenario(energy_items_1, DURATION_YEARS)
    scenario.execute(input_data)
    print(scenario.get_output_data()["total_cost"])
    input_data["percentage_increase"] = 15.
    input_data["curve_1"] = 0.25
    scenario.execute(input_data)
    print(scenario.get_output_data()["total_cost"])
