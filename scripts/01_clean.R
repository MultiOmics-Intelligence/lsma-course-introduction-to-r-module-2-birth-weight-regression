# Task 1 · Set up and clean
# Lessons to revisit: Module 1, lessons 3 and 4; Module 2, lesson 6
#
# Run every script from the project folder (open the .Rproj file in RStudio first),
# so that "data/..." and "results/..." point to the right places.
# The later scripts start with source("scripts/01_clean.R"), so this script is
# the one place where the data are read and cleaned.

library(dplyr)

# TODO 1a: read data/birthwt.csv into an object called bw.
#          This is MASS::birthwt saved as a CSV file, with the raw codes (0 and 1).

# TODO 1b: inside mutate(), turn smoke, ht and low into labelled factors with
#          factor(..., levels = ..., labels = ...).
#          Make "no hypertension" the first level of ht, so it becomes the reference group.

# TODO 1c: check your work with nrow() and a table() of the new ht column.

# TODO 1d: save the counts of each ht group to results/ht_counts.csv
#          with two columns: ht, n  (one row per group, reference group first).
#          Hint: as.data.frame(table(ht = bw$ht), responseName = "n")
#          and write.csv(..., row.names = FALSE).
