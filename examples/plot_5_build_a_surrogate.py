"""
6. Use a surrogate model
========================

.. image:: /_static/map_8.PNG

The computational cost of the simulator limits the sampling size.
For instance,
we cannot get 10'000 evaluations to estimate sensitivity indices,
e.g. Sobol' indices.

.. note::

   A Sobol' index measures the percentage of output variance
   explained by one or several uncertain inputs.

but use the previous dataset to build a surrogate model, cheap to evaluate.

Train the surrogate model
-------------------------
"""
from pickle import load
from pprint import pprint

from gemseo.api import create_surrogate
from gemseo.mlearning.qual_measure.r2_measure import R2Measure
from gemseo.utils.data_conversion import split_array_to_dict_of_arrays

with open("filtered_dataset.pkl", "rb") as f:
    dataset = load(f)

output_names = dataset.get_names("outputs")
output_names.remove("error")

surrogate = create_surrogate("RBFRegressor", dataset, output_names=output_names, function="thin_plate")
regression_model = surrogate.regression_model

# %%
# Assess the quality of the surrogate model
# -----------------------------------------
# The quality of the surrogate model can be assessed with various metrics,
# e.g. the mean-squared error (MSE), the mean absolute error (MSE) and the R2.
# The latter is of the form "1 - MSE / noise"; the greater, the better.
quality = R2Measure(regression_model, fit_transformers=True)
# %%
# We can evaluate this metrics as a training measure:
r2_learn = quality.evaluate_learn()
pprint(split_array_to_dict_of_arrays(r2_learn, dataset.sizes, dataset.get_names("outputs")))
# %%
# or a validation one (here the cross-validation):
r2_cv = quality.evaluate_kfolds(randomize=True)
pprint(split_array_to_dict_of_arrays(r2_cv, dataset.sizes, dataset.get_names("outputs")))
# %%
# .. note::
#
#    We could also evaluate
#    a leave-one-out error with :meth:`R2Measure.evaluate_loo`
#    or a test error with :meth:`R2Measure.evaluate_test` and a test dataset.
#
# Save your model
# ---------------
# This surrogate model can be saved on the disk as any other :class:`MDODiscipline`:
surrogate.serialize("surrogate_model.pkl")
# %%
#
from gemseo.api import import_discipline

loaded_surrogate = import_discipline("surrogate_model.pkl")