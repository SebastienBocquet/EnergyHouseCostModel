import numpy as np
from matplotlib import pyplot as plt
from numpy import array, interp, allclose, insert
from numpy.typing import NDArray


class EnergyCostProjection():
    """Estimates the cost of energy in the future."""

    def __init__(
            self,
            energy_name: str,
            initial_cost_one_kwh: float,
            profile_type: str,
            slope: float = 0.,
            percentage_of_increase_per_year: float = 0.,
            curve: tuple[NDArray, NDArray] | None = None,
            injected_price_per_kwh = 0.):
        """
        Args:
            initial_cost_one_kwh: current cost of one kWh of energy.
            profile_type: type of profile for the cost of energy in the future.
            Should be 'linear', 'power' or 'curve'.
            slope: slope in euros per year for a linear profile.
            percentage_of_increase_per_year: percentage of increase each year for the power profile.
            curve: a tuple of two Numpy arrays. The first array defines the x-axis in year,
            and the second array defines the cost in euros of one kWh.

        """
        self.energy_name = energy_name
        self.initial_cost_one_kwh = initial_cost_one_kwh
        self.profile_type = profile_type
        self.slope = slope
        self.percentage_of_increase_per_year = percentage_of_increase_per_year
        self.curve = curve
        self.injected_price_per_kwh = injected_price_per_kwh

    def compute_linear_profile_value(self, year):
        return self.initial_cost_one_kwh + self.slope * year

    def compute_power_profile_value(self, year):
        return self.initial_cost_one_kwh * (1 + 0.01 * self.percentage_of_increase_per_year)**year

    def compute(
            self,
            year_n: int,
            energy_kwh: float
    ):
        """Computes price in euros during ``year_n`` of a given number of kWh of energy.

        Args:
            year_n: number of year in the future at which price is computed.
            energy_kwh: number of kWh for which price is computed.

        Returns: price of ``energy_kWh`` of energy at year ``year_n``.

        """
        if self.profile_type == "linear":
            price_one_kwh_january = self.compute_linear_profile_value(year_n)
            price_one_kwh_december = self.compute_linear_profile_value(year_n + 1)
            price_one_kwh_at_year_n = 0.5 * (price_one_kwh_january + price_one_kwh_december)
        elif self.profile_type == "power":
            price_one_kwh_january = self.compute_power_profile_value(year_n)
            price_one_kwh_december = self.compute_power_profile_value(year_n + 1)
            price_one_kwh_at_year_n = 0.5 * (price_one_kwh_january + price_one_kwh_december)
        elif self.profile_type == "curve":
            if self.curve[0][-1] < year_n:
                raise ValueError(f"Last value of year axis of curve must be greater than arg year_n + 1 which is {year_n}.")
            insert(self.curve[0], 0, 0)
            insert(self.curve[1], 0, self.initial_cost_one_kwh)
            # Compute price as the half sum of the price at beginning of the year and price at the end of the year.
            price_one_kwh_january = interp(array([year_n]), self.curve[0], self.curve[1])[0]
            price_one_kwh_december = interp(array([year_n + 1]), self.curve[0], self.curve[1])[0]
            price_one_kwh_at_year_n = 0.5 * (price_one_kwh_january + price_one_kwh_december)
        else:
            raise ValueError("The profile type should be 'linear', 'power' or 'curve'.")
        return energy_kwh * price_one_kwh_at_year_n

    def compute_injected(
            self,
            year_n: int,
            energy_kwh: float
    ):
        return self.injected_price_per_kwh * energy_kwh

    def __repr__(self):
        return f"{self.energy_name}"

    def plot(self, nb_years, show=False, save=False):
        if show or save:
            x = np.linspace(0, nb_years, nb_years + 1)
            y = np.empty((len(x)))
            for i, year in np.ndenumerate(x):
                y[i] = self.compute(year, 1)

            fig, ax = plt.subplots()
            ax.plot(x, y, linewidth=2.0)
            if show:
                plt.show()
            if save:
                plt.savefig(f"{self.energy_name}.png")
            plt.close()


class EnergyCost:

    UNCERTAIN_PARAMETERS = {}

    def __init__(self, duration_years: int):
        self.duration_years = duration_years
        self.cost = None

    def update(self):
        """"""


def component_integrated_cost(energy_item, duration_years):
    """Computes the integrated cost in euros over ``duration_years`` of an energy item.

    Args:
        energy_item: an energy item (hot water, heating, electricity equipments etc...)
        duration_years: the period in years over which the cost is computed.

    Returns:
        total_cost: the integrated cost in euros of an energy item over ``duration_years``.
        cost_evolution: the cost in euros per year of an energy item.

    """
    energy_kwh = energy_item.component.energy_consumption(energy_item.energy_value, energy_item.is_produced)
    energy_kwh_injected = energy_item.component.injected_energy()
    cost_evolution = np.zeros((duration_years))

    for year in range(0, duration_years):
        cost_evolution[year] = energy_item.energy_cost.cost.compute(year, energy_kwh)
        if energy_item.energy_cost.energy_name == "electricity":
            cost_evolution[year] -= energy_item.energy_cost.compute_injected(year, energy_kwh_injected)
        if year > 0:
            cost_evolution[year] += energy_item.component.maintenance_cost_per_year
    cost_evolution[0] += energy_item.component.initial_install_cost

    total_cost = np.sum(cost_evolution)

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
    print(f"Detailed cost in kWh per year is \n{[i for i in energy_items]}")

    if show or save:
        component_names = []
        for item in energy_items:
            component_names.append(item.component.name)
        plot_integrated_cost_per_component(component_names, cost_per_year_per_component, duration_years)

    return total_cost, cost_per_year_per_component

