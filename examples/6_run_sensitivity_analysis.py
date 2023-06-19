"""
7. Run a Sobol' sensitivity analysis
====================================

.. image:: /_static/map_7.PNG

Lastly,
we can look at the sensitivity of an output,
e.g. ``"max_RF_at_BC"``,
to the random inputs.

For instance,
we can compute Sobol' indices.

.. note::

   A Sobol' index measures the percentage of output variance
   explained by one or several uncertain inputs.
"""
from gemseo.api import import_discipline

surrogate = import_discipline("surrogate_model.pkl")

from gemseo.uncertainty.api import create_sensitivity_analysis
from gemseo_uq_awareness.uncertain_space import UncertainSpace

analysis = create_sensitivity_analysis(
    "SobolAnalysis", [surrogate], UncertainSpace(), n_samples=10000
)
analysis.compute_indices()
analysis.plot("max_SG1", save=False, show=True)

# %%
#
# .. image:: /_static/sobol_analysis_2.png
#
# We can also repeat this analysis for another output.

analysis.plot("max_RF_at_BC", save=False, show=True)

# %%
#
# .. image:: /_static/sobol_analysis.png
#