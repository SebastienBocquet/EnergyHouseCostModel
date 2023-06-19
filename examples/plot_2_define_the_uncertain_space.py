"""
2. Define the uncertain space
=============================

.. image:: /_static/map_3.PNG

In addition to the discipline,
we need to define the uncertain space from the random variables.

In this case,
we consider independent random variables triangularly distributed:

.. include:: /probability_space.rst

.. note::

   A triangular distribution is a probability distribution
   defined by a lower bound, a mode and an upper bound:

   .. figure:: /_static/triangular_distribution.png

      Probability density function of the random variable *friction*
      distributed as a triangular distribution :math:`\mathcal{T}(0.1, 0.2, 0.3)`.

.. seealso::

   We can use any distribution of
   `OpenTURNS <https://openturns.github.io/openturns/latest/user_manual/probabilistic_modelling.html>`__
   and
   `SciPy <https://docs.scipy.org/doc/scipy/reference/stats.html#probability-distributions>`__.

Define the uncertain space
--------------------------

A :class:`ParameterSpace` can store
both deterministic variables with :meth:`add_variable`
and random variables with :meth:`add_random_variable`.
Here, we propose to derive a new class and instantiate it whenever necessary.
"""
from pprint import pprint

from gemseo.algos.parameter_space import ParameterSpace
from gemseo.core.dataset import Dataset
from matplotlib import pyplot as plt

from energy_house_cost.uncertain import get_uncertain_parameters
from house_energy_cost import energetic_scenario


class UncertainSpace(ParameterSpace):
    """The space spanned by the random variables."""

    def __init__(self):
        super().__init__()
        for name, param in get_uncertain_parameters(energetic_scenario._energy_items).items():
            if not param.is_constant:
                self.add_random_variable(
                    name,
                    "OTTriangularDistribution",
                    minimum=param.min_value,
                    maximum=param.max_value,
                    mode=param.default_value
                )


if __name__ == "__main__":

    # %%
    # .. note::
    #
    #    For a one-shot use,
    #    we can also instantiate a uncertain space
    #    without subclassing :class:`ParameterSpace`.
    #
    #    .. code::
    #
    #       from gemseo.api import create_parameter_space
    #
    #       uncertain_space = create_parameter_space()
    #       for (name, minimum, mode, maximum) in [
    #           ("plate_len", 210, 214.3, 220.0),
    #             ("plate_wid", 50.5, 50.8, 51.0),
    #             ("plate_thick", 2.9, 3.0, 3.1),
    #             ("friction", 0.1, 0.2, 0.3),
    #             ("boundary", 57000.0, 60000.0, 63000.0),
    #             ("huth_factor", 0.95, 1., 1.05),
    #             ("preload", -10500., -10000., -9500.)
    #       ]:
    #           uncertain_space.add_random_variable(
    #               name,
    #               "OTTriangularDistribution",
    #               minimum=minimum,
    #               maximum=maximum,
    #               mode=mode
    #           )
    #
    # Discover this uncertain space
    # -----------------------------
    # Then,
    # we can instantiate this uncertain space:
    uncertain_space = UncertainSpace()
    # %%
    # Print
    # ~~~~~
    # and check its content by printing it:
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
    dataset.set_from_array(uncertain_space.compute_samples(200),uncertain_space.uncertain_variables)

    # %%
    # For instance,
    # a scatter graph plotting these 200 realizations for a pair of variables
    dataset.plot("Scatter", x="electricity_cost.curve_1", y="electricity_cost.curve_2", show=False, save=False)
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()

    # %%
    # or a scatter matrix
    # where the diagonal blocks represent the histograms of the random variables
    # while the other blocks represents the value of a variable versus another.
    dataset.plot("ScatterMatrix", show=False, save=False)
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()
    # %%
    # .. seealso::
    #
    #    `Examples of visualization tools <https://gemseo.readthedocs.io/en/stable/examples/dataset/index.html>`__
    #    to post-process a :class:`Dataset`.
    #