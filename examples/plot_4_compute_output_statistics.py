"""
4. Compute output statistics
============================

.. image:: /_static/map_5.PNG

Now, we can post-process the samples stored in the file *dataset.pkl*.
For that, we can use ``pickle`` to read it and get the corresponding :class:`Dataset`:
"""
from pickle import load

from numpy import array

with open("dataset.pkl", "rb") as f:
    dataset = load(f)

print(dataset)


# %%
# .. seealso::
#
#    `Examples about dataset <https://gemseo.readthedocs.io/en/stable/examples/dataset/index.html>`__
#
# Export to Pandas DataFrame
# --------------------------
# This dataset can easily be converted to a `Pandas <https://pandas.pydata.org/>`__ ``DataFrame``:
dataframe = dataset.export_to_dataframe()
dataframe
# %%
# from which we can get elementary statistics
# (mean, median, standard deviation, quartiles, minimum and maximum):
df_statistics = dataframe.describe()
df_statistics
# %%
# People used to Pandas can go much further in terms of data analysis
# (filtering, plotting, sorting, ...).
#
# Compute statistics
# ------------------
# One can create an :class:`EmpiricalStatistics` or :class:`ParametricStatistics` instance
# to get specific statistics for specific names, e.g. ``"max_RF_at_BC"``:
from gemseo.uncertainty.api import create_statistics

name = "total_cost"
empirical_statistics = create_statistics(dataset, variables_names=[name])
parametric_statistics = create_statistics(
    dataset,
    variables_names=[name],
    tested_distributions=["Uniform", "Triangular", "Normal"],
    fitting_criterion="Kolmogorov"
)
# %%
# Given the families of probability distributions,
# the :class:`ParametricStatistics` looks for the one that best fits the data.
parametric_statistics.plot_criteria(name)
# %%
# Here, this is a Gaussian distribution:
#
# .. image:: /_static/fitting.png
#
# From these statistics toolbox,
# we can compute the great classics like the mean and standard deviation:
print(empirical_statistics.compute_mean()[name][0])
print(parametric_statistics.compute_mean()[name][0])
print(empirical_statistics.compute_standard_deviation()[name][0])
print(parametric_statistics.compute_standard_deviation()[name][0])

# %%
# but also mixes of these statistics,
# such as the coefficient of variation,
# a.k.a. relative standard deviation (standard deviation divided by the mean):
print(empirical_statistics.compute_variation_coefficient()[name][0])
print(parametric_statistics.compute_variation_coefficient()[name][0])

# %%
# or a margin,
# e.g. "3-sigma" (mean + 3 x standard deviation):
print(empirical_statistics.compute_margin(3)[name][0])
print(parametric_statistics.compute_margin(3)[name][0])

# %%
# From a reliability point of view,
# we can compute quantiles:
print(empirical_statistics.compute_quantile(0.8)[name][0])  # 80% of the values are lower than this one
print(parametric_statistics.compute_quantile(0.8)[name][0])  # 80% of the values are lower than this one

# %%
# quartiles (e.g. the 3:
print(empirical_statistics.compute_quartile(3)[name][0])  # 75% of the values are lower than this one
print(parametric_statistics.compute_quartile(3)[name][0])  # 75% of the values are lower than this one
# %%
# percentiles:
print(empirical_statistics.compute_percentile(23)[name][0])  # 23% of the values are lower than this one
print(parametric_statistics.compute_percentile(23)[name][0])  # 23% of the values are lower than this one
# %%
# as well as probabilities to exceed a threshold:
print(empirical_statistics.compute_probability({name: array([0.006])})[name])
print(parametric_statistics.compute_probability({name: array([0.006])})[name])
# %%
# and probabilities to not exceed it:
print(empirical_statistics.compute_probability({name: array([0.006])}, greater=False)[name])
print(parametric_statistics.compute_probability({name: array([0.006])}, greater=False)[name])
# %%
# .. note::
#
#    In the case of multidimensional variables,
#    :class:`Statistics` compute all the statistics by component
#    except for the probability which is the joint probability,
#    i.e. the probability that all the components exceed (or not) the threshold.
#
# Visualization
# -------------
# .. image:: /_static/map_6.PNG
#
import matplotlib.pyplot as plt
input_names = dataset.get_names("inputs")
output_names = dataset.get_names("outputs")
# %%
# Scatter matrix
# ~~~~~~~~~~~~~~
dataset.plot("ScatterMatrix", show=False, variable_names=input_names+[name])
# Workaround for HTML rendering, instead of ``show=True``
plt.show()
# %%
# Boxplot
# ~~~~~~~
dataset.plot(
    "Boxplot",
    show=False,
    variables=output_names,
    scale=True,
    center=True,
    use_vertical_bars=False
)
# Workaround for HTML rendering, instead of ``show=True``
plt.show()

# %%
# Line plot
# ~~~~~~~~~
dataset.plot(
    "YvsX",
    show=False,
    x="electricity_cost.curve_1",
    y=name
)
# Workaround for HTML rendering, instead of ``show=True``
plt.show()

# %%
# Surface plot
# ~~~~~~~~~~~~
dataset.plot(
    "ZvsXY",
    show=False,
    x="electricity_cost.curve_1",
    y="electricity_cost.curve_2",
    z=name
)
# Workaround for HTML rendering, instead of ``show=True``
plt.show()

# %%
# Parallel coordinates
# ~~~~~~~~~~~~~~~~~~~~
from gemseo.core.dataset import Dataset

normalized_dataset = Dataset()
for _name in input_names+[name]:
    normalized_dataset.add_variable(_name, dataset[_name])

normalized_dataset = normalized_dataset.get_normalized_dataset()
normalized_dataset.plot(
    "ParallelCoordinates",
    classifier=name,
    lower=0.4,
    color=["b", "r"],
    show=False
)
# Workaround for HTML rendering, instead of ``show=True``
plt.show()
