# Model and Methods

## Disease model

We model the spread of an infectious disease with a discrete-time SIR (Susceptible, Infected, Recovered) model that runs on a contact network. Each person is a node and each contact between two people is an edge. At every time step, each infected person infects each of their susceptible neighbours independently with probability beta, and then recovers with probability gamma. All updates in a step happen at the same time, so a person infected in one step can only start infecting others in the next step. A recovered person cannot be infected again. Every simulation starts with one randomly chosen unvaccinated person infected, and it ends when nobody is infected any more (or after 500 steps, which was never reached in our runs).

Vaccination is modelled in the simplest possible way: before the outbreak starts, a fixed fraction of the population (the vaccination budget, 10% in our experiments) is moved straight into the recovered state. These people are fully and immediately immune and can neither catch nor pass on the disease. This ignores partial protection and the time it takes to roll out a vaccine, which we discuss as a limitation in the conclusion.

## Contact networks

We compare three network types, each built with 300 people and an average of about six contacts per person so that the comparison is fair:

- **Random (Erdos-Renyi):** every pair of people is connected with the same small probability, so almost everyone has a similar number of contacts.
- **Small-world (Watts-Strogatz):** people sit on a ring and are connected to their nearest neighbours, which creates tight groups of friends, and 10% of the connections are rewired to random people, which creates a few shortcuts between groups.
- **Scale-free (Barabasi-Albert):** new people join and prefer to connect to people who already have many contacts, so a few "hubs" have very many contacts while most people have few.

## Vaccination strategies

With a budget of 10% of the population (30 people), we compare four strategies. **None** is the baseline with no vaccination. **Random** vaccinates 30 people chosen uniformly at random. **Degree** vaccinates the 30 people with the most contacts. **Betweenness** vaccinates the 30 people with the highest betweenness centrality, meaning the people who lie on the most shortest paths between other people and so act as bridges between groups. The targeted strategies are computed once on the network before the outbreak and do not change afterwards.

## Outcome measures

For each run we record the **final size** (the fraction of the population that was infected at some point; vaccinated people are not counted as infected), the **peak** number infected at the same time, the **time to peak** (in steps) and the **duration** of the outbreak.

## Experimental design

We run the model for every combination of the three networks, four strategies and seven values of beta (0.02, 0.04, 0.06, 0.08, 0.10, 0.15 and 0.20), with gamma fixed at 0.1. Each combination is repeated 30 times, giving 2,520 simulations. Because the model is random, repetition number k uses the same random seed for every strategy, so within a repetition all four strategies are tested on exactly the same network. We report means with 95% confidence intervals.

## Calibration against a real outbreak

To check that the model gives realistic numbers, we calibrated it against the 1978 influenza outbreak at an English boarding school (763 boys; 512 were confined to bed, a final size of 0.671; peak of about 298 in bed at once around day 6). A search over the average number of contacts, beta and gamma, on random and small-world networks, found the best fit at roughly 12 contacts per person, beta 0.18 and gamma 0.5, which reproduces the peak well (an average peak of about 299 people against 298 reported) and the timing roughly (day 8 against day 6), but it overshoots the final size badly (0.97 against 0.67). We calibrated using only the runs where the outbreak took off, because on a network an outbreak often dies out immediately, and averaging those runs in gave a misleadingly good fit. We discuss why the final size does not match in the limitations.

## Software

The model is written in Python using NetworkX for the networks, NumPy and pandas for the numbers, and Matplotlib for the figures. All code, results and the analysis notebook are in the project repository, and the README explains how to reproduce every result.
