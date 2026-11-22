# Data

## birthwt.csv

189 births at Baystate Medical Center, Springfield, Massachusetts, USA, in 1986. This is the
`birthwt` dataset from the R package MASS, saved as a CSV file with no changes: the same rows,
the same columns and the raw numeric codes (0 and 1). You can load the identical data in R with
`MASS::birthwt`.

| Column | Meaning |
|---|---|
| low | birth weight under 2,500 g: 1 = yes, 0 = no |
| age | mother's age in years |
| lwt | mother's weight at her last menstrual period, in pounds |
| race | mother's recorded race: 1 = white, 2 = black, 3 = other |
| smoke | smoking during pregnancy: 1 = yes, 0 = no |
| ptl | number of previous premature labours |
| ht | history of hypertension: 1 = yes, 0 = no |
| ui | presence of uterine irritability: 1 = yes, 0 = no |
| ftv | number of physician visits in the first trimester |
| bwt | birth weight in grams |

**Source.** Hosmer, D. W. and Lemeshow, S. (1989) *Applied Logistic Regression*. New York: Wiley.
Distributed in the MASS package (Venables, W. N. and Ripley, B. D. (2002) *Modern Applied
Statistics with S*, 4th edition, Springer), version 7.3-65.

**Licence.** MASS is distributed under the GNU General Public Licence (GPL-2 or GPL-3).
`birthwt` is a public teaching dataset with no names or identifiers. It is not synthetic: it is a
published dataset used for teaching. The MIT licence of this repository covers the code, not this
data file.
