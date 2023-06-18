from pathlib import Path
from pytest import approx
from energy_house_cost.energetic_components import Component
from energy_house_cost.database import DB_PATH
from energy_house_cost.energy_cost import EnergyCostProjection


def test_consumption():
    c = Component(DB_PATH / "mock.json")
    assert c._name == "mock"
    assert c.parameters["mock.slope"].value == 0.2


def test_energy_cost_user_points():
    c = EnergyCostProjection(DB_PATH / "mock_energy_cost_user_points.json", 15)
    assert c._name == "mock_user_points"
    assert c.compute(2, 1.) == approx(0.25)


def test_energy_cost_linear():
    c = EnergyCostProjection(DB_PATH / "mock_energy_cost_linear.json", 15)
    assert c._name == "mock_linear"
    assert c.compute(2, 1.) == approx(0.5 * (0.2 + 2. * 2 + 0.2 + 3. * 2))

