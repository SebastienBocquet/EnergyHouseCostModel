from energy_house_cost.energy_cost import EnergyCostProjection
from energy_house_cost.uncertain import UncertainParameter


class ElectricityCostProjection(EnergyCostProjection):
    """Estimates the cost of electricity in the future."""

    ENERGY_NAME = "electricity"

    PROFILE_TYPE = "curve"

    UNCERTAIN_PARAMETERS = {
        "initial_cost_one_kwh": UncertainParameter(0.24),
        "curve_1": UncertainParameter(0.28, 0.24, 0.32),
        "curve_2": UncertainParameter(0.32, 0.28, 0.36),
        "curve_3": UncertainParameter(0.36, 0.28, 0.4),
        "injected_price_per_kwh": UncertainParameter(0.13)
    }


class GasCostProjection(EnergyCostProjection):
    """Estimates the cost of gas in the future."""

    ENERGY_NAME = "gas"

    PROFILE_TYPE = "power"

    UNCERTAIN_PARAMETERS = {
        "initial_cost_one_kwh": UncertainParameter(0.1043),
        "percentage_of_increase_per_year": UncertainParameter(10., 5., 15.),
    }
