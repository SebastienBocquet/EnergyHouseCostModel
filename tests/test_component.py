from EnergyHouseCostModel.energetic_components import Component, EnergyItem


def test_consumption():
    energy_value = 1.
    c = Component("mock", 0, 0, 0.5)
    assert c.energy_consumption(energy_value, is_produced=False) == 1
    assert c.energy_consumption(energy_value, is_produced=True) == 2


