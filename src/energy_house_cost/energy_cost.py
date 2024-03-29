from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar
from typing import Iterable
from typing import Mapping

import numpy as np
from matplotlib import pyplot as plt
from numpy import array
from numpy import interp

from energy_house_cost.uncertain import UncertainParameter


class Component:
    _uncertain_parameters = None

    UNCERTAIN_PARAMETERS: ClassVar[Mapping[str, UncertainParameter] | None] = None

    _RESERVED_KEYS = ["name"]

    def __init__(self, data_file_path: Path | None = None):
        data = json.load(open(data_file_path)) if data_file_path is not None else {}
        self._data = data
        self._uncertain_parameters = {}

        if "name" in data.keys():
            self.name = data["name"]
        else:
            self.name = self.__class__.__name__

        for k, v in data.items():
            if k not in self._RESERVED_KEYS:
                param_name = f"{self.name}.{k}"
                param = self._parse_single_key(param_name, v)
                self._uncertain_parameters[param_name] = param

    def _parse_single_key(self, name, v):
        min_value = None
        max_value = None
        if isinstance(v, dict):
            value = v["value"]
            if "min" in v.keys():
                min_value = v["min"]
            if "max" in v.keys():
                max_value = v["max"]
        else:
            value = v
        return UncertainParameter(name, value, min_value, max_value)

    @property
    def parameters(self) -> Iterable[UncertainParameter]:
        return self._uncertain_parameters


class EnergyCostProjection(Component):
    """Estimates the cost of energy in the future."""

    _RESERVED_KEYS = ["name", "energy_name", "profile_type", "points"]

    def __init__(self, data_file_path: Path, duration_years):
        """Constructor.

        Args:
            data_file_path: The path to a json file defining the cost.
            duration_years: The number of years over which the cost projection is computed.
        """
        super().__init__(data_file_path)
        self.energy_name = self._data["energy_name"]
        self.duration_years = duration_years
        self.profile_type = self._data["profile_type"]
        if self.profile_type == "user_points":
            for i, p in enumerate(self._data["points"]):
                param_name = f"{self.name}.point{i}"
                param = self._parse_single_key(param_name, p)
                self._uncertain_parameters[param_name] = param

    def compute_linear_profile_value(self, year: int):
        return (
            self._uncertain_parameters[f"{self.name}.initial_cost_one_kwh"].value
            + self._uncertain_parameters[f"{self.name}.slope"].value * year
        )

    def compute_power_profile_value(self, year: int):
        return (
            self._uncertain_parameters[f"{self.name}.initial_cost_one_kwh"].value
            * (
                1
                + 0.01
                * self._uncertain_parameters[
                    f"{self.name}.percentage_of_increase_per_year"
                ].value
            )
            ** year
        )

    def __compute_band_value(self, value_start, value_end):
        return 0.5 * (value_start + value_end)

    def compute(self, year_n: int, energy_kwh: float) -> float:
        """Computes price in euros during ``year_n`` of a given number of kWh of energy.

        Args:
            year_n: number of year in the future at which price is computed.
            energy_kwh: number of kWh for which price is computed.

        Returns: price of ``energy_kWh`` of energy at year ``year_n``.
        """
        if self.profile_type == "linear":
            price_one_kwh_january = self.compute_linear_profile_value(year_n)
            price_one_kwh_december = self.compute_linear_profile_value(year_n + 1)
            price_one_kwh_at_year_n = self.__compute_band_value(
                price_one_kwh_january, price_one_kwh_december
            )
        elif self.profile_type == "power":
            price_one_kwh_january = self.compute_power_profile_value(year_n)
            price_one_kwh_december = self.compute_power_profile_value(year_n + 1)
            price_one_kwh_at_year_n = self.__compute_band_value(
                price_one_kwh_january, price_one_kwh_december
            )
        elif self.profile_type == "user_points":
            profile = []
            profile.append(
                (0.0, self._uncertain_parameters[f"{self.name}.initial_cost_one_kwh"])
            )
            for i, p in enumerate(self._data["points"]):
                value = self._uncertain_parameters[f"{self.name}.point{i}"]
                profile.append((p["year"], value))
            profile_y_values = [v[1].value for v in profile]
            year_axis = [v[0] for v in profile]
            if year_axis[-1] < year_n:
                raise ValueError(
                    f"Last value of year axis of curve must be greater than arg"
                    f" year_n + 1 which is {year_n}."
                )
            # Compute price as the half sum of the price at beginning of the year and
            # price at the end of the year.
            price_one_kwh_january = interp(
                array([year_n]), year_axis, profile_y_values
            )[0]
            price_one_kwh_december = interp(
                array([year_n + 1]), year_axis, profile_y_values
            )[0]
            price_one_kwh_at_year_n = self.__compute_band_value(
                price_one_kwh_january, price_one_kwh_december
            )
        else:
            raise ValueError(
                "The profile type should be 'linear', 'power' or 'user_points'."
            )

        return energy_kwh * price_one_kwh_at_year_n

    def compute_injected(self, year_n: int, energy_kwh: float) -> float:
        return (
            self._uncertain_parameters[f"{self.name}.injected_price_per_kwh"].value
            * energy_kwh
        )

    def plot(self, nb_years, show=False, save=False):
        if show or save:
            x = np.linspace(0, nb_years, nb_years + 1)
            y = np.empty(len(x))
            for i, year in np.ndenumerate(x):
                y[i] = self.compute(year, 1)

            fig, ax = plt.subplots()
            ax.plot(x, y, linewidth=2.0)
            if show:
                plt.show()
            if save:
                plt.savefig(f"{self.energy_name}.png")
            plt.close()
