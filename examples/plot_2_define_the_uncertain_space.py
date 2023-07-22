r"""
2. Define the uncertain space
=============================

"""
from __future__ import annotations

from pprint import pprint

from energy_house_cost.energy_item import get_uncertain_parameters
from gemseo.algos.parameter_space import ParameterSpace
from gemseo.core.dataset import Dataset
from house_energy_cost import scenario
from matplotlib import pyplot as plt


class UncertainSpace(ParameterSpace):
    """The space spanned by the random variables."""

    def __init__(self):
        super().__init__()
        for name, param in get_uncertain_parameters(scenario._energy_items).items():
            if param.is_uncertain:
                self.add_random_variable(
                    name,
                    "OTTriangularDistribution",
                    minimum=param.min_value,
                    maximum=param.max_value,
                    mode=param.default_value,
                )


if __name__ == "__main__":
    uncertain_space = UncertainSpace()
    print(uncertain_space)

    # %%
    # Sample
    # ~~~~~~
    # We can also sample this uncertain space:
    three_samples = uncertain_space.compute_samples(3, as_dict=True)
    pprint(three_samples)

    # %%
    # Post-process
    # ~~~~~~~~~~~~
    # Lastly, we can generate some visualizations from 200 realizations of the input variables:
    dataset = Dataset()
    dataset.set_from_array(
        uncertain_space.compute_samples(200), uncertain_space.uncertain_variables
    )

    # %%
    # For instance,
    # a scatter graph plotting these 200 realizations for a pair of variables
    dataset.plot(
        "Scatter",
        x="electricity_cost.slope",
        y="pv.auto_consumption_ratio",
        show=True,
        save=False,
    )
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()

    # %%
    # or a scatter matrix
    # where the diagonal blocks represent the histograms of the random variables
    # while the other blocks represents the value of a variable versus another.
    dataset.plot("ScatterMatrix", show=True, save=False)
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()
