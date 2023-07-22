"""
4. Compute output statistics
============================

"""
from __future__ import annotations

from pickle import load


if __name__ == "__main__":
    with open("dataset.pkl", "rb") as f:
        dataset = load(f)

    print(dataset)

    dataframe = dataset.export_to_dataframe()
    dataframe
    df_statistics = dataframe.describe()
    df_statistics
    from gemseo.uncertainty.api import create_statistics

    name = "total_cost"
    empirical_statistics = create_statistics(dataset, variables_names=[name])
    parametric_statistics = create_statistics(
        dataset,
        variables_names=[name],
        tested_distributions=["Uniform", "Triangular", "Normal"],
        fitting_criterion="Kolmogorov",
    )
    parametric_statistics.plot_criteria(name)
    print(empirical_statistics.compute_mean()[name][0])
    print(parametric_statistics.compute_mean()[name][0])
    print(empirical_statistics.compute_standard_deviation()[name][0])
    print(parametric_statistics.compute_standard_deviation()[name][0])

    print(empirical_statistics.compute_variation_coefficient()[name][0])
    print(parametric_statistics.compute_variation_coefficient()[name][0])

    print(empirical_statistics.compute_margin(3)[name][0])
    print(parametric_statistics.compute_margin(3)[name][0])

    print(
        empirical_statistics.compute_quantile(0.8)[name][0]
    )  # 80% of the values are lower than this one
    print(
        parametric_statistics.compute_quantile(0.8)[name][0]
    )  # 80% of the values are lower than this one

    print(
        empirical_statistics.compute_quartile(3)[name][0]
    )  # 75% of the values are lower than this one
    print(
        parametric_statistics.compute_quartile(3)[name][0]
    )  # 75% of the values are lower than this one
    print(
        empirical_statistics.compute_percentile(23)[name][0]
    )  # 23% of the values are lower than this one
    print(
        parametric_statistics.compute_percentile(23)[name][0]
    )  # 23% of the values are lower than this one

    import matplotlib.pyplot as plt

    input_names = dataset.get_names("inputs")
    output_names = dataset.get_names("outputs")
    dataset.plot("ScatterMatrix", show=False, variable_names=input_names + [name])
    plt.show()
    dataset.plot(
        "Boxplot",
        show=False,
        variables=output_names,
        scale=True,
        center=True,
        use_vertical_bars=False,
    )
    plt.show()

    # %%
    # Line plot
    # ~~~~~~~~~
    dataset.plot("YvsX", show=False, x="electricity_cost.slope", y=name)
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()

    # %%
    # Surface plot
    # ~~~~~~~~~~~~
    dataset.plot(
        "ZvsXY",
        show=False,
        x="pv.auto_consumption_ratio",
        y="electricity_cost.slope",
        z=name,
    )
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()

    # %%
    # Parallel coordinates
    # ~~~~~~~~~~~~~~~~~~~~
    from gemseo.core.dataset import Dataset

    normalized_dataset = Dataset()
    for _name in input_names + [name]:
        normalized_dataset.add_variable(_name, dataset[_name])

    normalized_dataset = normalized_dataset.get_normalized_dataset()
    normalized_dataset.plot(
        "ParallelCoordinates", classifier=name, lower=0.4, color=["b", "r"], show=False
    )
    # Workaround for HTML rendering, instead of ``show=True``
    plt.show()
