from __future__ import annotations

from energy_house_cost.database import DB_PATH
from energy_house_cost.energetic_components import EnergeticComponent
from energy_house_cost.energy_cost import EnergyCostProjection
from energy_house_cost.energy_scenario import EnergyItem
from energy_house_cost.energy_scenario import EnergyScenario
from pytest import approx


def test_energy_cost_user_points():
    c = EnergyCostProjection(DB_PATH / "mock_energy_cost_user_points.json", 15)
    assert c.name == "mock_user_points"
    assert c.compute(2, 1.0) == approx(0.25)


def test_energy_cost_linear():
    slope = 2.0
    initial_cost = 0.2
    c = EnergyCostProjection(DB_PATH / "mock_energy_cost_linear.json", 15)
    assert c.name == "mock_linear"
    assert c.energy_name == "electricity"
    assert c.profile_type == "linear"
    assert c.parameters["mock_linear.initial_cost_one_kwh"].value == initial_cost
    assert c.parameters["mock_linear.slope"].value == slope
    # Check that cost at year 2 is estimated at mid-year (to increase integration accuracy
    # (trapeziodal rule)).
    cost_at_year_2 = initial_cost + 2 * slope
    cost_at_year_3 = initial_cost + 3 * slope
    assert c.compute(2, 1.0) == approx(0.5 * (cost_at_year_2 + cost_at_year_3))


def test_scenario():
    duration_years = 10
    cost = EnergyCostProjection(DB_PATH / "mock_energy_cost_linear.json", 15)
    mock_component = EnergeticComponent("mock", 0.0, 0.0)
    consumed_kwh_per_year = 1e3
    energy_items = [EnergyItem(consumed_kwh_per_year, mock_component, cost)]
    scenario = EnergyScenario(energy_items, duration_years)
    scenario.execute()
    output_data = scenario.get_output_data()
    total_cost = output_data["total_cost"][0]
    # Check total cost versus integration of cost by trapezoidal rule (which is half sum
    # of the final value plus the initial value for this linear profile).
    assert total_cost == approx(
        consumed_kwh_per_year
        * duration_years
        * 0.5
        * (0.2 + (0.2 + duration_years * 2))
    )
