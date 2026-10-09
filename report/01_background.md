# Background

## Disease Spread as a Computational Model

Disease transmission can be studied using computational models that represent how an infection moves through a population over time. These models make it possible to investigate how different assumptions, contact patterns and intervention strategies affect the size and behaviour of an outbreak.

This project focuses on disease spread through a contact network. Instead of assuming that every person can interact equally with every other person, individuals are represented as nodes and their possible contacts are represented as edges. This makes it possible to examine how the structure of a population can influence disease transmission.

The main research question for this project is:

**How does targeted vaccination of highly connected individuals compare with random vaccination across different network structures in reducing epidemic size and peak infection levels?**

The project therefore combines an epidemic model with several network structures and vaccination strategies.

## SIRV Model

The model used in this project is based on the traditional SIR model, with an additional vaccinated state.

Each individual can be in one of four states:

- **Susceptible (S):** the individual is not infected but can become infected through contact with an infected neighbour.
- **Infected (I):** the individual currently has the infection and can transmit it to susceptible neighbours.
- **Recovered (R):** the individual has recovered and is no longer infectious.
- **Vaccinated (V):** the individual is protected from infection under the assumptions of the baseline model.

At the beginning of a simulation, most individuals are susceptible. Vaccination is applied before the outbreak according to the selected vaccination strategy, and one susceptible individual is then selected as the initial infected person.

During each simulation step, infected individuals can transmit the infection to susceptible neighbours. Infected individuals can also recover. State changes are handled synchronously so that an individual who becomes infected during one time step does not immediately infect another individual during that same step.

## Transmission Probability

The transmission probability is represented by **beta (β)**.

Beta controls the probability that an infected individual transmits the disease to a susceptible neighbour during a contact in one simulation time step.

A lower beta value makes transmission less likely, while a higher beta value makes transmission more likely. The comparison model tests several beta values so that the effect of changing disease transmissibility can be examined.

The beta values used in the sensitivity experiment are:

- 0.05
- 0.10
- 0.15
- 0.20
- 0.25
- 0.30

These values are modelling parameters used to compare simulation behaviour rather than estimates intended to predict a specific real-world disease.

## Recovery Probability

The recovery probability is represented by **gamma (γ)**.

Gamma controls the probability that an infected individual recovers during a simulation time step.

In the comparison model, the recovery probability is set to 0.10. Once an individual moves into the recovered state, they remain recovered for the rest of the simulation.

Together, beta and gamma influence how quickly an outbreak grows, how large the epidemic becomes and how long the outbreak continues.

## Why Use a Network Model?

A network model is useful because real populations do not normally behave as completely mixed groups. People usually interact with a limited number of contacts, and some individuals may have many more connections than others.

In the model:

- nodes represent individuals
- edges represent possible disease-transmission contacts
- infection can only pass between connected nodes

This allows the project to study how differences in contact structure affect epidemic behaviour.

Network structure is particularly important for the vaccination question because highly connected individuals may contribute to a large number of possible transmission pathways. Vaccinating these individuals may therefore reduce transmission more effectively than vaccinating the same number of randomly selected individuals.

## Random Network

The random network is generated using an Erdős-Rényi model.

Connections are distributed approximately randomly between individuals. This provides a useful baseline network where contacts are not deliberately clustered around particular nodes.

The random network has relatively low clustering and does not normally contain extremely large hub nodes.

## Small-World Network

The small-world network is generated using a Watts-Strogatz model.

Small-world networks combine strong local clustering with some longer-range connections. This represents situations where individuals have groups of closely connected contacts while still maintaining some connections outside those groups.

The network property analysis showed that the small-world networks used in this project had substantially higher clustering than the random and scale-free networks.

This clustering can influence the way an outbreak spreads because infection may circulate strongly within locally connected groups before reaching other parts of the network.

## Scale-Free Network

The scale-free network is generated using a Barabási-Albert model.

A major feature of this structure is the presence of highly connected hub nodes. Most individuals have relatively few connections, while a small number of individuals have many connections.

The network property comparison showed that the scale-free networks had a similar overall average degree to the other networks but a much larger maximum node degree.

This is particularly relevant to targeted vaccination. Vaccinating a highly connected hub can remove many potential transmission pathways at once, which may explain why targeted vaccination performs strongly in scale-free networks.

## Relationship to the Research Question

The three network types allow the same vaccination strategies to be tested under different contact structures.

The project compares:

- no vaccination
- 20% random vaccination
- 20% targeted vaccination

The main outcomes measured are:

- epidemic size
- peak infections
- time to peak
- epidemic duration

By keeping the overall network connectivity reasonably similar while changing structural properties such as clustering and the presence of hubs, the experiments can investigate whether the effectiveness of vaccination depends on the way contacts are organised.

The purpose of the model is not to predict a real epidemic. Instead, it provides a controlled computational environment for examining how network structure and vaccination strategy interact.