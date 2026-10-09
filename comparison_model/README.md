# SIRV Comparison Model

This folder contains an independent implementation of the disease spread model used as a cross-check of the main project model.

The model investigates how vaccination strategy and network structure influence epidemic behaviour.

## Research Quesation

How does targeted vaccination of highly connected individuals compare with random vaccination across different network structures in reducing epidemic size and peak infection levels?

## Model

The comparison model uses a network-based SIRV model.

Each person is represented as a node in a contact network.

The possible states are:

- **S – Susceptible:** can become infected.
- **I – Infected:** can transmit the disease to susceptible neighbours.
- **R – Recovered:** no longer infectious.
- **V – Vaccinated:** protected from infection in the baseline model.

Disease transmission occurs only between connected nodes.

State changes are applied synchronously so that a person infected during the current time step does not immediately infect another person during that same step.

## Network Types

Three network structures are compared.

### Random Network

An Erdős–Rényi random network is used to represent contacts distributed approximately randomly across the population.

### Small-World Network

A Watts–Strogatz small-world network represents populations with strong local clustering and some longer-range connections.

### Scale-Free Network

A Barabási–Albert scale-free network contains a small number of highly connected hub nodes and many nodes with fewer connections.

## Vaccination Strategies

Three vaccination conditions are compared:

- No vaccination
- 20% random vaccination
- 20% targeted vaccination

Random vaccination selects individuals randomly.

Targeted vaccination selects individuals with the highest node degree, meaning people with the largest number of network connections are vaccinated first.

## Experimental Settings

The main comparison model uses:

- Population: 100
- Vaccination proportion: 20%
- Recovery probability: 0.10
- Maximum simulation length: 200 time steps
- Repeated simulations: 100 runs per condition
- Base random seed: 42

The beta sensitivity experiment tests six transmission probabilities:

- 0.05
- 0.10
- 0.15
- 0.20
- 0.25
- 0.30

The experiment compares:

- 3 network types
- 3 vaccination strategies
- 6 beta values
- 100 repeated simulations

This produces:

**3 × 3 × 6 × 100 = 5,400 individual simulation runs.**

## Measurements

The following epidemic measurements are recorded:

- Peak infections
- Epidemic size
- Time to peak
- Epidemic duration

Individual beta sweep runs are saved so that both averages and variability can be analysed.

## Network Property Comparison

The structural characteristics of the three network types are also compared.

The network analysis calculates:

- Average degree
- Clustering coefficient
- Maximum node degree

The three networks have similar average degree but different structures.

The small-world network has substantially higher clustering, while the scale-free network contains much larger hub nodes.

These differences help explain why vaccination strategies can perform differently across network structures.

## Validation

The comparison model includes automated validation tests.

The tests check that:

- beta = 0 produces no secondary infections
- random vaccination selects the expected number of people
- targeted vaccination selects highly connected nodes
- patient zero is selected from susceptible individuals
- vaccinated nodes remain protected
- S, I, R and V counts always equal the total population
- simulations are reproducible using the same random seed
- simulations stop when no infected individuals remain
- all three network types run successfully

The validation suite currently contains 9 tests.

## Installation

From the `comparison_model` directory, install the required packages:

```bash
py -m pip install -r requirements.txt