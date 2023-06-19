"""
5. Run a Morris sensitivity analysis
====================================

.. image:: /_static/map_7.PNG

Lastly,
we can look at the sensitivity of an output,
e.g. ``"max_RF_at_BC"``,
to the random inputs.

For instance,
we can compute sensitivity indices with the Morris method.

.. note::

   The Morris method compares the mean and variation of finite differences
   associated with the different uncertain inputs:

   - the higher the mean, the greater the effect of the uncertain input,
   - the higher the variation, the more the uncertain variable plays a non-linear role
     (alone or interaction with another uncertain variable).

"""
from gemseo_uq_awareness.bolted_joint_discipline import BoltedJointModel
from gemseo_uq_awareness.uncertain_space import UncertainSpace
from gemseo.uncertainty.sensitivity.morris.analysis import MorrisAnalysis
from gemseo.api import configure_logger

LOGGER = configure_logger(message_format="%(levelname)8s: %(message)s", filename="6_sensitivity_morris.log", filemode="w")

discipline = BoltedJointModel()
uncertain_space = UncertainSpace()

from gemseo.uncertainty.api import create_sensitivity_analysis

output_names = [
    "max_RF_at_BC", "max_SG1", "max_SG2", "max_SG3", "max_SG4", "max_FL1", "max_FL2"
]

sensitivity = create_sensitivity_analysis(analysis="MorrisAnalysis",
                                          disciplines=[discipline],
                                          parameter_space=uncertain_space,
                                          n_replicates=5)


# %%
# Note that we can save the results
sensitivity.save("morris_analysis")

# %%
# and post-process them later:
analysis = MorrisAnalysis.load("morris_analysis")

analysis.plot("max_SG1", save=False, show=True)

# %%
#
# .. image:: /_static/morris_analysis_2.png
# We can also repeat this analysis for another output.

analysis.plot("max_RF_at_BC", save=True, show=True)

# %%
#
# .. image:: /_static/morris_analysis.png
#
#
# Other plots are available:

analysis.plot_radar("max_SG1", save=False, show=True)

# %%
#
# .. image:: /_static/morris_analysis_SG1_radar.png
# We can also repeat this analysis for another output.

analysis.plot_radar("max_RF_at_BC", save=True, show=True)

# %%
#
# .. image:: /_static/morris_analysis_RF_at_BC_radar.png
#