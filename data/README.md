# Data

`boarding_school_1978.csv` holds the summary numbers of the 1978 influenza outbreak at an English
boarding school, which `calibrate.py` uses as a real outbreak to compare the model against.

Source: Anonymous (1978), "Influenza in a boarding school", *British Medical Journal* 1: 587.
Only these summary statistics are used. They are widely quoted for this outbreak, for example in
textbooks on mathematical epidemiology. "Confined to bed" is used as the measure of being infected,
so it understates the true number of infections.

All other results in the project are produced by simulation (`run_experiment.py`) and are saved in
`results/`, so there is no other input data.
