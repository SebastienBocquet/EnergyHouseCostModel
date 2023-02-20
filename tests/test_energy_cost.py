from numpy import allclose, array
from pytest import approx

from EnergyHouseCostModel.energy_cost import EnergyCostProjection, component_integrated_cost
from EnergyHouseCostModel.energetic_components import Component, EnergyItem

component = Component('component', 0., 0., production_over_consumption_ratio=None)


def test_integrated_linear_slope_0_cost_one_component():
    energy_cost = EnergyCostProjection('an energy', 0.1, 'linear', slope=0.)
    item = EnergyItem(1., component, energy_cost, is_produced=False)

    total_cost, cost_evolution = component_integrated_cost(item, 1)
    assert total_cost == approx(0.1)
    assert allclose(cost_evolution, array([0.1]))

    total_cost, cost_evolution = component_integrated_cost(item, 2)
    assert total_cost == approx(0.2)
    assert allclose(cost_evolution, array([0.1, 0.1]))

    item = EnergyItem(10., component, energy_cost, is_produced=False)
    total_cost, cost_evolution = component_integrated_cost(item, 1)
    assert total_cost == approx(0.1 * 10.)
    assert allclose(cost_evolution, array([0.1 * 10.]))


def test_integrated_linear_cost_one_component():
    energy_cost = EnergyCostProjection('an energy', 0.1, 'linear', slope=0.05)
    item = EnergyItem(1., component, energy_cost, is_produced=False)

    total_cost, cost_evolution = component_integrated_cost(item, 1)
    cost_year_0 = 0.5 * (0.1 + (0.1 + 0.05 * 1))
    assert total_cost == approx(cost_year_0)
    assert allclose(cost_evolution, array([cost_year_0]))


def test_integrated_linear_slope_0_cost_one_component_with_initial_cost():
    component = Component('component', 100., 0., production_over_consumption_ratio=None)
    energy_cost = EnergyCostProjection('an energy', 0.1, 'linear', slope=0.)
    item = EnergyItem(1., component, energy_cost, is_produced=False)

    total_cost, cost_evolution = component_integrated_cost(item, 1)
    assert total_cost == approx(100. + 0.1)
    assert allclose(cost_evolution, array([100. + 0.1]))

    component = Component('component', 0., 10., production_over_consumption_ratio=None)
    item = EnergyItem(1., component, energy_cost, is_produced=False)
    total_cost, cost_evolution = component_integrated_cost(item, 1)
    assert total_cost == approx(0.1)
    assert allclose(cost_evolution, array([0.1]))

    total_cost, cost_evolution = component_integrated_cost(item, 2)
    assert total_cost == approx(0.1 + 0.1 + 10.)
    assert allclose(cost_evolution, array([0.1, 0.1 + 10.]))
