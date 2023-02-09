from numpy import array, interp, allclose, insert
from numpy.typing import NDArray
from abc import ABC, abstractmethod


class EnergyCostProjection():
    """Estimates the cost of energy in the future."""

    def __init__(
            self,
            energy_name: str,
            initial_cost_one_kwh: float,
            profile_type: str,
            slope: float = 0.,
            percentage_of_increase_per_year: float = 0.,
            curve: tuple[NDArray, NDArray] | None = None):
        """
        Args:
            initial_cost_one_kwh: current cost of one kWh of energy.
            profile_type: type of profile for the cost of energy in the future.
            Should be 'linear', 'power' or 'curve'.
            slope: slope for a linear profile.
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

    def compute(
            self,
            year_n: int,
            energy_kwh: float
    ):
        """Computes price in euros of a given number of kWh of energy.

        Args:
            year_n: number of year in the future at which price is computed.
            energy_kwh: number of kWh for which price is computed.

        Returns: price of ``energy_kWh`` of energy at year ``year_n``.

        """
        if self.profile_type == "linear":
            price_one_kwh_at_year_n = self.initial_cost_one_kwh + self.slope * year_n
        elif self.profile_type == "power":
            price_one_kwh_at_year_n = self.initial_cost_one_kwh * (1 + self.percentage_of_increase_per_year)**year_n
        elif self.profile_type == "curve":
            if self.curve[0][0] > 1:
                raise ValueError("First value of year axis of curve must be less than one.")
            if self.curve[0][-1] < year_n:
                raise ValueError(f"Last value of year axis of curve must be greater than arg year_n which is {year_n}.")
            insert(self.curve[0], 0, 0)
            insert(self.curve[1], 0, self.initial_cost_one_kwh)
            price_one_kwh_at_year_n = interp(array([year_n]), self.curve[0], self.curve[1])[0]
        else:
            raise ValueError("The profile type should be 'linear', 'power' or 'curve'.")
        return energy_kwh * price_one_kwh_at_year_n

    def __repr__(self):
        return f"{self.energy_name}"


def component_integrated_cost(energy_item, duration_years):
    """Computes the integrated cost in euros over ``duration_years`` of an energy item.

    Args:
        energy_item: an energy item (hot water, heating, electricity equipments etc...)
        duration_years: the period in years over which the cost is computed.

    Returns: the integrated cost of an energy item.

    """
    energy_kwh = energy_item.component.energy_consumption(energy_item)
    integrated_energy_cost = 0.
    for year in range(duration_years):
        integrated_energy_cost += energy_item.energy_cost.compute(year, energy_kwh)
    total_cost = energy_item.component.initial_install_cost \
                 + duration_years * energy_item.component.maintenance_cost_per_year \
                 + integrated_energy_cost

    return total_cost

def compute_cost(energy_items, duration_years):
    integrated_cost = 0.
    for i in energy_items:
        integrated_cost += component_integrated_cost(i, duration_years)
    return integrated_cost
