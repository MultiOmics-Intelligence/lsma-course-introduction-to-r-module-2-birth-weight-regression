# Task 3 · Compare      (lesson to revisit: Module 2, lesson 2)
# Task 4 · Low birth weight   (lesson to revisit: Module 2, lesson 3)

source("scripts/01_clean.R")

# ---- Task 3 ----
# TODO 3a: run Welch's t-test and the Wilcoxon test with the formula form, bwt ~ ht.
#          Read the "sample estimates" lines: which group is subtracted from which?
#          For the Wilcoxon test, conf.int = TRUE gives an estimate and an interval too.

# TODO 3b: save results/ht_tests.csv with one row per test and the columns
#          test, estimate, conf_low, conf_high, p_value
#          Use test = "welch_t" and test = "wilcoxon".
#          For welch_t, estimate is the difference in mean birth weight (g) between the groups.

# ---- Task 4 ----
# TODO 4a: make the two-by-two table of ht against low with table(),
#          then the row percentages with prop.table(..., margin = 1).

# TODO 4b: save results/ht_low_table.csv with one row per ht group and the columns
#          ht, normal, low, pct_low      (pct_low = percentage of that group with low birth weight)

# TODO 4c: run Fisher's exact test on the table.
#          Work out the expected count of every cell: row total x column total / grand total.
#          Save results/fisher_test.csv with the columns
#          p_value, expected_smallest     (the smallest expected count)
