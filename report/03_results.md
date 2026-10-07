# Results

All results below come from the sweep described in the Model and Methods section: 300 people, about six contacts each, gamma = 0.1, 10% of people vaccinated, and 30 repetitions for every combination of network, strategy and beta. Values are means over the 30 repetitions, and the "+/-" values are 95% confidence intervals. The full analysis, including every table, is in `analysis.ipynb`.

## Which strategy works best depends on the network

Table 1 shows the mean final size, the fraction of the population that was infected, at beta = 0.10.

| Network | None | Random | Degree | Betweenness |
|---|---|---|---|---|
| Random | 0.83 +/- 0.12 | 0.67 +/- 0.12 | 0.66 +/- 0.11 | 0.77 +/- 0.05 |
| Small-world | 0.84 +/- 0.12 | 0.59 +/- 0.14 | 0.58 +/- 0.11 | 0.44 +/- 0.12 |
| Scale-free | 0.84 +/- 0.10 | 0.68 +/- 0.11 | 0.22 +/- 0.09 | 0.25 +/- 0.09 |

*Table 1: mean final size at beta = 0.10 (see `results/analysis_final_size_by_strategy.png`).*

The scale-free network shows by far the largest effect. Vaccinating the 10% best-connected people (by degree) reduces the final size from 0.84 to 0.22, a 74% reduction, while vaccinating 10% at random only reduces it by 19%. Betweenness gives almost the same result (0.25), because in a scale-free network the hubs are also the people with the highest betweenness. Both targeted strategies are clearly better than random vaccination, as their confidence intervals do not overlap with it. Targeted vaccination also lowers the peak number infected at the same time from about 128 people (out of 300) with no vaccination to about 16 to 20, and it delays the peak from about step 16 to step 25.

On the small-world network, all three vaccination strategies help, and betweenness is the best (0.44, a 48% reduction), followed by degree (0.58) and random (0.59). This is consistent with the idea that on a clustered network the people who bridge groups matter most, because they carry the disease between otherwise separate clusters. However, the confidence intervals of betweenness and random vaccination overlap somewhat (0.44 +/- 0.12 against 0.59 +/- 0.14), so with 30 repetitions this difference is suggestive rather than conclusive.

On the random network there is little to gain from targeting. Degree vaccination (0.66) is no better than random vaccination (0.67), and betweenness (0.77) is actually the weakest of the three. This is what we expect: in a random network almost everyone has a similar number of contacts, so no person is structurally special and choosing by degree or betweenness is not better than a random choice.

## Effect of the transmission probability

Figure 2 (`results/analysis_final_size_vs_beta.png`) shows how the final size changes with beta. Without vaccination, the epidemic takes off from about beta = 0.04 on the random and scale-free networks and from about 0.08 on the small-world network, where the clustering of contacts slows the spread between groups. On the scale-free network, targeted vaccination keeps the final size low over the whole range: at beta = 0.20 it is still about 0.54 to 0.56, against 0.92 with no vaccination and 0.82 with random vaccination. For stronger transmission the benefit of every strategy shrinks. On the random network at beta = 0.20 all strategies end between 0.76 and 0.87, and random vaccination (0.76) is the best of them, while on the small-world network betweenness remains the best (0.80 against 0.97 with no vaccination).

## Outbreaks that die out

On a network, an outbreak sometimes dies out almost immediately because the first infected person recovers before passing on the disease. We counted a run as a major outbreak if more than 10% of the population was infected. At beta = 0.10 without vaccination, about 87% to 90% of runs became major outbreaks on every network. On the scale-free network targeted vaccination reduces this share to about 43% to 50%, and the outbreaks that do happen are also about half the size (about 0.49 against 0.93). On the random network the share of major outbreaks barely changes (0.80 to 0.97), so the benefit there comes only from smaller outbreaks. This is the reason for the large confidence intervals in Table 1: the final size of a single run is either close to zero or large, so the means hide a lot of variation, and differences below about 0.1 should not be over-interpreted.

## Calibration

The calibration against the 1978 boarding-school outbreak found that the model can reproduce the size of the peak (an average of about 299 people infected at once, against 298 reported) and roughly its timing (day 8 against day 6), but not the final size (0.97 against the reported 0.67). In our model, once an outbreak takes off on a network with this many contacts per person, it reaches almost everyone, whereas in the real outbreak a third of the boys were never ill. We return to this in the limitations.
