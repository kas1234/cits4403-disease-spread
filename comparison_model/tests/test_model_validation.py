import os
import random
import sys
import unittest

import networkx as nx


# --------------------------------------------------
# MAKE EXPERIMENT MODULE IMPORTABLE
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

COMPARISON_MODEL_DIR = os.path.dirname(
    CURRENT_DIR
)

EXPERIMENTS_DIR = os.path.join(
    COMPARISON_MODEL_DIR,
    "experiments"
)

if EXPERIMENTS_DIR not in sys.path:
    sys.path.insert(
        0,
        EXPERIMENTS_DIR
    )


import compare_vaccination as cv


class TestSIRVModelValidation(unittest.TestCase):

    # --------------------------------------------------
    # TEST 1
    # BETA = 0 SHOULD PREVENT SECONDARY INFECTIONS
    # --------------------------------------------------

    def test_zero_beta_has_no_secondary_infections(self):

        original_recovery_probability = (
            cv.RECOVERY_PROBABILITY
        )

        try:
            # Make recovery immediate so the test
            # finishes deterministically.
            cv.RECOVERY_PROBABILITY = 1.0

            (
                peak,
                epidemic_size,
                time_to_peak,
                duration,
            ) = cv.run_simulation(
                vaccination_rate=0.0,
                strategy="none",
                network_type="random",
                seed=cv.BASE_SEED,
                beta=0.0,
            )

            # Only patient zero should ever
            # become infected.
            self.assertEqual(
                peak,
                1
            )

            self.assertEqual(
                epidemic_size,
                1
            )

        finally:
            cv.RECOVERY_PROBABILITY = (
                original_recovery_probability
            )

    # --------------------------------------------------
    # TEST 2
    # RANDOM VACCINATION SHOULD VACCINATE
    # THE CORRECT NUMBER OF PEOPLE
    # --------------------------------------------------

    def test_random_vaccination_count(self):

        states = {
            node: "S"
            for node in range(
                cv.POPULATION
            )
        }

        random.seed(
            cv.BASE_SEED
        )

        states = cv.random_vaccination(
            states,
            0.20,
        )

        vaccinated_count = sum(
            state == "V"
            for state in states.values()
        )

        expected_count = int(
            cv.POPULATION
            * 0.20
        )

        self.assertEqual(
            vaccinated_count,
            expected_count,
        )

    # --------------------------------------------------
    # TEST 3
    # TARGETED VACCINATION SHOULD INCLUDE
    # THE HIGHEST-DEGREE NODE
    # --------------------------------------------------

    def test_targeted_vaccination_selects_hub(self):

        graph = nx.star_graph(
            cv.POPULATION - 1
        )

        states = {
            node: "S"
            for node in graph.nodes
        }

        states = cv.targeted_vaccination(
            graph,
            states,
            0.20,
        )

        vaccinated_count = sum(
            state == "V"
            for state in states.values()
        )

        expected_count = int(
            cv.POPULATION
            * 0.20
        )

        self.assertEqual(
            vaccinated_count,
            expected_count,
        )

        # Node 0 is the centre of a NetworkX
        # star graph and therefore has the
        # highest degree.
        self.assertEqual(
            states[0],
            "V",
        )

    # --------------------------------------------------
    # TEST 4
    # PATIENT ZERO MUST COME FROM THE
    # SUSCEPTIBLE POPULATION
    # --------------------------------------------------

    def test_patient_zero_is_not_vaccinated(self):

        states = {
            node: "S"
            for node in range(
                cv.POPULATION
            )
        }

        random.seed(
            cv.BASE_SEED
        )

        states = cv.random_vaccination(
            states,
            0.20,
        )

        vaccinated_before = {
            node
            for node, state
            in states.items()
            if state == "V"
        }

        states = cv.infect_patient_zero(
            states
        )

        vaccinated_after = {
            node
            for node, state
            in states.items()
            if state == "V"
        }

        infected_nodes = [
            node
            for node, state
            in states.items()
            if state == "I"
        ]

        self.assertEqual(
            len(infected_nodes),
            1,
        )

        self.assertEqual(
            vaccinated_before,
            vaccinated_after,
        )

        self.assertNotIn(
            infected_nodes[0],
            vaccinated_before,
        )

    # --------------------------------------------------
    # TEST 5
    # VACCINATED PEOPLE SHOULD NEVER
    # BECOME INFECTED
    # --------------------------------------------------

    def test_vaccinated_nodes_remain_protected(self):

        graph = nx.Graph()

        graph.add_edges_from(
            [
                (0, 1),
                (1, 2),
            ]
        )

        states = {
            0: "I",
            1: "V",
            2: "S",
        }

        random.seed(
            cv.BASE_SEED
        )

        new_states = cv.simulation_step(
            graph,
            states,
            beta=1.0,
        )

        self.assertEqual(
            new_states[1],
            "V",
        )

        # Infection cannot cross through
        # the vaccinated node.
        self.assertEqual(
            new_states[2],
            "S",
        )

    # --------------------------------------------------
    # TEST 6
    # STATE COUNTS MUST ALWAYS EQUAL
    # TOTAL POPULATION
    # --------------------------------------------------

    def test_state_counts_preserve_population(self):

        graph = nx.erdos_renyi_graph(
            n=cv.POPULATION,
            p=0.05,
            seed=cv.BASE_SEED,
        )

        states = {
            node: "S"
            for node in graph.nodes
        }

        random.seed(
            cv.BASE_SEED
        )

        states = cv.random_vaccination(
            states,
            0.20,
        )

        states = cv.infect_patient_zero(
            states
        )

        valid_states = {
            "S",
            "I",
            "R",
            "V",
        }

        for _ in range(25):

            states = cv.simulation_step(
                graph,
                states,
                beta=cv.INFECTION_PROBABILITY,
            )

            susceptible = sum(
                state == "S"
                for state
                in states.values()
            )

            infected = sum(
                state == "I"
                for state
                in states.values()
            )

            recovered = sum(
                state == "R"
                for state
                in states.values()
            )

            vaccinated = sum(
                state == "V"
                for state
                in states.values()
            )

            total = (
                susceptible
                + infected
                + recovered
                + vaccinated
            )

            self.assertEqual(
                total,
                cv.POPULATION,
            )

            self.assertTrue(
                set(
                    states.values()
                ).issubset(
                    valid_states
                )
            )

            if infected == 0:
                break

    # --------------------------------------------------
    # TEST 7
    # SAME SEED SHOULD PRODUCE
    # THE SAME RESULT
    # --------------------------------------------------

    def test_same_seed_is_reproducible(self):

        first_result = cv.run_simulation(
            vaccination_rate=0.20,
            strategy="targeted",
            network_type="scale_free",
            seed=cv.BASE_SEED,
            beta=0.20,
        )

        second_result = cv.run_simulation(
            vaccination_rate=0.20,
            strategy="targeted",
            network_type="scale_free",
            seed=cv.BASE_SEED,
            beta=0.20,
        )

        self.assertEqual(
            first_result,
            second_result,
        )

    # --------------------------------------------------
    # TEST 8
    # SIMULATION SHOULD STOP AFTER
    # INFECTIONS DISAPPEAR
    # --------------------------------------------------

    def test_simulation_stops_when_no_infected_remain(self):

        original_recovery_probability = (
            cv.RECOVERY_PROBABILITY
        )

        try:
            cv.RECOVERY_PROBABILITY = 1.0

            (
                peak,
                epidemic_size,
                time_to_peak,
                duration,
            ) = cv.run_simulation(
                vaccination_rate=0.0,
                strategy="none",
                network_type="random",
                seed=cv.BASE_SEED,
                beta=0.0,
            )

            self.assertLess(
                duration,
                cv.TIME_STEPS,
            )

            self.assertEqual(
                epidemic_size,
                1,
            )

        finally:
            cv.RECOVERY_PROBABILITY = (
                original_recovery_probability
            )

    # --------------------------------------------------
    # TEST 9
    # ALL THREE NETWORK TYPES SHOULD RUN
    # AND RETURN VALID RESULTS
    # --------------------------------------------------

    def test_all_network_types_run_successfully(self):

        network_types = [
            "random",
            "small_world",
            "scale_free",
        ]

        for network_type in network_types:

            with self.subTest(
                network=network_type
            ):

                (
                    peak,
                    epidemic_size,
                    time_to_peak,
                    duration,
                ) = cv.run_simulation(
                    vaccination_rate=0.0,
                    strategy="none",
                    network_type=network_type,
                    seed=cv.BASE_SEED,
                    beta=0.20,
                )

                self.assertGreaterEqual(
                    peak,
                    1,
                )

                self.assertLessEqual(
                    peak,
                    cv.POPULATION,
                )

                self.assertGreaterEqual(
                    epidemic_size,
                    1,
                )

                self.assertLessEqual(
                    epidemic_size,
                    cv.POPULATION,
                )

                self.assertGreaterEqual(
                    time_to_peak,
                    0,
                )

                self.assertGreaterEqual(
                    duration,
                    0,
                )

                self.assertLessEqual(
                    duration,
                    cv.TIME_STEPS,
                )


if __name__ == "__main__":
    unittest.main()