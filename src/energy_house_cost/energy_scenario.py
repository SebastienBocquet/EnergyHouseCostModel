from dataclasses import dataclass
from pprint import pprint

import numpy as np
from gemseo.core.discipline import MDODiscipline
from matplotlib import pyplot as plt
from numpy import atleast_1d

from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energetic_components import ProductorComponent
from energy_house_cost.energy_cost import EnergyCostProjection
from energy_house_cost.uncertain import get_uncertain_parameters
from energy_house_cost.uncertain import set_uncertain_parameters


class EnergyScenario(MDODiscipline):

    def __init__(self, energy_items, duration_years):
        super().__init__("energy_scenario", grammar_type="SimpleGrammar")
        self.duration_years = duration_years
        self._energy_items = energy_items
        input_data = {}
        for name, param in get_uncertain_parameters(energy_items).items():
            input_data.update({name: atleast_1d(param.value)})
        self.input_grammar.update_from_data(input_data)
        self.default_inputs = input_data
        # self.output_grammar.update({"total_cost": float,
        # "cost_per_year_per_component": list})
        self.output_grammar.update_from_data({"total_cost": atleast_1d(0.)})

    def _run(self):
        input_data = self.get_input_data()
        set_uncertain_parameters(self._energy_items, input_data)
        total_cost, cost_per_year_per_component = \
            compute_cost(self._energy_items, self.duration_years, show=False)
        # self.store_local_data(**{"total_cost": total_cost,
        #     "cost_per_year_per_component": cost_per_year_per_component})
        self.store_local_data(**{"total_cost": atleast_1d(total_cost)})


@dataclass
class EnergyItem:
    """An energy item. The energetic profile is defined as a list of energy items."""
    energy_value: float
    component: EnergeticComponent
    energy_cost: EnergyCostProjection
    is_produced: bool = False
    integrated_cost: float = 0.

    def __repr__(self):
        return f"{self.component.name} {self.component.get_summary(self.component.compute(self.energy_value, self.is_produced))}" \
               f" of {self.energy_cost.name}\n" \
               f" which represents {(self.integrated_cost / self.energy_cost.duration_years):.0f}" \
               f" euros (average per year, including initial cost and maintenance)\n"


def component_integrated_cost(energy_item, duration_years):
    """Computes the integrated cost in euros over ``duration_years`` of an energy item.

    Args:
        energy_item: an energy item (hot water, heating, electricity equipments etc...)
        duration_years: the period in years over which the cost is computed.

    Returns:
        total_cost: the integrated cost in euros of an energy item over ``duration_years``.
        cost_evolution: the cost in euros per year of an energy item.

    """
    energy_kwh = energy_item.component.compute(energy_item.energy_value, energy_item.is_produced)
    cost_evolution = np.zeros((duration_years))

    for year in range(0, duration_years):
        cost_evolution[year] = energy_item.energy_cost.compute(year, energy_kwh)
        if isinstance(energy_item.component, ProductorComponent):
            energy_kwh_injected = energy_item.component.injected_energy()
            cost_evolution[year] -= energy_item.energy_cost.compute_injected(year, energy_kwh_injected)
        if year > 0:
            cost_evolution[year] += energy_item.component.maintenance_cost_per_year
    cost_evolution[0] += energy_item.component.initial_install_cost

    total_cost = np.sum(cost_evolution)
    energy_item.integrated_cost = total_cost

    return total_cost, cost_evolution

def plot_integrated_cost_per_component(component_names, cost_per_year_per_component, duration_years):

    columns = component_names
    columns = tuple(columns)
    rows = np.linspace(0, duration_years - 1, duration_years)

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0.1, 0.5, len(rows)))
    n_rows = len(cost_per_year_per_component)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.zeros(len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        plt.bar(index, cost_per_year_per_component[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + cost_per_year_per_component[row]
        cell_text.append(['%1.1f' % (x / 1) for x in y_offset])
    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    rows = rows[::-1]
    cell_text.reverse()

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.5)

    plt.ylabel(f"Cost in euros")
    # plt.yticks(values * value_increment, ['%d' % val for val in values])
    plt.xticks([])
    plt.title('Integrated cost by component')

    plt.show()

def compute_cost(energy_items, duration_years, show=True, save=False):
    total_cost = 0.
    cost_per_year_per_component = np.empty((duration_years, len(energy_items)))
    for i, item in enumerate(energy_items):
        total_cost_of_component, cost_evolution_of_component = component_integrated_cost(item, duration_years)
        cost_per_year_per_component[:,i] = cost_evolution_of_component
        total_cost += total_cost_of_component
    print(f"Integrated cost is {total_cost} euros over {duration_years} years.")
    print(f"Detailed cost in kWh per year")
    pprint([i for i in energy_items])

    # if show or save:
    #     component_names = []
    #     for item in energy_items:
    #         component_names.append(item.component.name)
    #     plot_integrated_cost_per_component(component_names, cost_per_year_per_component, duration_years)

    return total_cost, cost_per_year_per_component



