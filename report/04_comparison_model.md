# Comparison Model

## Overview

An independent SIRV comparison model was developed to cross-check the behaviour of the main disease spread model. The purpose of this model was to investigate how different network structures and vaccination strategies affect the spread of an epidemic.

The main research question is:

**How does targeted vaccination of highly connected individuals compare with random vaccination across different network structures in reducing epidemic size and peak infection levels?**

The model represents each person as a node in a contact network and connections between people as edges. Individuals can be susceptible, infected, recovered or vaccinated.

## Experimental Setup

The comparison model used the following settings:

- Population size: 100
- Recovery probability: 0.10
- Vaccination proportion: 20%
- Maximum simulation time: 200 steps
- Number of repeated runs: 100 per condition
- Base random seed: 42

Three vaccination strategies were compared:

- No vaccination
- 20% random vaccination
- 20% targeted vaccination

Random vaccination selects individuals without considering their position in the network.

Targeted vaccination selects individuals with the highest number of connections first. This allows the experiment to test whether protecting highly connected people can reduce disease transmission more effectively.

## Network Structures

Three different network structures were used:

- Random network
- Small-world network
- Scale-free network

The networks were configured so that their average degree was close to four. This helped make the comparison fair because the networks had a similar overall level of connectivity.

A separate network property analysis was also completed across 100 generated networks of each type.

The random network had an average clustering coefficient of approximately 0.037 and an average maximum degree of 9.52.

The small-world network had an average degree of 4.0, a clustering coefficient of approximately 0.377 and an average maximum degree of 5.82.

The scale-free network had an average degree of approximately 3.92, a clustering coefficient of approximately 0.132 and an average maximum degree of 24.76.

These results show that although the networks had a similar average number of connections, their structures were very different. The scale-free network contained much more highly connected hub nodes, while the small-world network had much stronger local clustering.

## Beta Sensitivity Experiment

The transmission probability, beta, was varied to understand how changes in disease transmissibility affected the results.

The beta values tested were:

- 0.05
- 0.10
- 0.15
- 0.20
- 0.25
- 0.30

Each beta value was tested across:

- 3 network types
- 3 vaccination strategies
- 100 repeated runs

This produced:

**3 × 3 × 6 × 100 = 5,400 individual simulation runs.**

Each individual run was saved rather than only saving the average result. This allowed the analysis to calculate both mean results and variation between repeated simulations.

## Measurements

Four main measurements were recorded:

- Peak infections
- Epidemic size
- Time to peak
- Epidemic duration

Peak infections represents the highest number of people infected at the same time.

Epidemic size represents the total number of people infected during the outbreak.

Time to peak shows how long the outbreak takes to reach its highest infection level.

Epidemic duration shows how long the outbreak continues before no infected individuals remain.

## Overall Results

The results showed that vaccination reduced epidemic size and peak infections compared with no vaccination.

Across the full beta experiment, the average results were approximately:

| Strategy | Mean Epidemic Size | Mean Peak Infections |
|---|---:|---:|
| No Vaccination | 64.32 | 33.12 |
| 20% Random | 38.00 | 19.25 |
| 20% Targeted | 12.11 | 5.79 |

Targeted vaccination produced the lowest epidemic size and peak infection levels.

This supports the hypothesis that vaccinating highly connected individuals can reduce disease transmission more effectively than randomly vaccinating the same proportion of the population.

## Effect of Transmission Probability

Increasing beta generally increased epidemic size and peak infections.

For example, in the random network with no vaccination, the mean epidemic size increased from approximately 18.54 at beta 0.05 to approximately 87.04 at beta 0.30.

This pattern shows that a higher probability of transmission allows the infection to spread through a larger part of the network.

Both vaccination strategies reduced the impact of increasing beta, although targeted vaccination generally produced the strongest reduction.

## Effect of Network Structure

The effect of vaccination was different across the three network structures.

The strongest difference was observed in the scale-free network.

At beta 0.20:

- No vaccination produced a mean epidemic size of approximately 80.26.
- 20% random vaccination reduced the mean epidemic size to approximately 54.68.
- 20% targeted vaccination reduced the mean epidemic size to approximately 2.81.

This means targeted vaccination reduced the epidemic size by approximately 96.5% compared with no vaccination under this experimental condition.

The network property analysis helps explain this result. The scale-free network contained highly connected hub nodes, with an average maximum degree of approximately 24.76.

Targeted vaccination protects these hub nodes first. Removing highly connected individuals from the susceptible population can interrupt many possible transmission pathways at the same time.

## Random Network Results

Targeted vaccination was also more effective than random vaccination in the random network.

At beta 0.20:

- No vaccination produced a mean epidemic size of approximately 75.75.
- Random vaccination reduced it to approximately 57.40.
- Targeted vaccination reduced it further to approximately 24.53.

This shows that targeting more connected individuals can still provide an advantage even when the network does not contain extremely large hub nodes.

## Small-World Network Results

The small-world network had the highest clustering coefficient.

At beta 0.20:

- No vaccination produced a mean epidemic size of approximately 80.72.
- Random vaccination reduced it to approximately 27.40.
- Targeted vaccination reduced it to approximately 16.02.

The higher clustering in the small-world network means that individuals are more likely to belong to closely connected groups.

Infection can therefore spread strongly within local groups. Vaccination helps break some of these transmission pathways, with targeted vaccination again producing the stronger reduction.

## Variability Analysis

The beta sweep originally stored only one averaged result for each experimental condition.

This was improved so that all 100 individual simulations for every condition were saved.

The final beta sweep dataset therefore contains 5,400 individual simulation records.

This allowed standard deviation to be calculated for epidemic size and peak infections. Including variation is important because the disease model is stochastic and individual simulation runs can produce different results even when the same general experimental condition is used.

## Model Validation

The comparison model was tested using an automated validation suite.

Nine validation tests were created.

The tests checked that:

- beta equal to zero produces no secondary infections
- random vaccination selects the expected number of individuals
- targeted vaccination selects highly connected individuals
- patient zero is selected only from susceptible individuals
- vaccinated individuals remain protected
- susceptible, infected, recovered and vaccinated counts always equal the population size
- simulations are reproducible when the same random seed is used
- simulations stop when no infected individuals remain
- all three network types run successfully

All nine validation tests passed successfully.

These tests provide additional confidence that the model is behaving according to its intended rules.

## Limitations

There are several limitations in the comparison model.

The contact networks remain static during each simulation. In real life, people's contact patterns can change over time.

Vaccination is assumed to provide complete protection. Real vaccines may reduce the probability of infection rather than completely preventing it.

All individuals use the same transmission and recovery probabilities. Real populations contain differences in age, health, behaviour and susceptibility.

The model does not include an exposed or incubation state. Individuals therefore move directly from susceptible to infected.

Behavioural changes during an outbreak are also not included. For example, individuals do not reduce their number of contacts when infection levels increase.

The population size is limited to 100 individuals. This was suitable for repeated computational experiments but is much smaller than a real population.

Finally, the random, small-world and scale-free networks are simplified mathematical models and do not represent the exact contact structure of a real community.

## Conclusion

The comparison model supports the main hypothesis under the conditions tested in this project.

Vaccination reduced epidemic size and peak infection levels, while targeted vaccination generally performed better than random vaccination.

The largest benefit of targeted vaccination was observed in the scale-free network because this network contained highly connected hub nodes. Protecting these nodes removed many possible transmission pathways.

The results show that the effectiveness of vaccination depends not only on how many people are vaccinated, but also on their position within the contact network.

These findings apply to the assumptions and parameters used in this computational model and should not be interpreted as direct predictions of a real epidemic.