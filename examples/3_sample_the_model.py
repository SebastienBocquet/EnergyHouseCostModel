"""
3. Sample the model
===================

"""
from __future__ import annotations

from gemseo.api import configure_logger
from house_energy_cost import scenario

from examples.plot_2_define_the_uncertain_space import UncertainSpace

LOGGER = configure_logger(
    message_format="%(levelname)8s: %(message)s",
    filename="3_sampling.log",
    filemode="w",
)

if __name__ == "__main__":
    uncertain_space = UncertainSpace()

    from gemseo.api import create_scenario

    output_names = ["total_cost"]
    scenario = create_scenario(
        [scenario],
        "DisciplinaryOpt",
        output_names[0],
        uncertain_space,
        scenario_type="DOE",
    )
    for name in output_names[1:]:
        scenario.add_observable(name)

    scenario.execute({"algo": "OT_OPT_LHS", "n_samples": 100})
    dataset = scenario.export_to_dataset(opt_naming=False)

    # %%
    # Save the results
    # ----------------
    # Lastly,
    # we can save the result in the file ``"dataset.pkl"`` with the library ``pickle``.
    from pickle import dump

    with open("dataset.pkl", "wb") as f:
        dump(dataset, f)
