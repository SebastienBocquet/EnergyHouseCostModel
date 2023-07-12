"""
3. Sample the model
===================

.. image:: /_static/map_4.PNG

Now,
we want to sample the :class:`BoltedJointDiscipline` over the :class:`UncertainSpace`
and save the input-output data on the disk.
We will post-process them in other scripts.

Create the objects
------------------
Firstly, we instantiate the :class:`BoltedJointDiscipline` and :class:`UncertainSpace`:
"""

from gemseo.api import configure_logger

from examples.plot_2_define_the_uncertain_space import UncertainSpace
from house_energy_cost import scenario

LOGGER = configure_logger(message_format="%(levelname)8s: %(message)s", filename="3_sampling.log", filemode="w")

if __name__ == "__main__":
    uncertain_space = UncertainSpace()

    # %%
    # Sample the discipline
    # ---------------------
    # Then,
    # we generate 100 input-output samples of the model
    # by sampling the discipline with a :class:`DOEScenario` executed from a design of experiments (DOE).
    # For instance,
    # we can use an optimal `latin hypercube sampling (LHS) <https://en.wikipedia.org/wiki/Latin_hypercube_sampling>`__ technique.
    #
    # .. note::
    #
    #    The LHS technique implemented by ``"OT_LHS"`` or ``"lhs"`` is stochastic:
    #    given a number of samples :math:`N` and an input space of dimension :math:`d`,
    #    executing it twice will lead to two different series of samples.
    #    Here, we are looking for the series of samples that best covers the input space
    #    (we talk about space-filling DOE);
    #    for that,
    #    we use ``"OT_OPT_LHS"`` relying on a global optimization algorithm
    #    (simulated annealing).
    #
    from gemseo.api import create_scenario

    output_names = [
        "total_cost"
    ]
    scenario = create_scenario(
        [scenario], "DisciplinaryOpt", output_names[0], uncertain_space, scenario_type="DOE"
    )
    for name in output_names[1:]:
        scenario.add_observable(name)

    scenario.execute({"algo": "OT_OPT_LHS", "n_samples": 100})
    dataset = scenario.export_to_dataset(opt_naming=False)

    # %%
    # .. note::
    #
    #    ``gemseo`` has an extension ``gemseo-mlearning`` to sample a discipline more easily:
    #
    #    .. code::
    #
    #       from gemseo_mlearning.api import sample_discipline
    #
    #       dataset = sample_discipline(discipline, uncertain_space, output_names, "OT_OPT_LHS", 20)
    #
    # .. seealso::
    #
    #    About the DOE,
    #    you can have a look to `the user guide <https://gemseo.readthedocs.io/en/stable/doe.html>`__
    #    and `the algorithms <https://gemseo.readthedocs.io/en/stable/algorithms/doe_algos.html>`__.
    #

    # %%
    # Save the results
    # ----------------
    # Lastly,
    # we can save the result in the file ``"dataset.pkl"`` with the library ``pickle``.
    from pickle import dump

    with open("dataset.pkl", "wb") as f:
        dump(dataset, f)

    # %%
    # .. seealso::
    #
    #    `Examples about dataset <https://gemseo.readthedocs.io/en/stable/examples/dataset/index.html>`__
    #