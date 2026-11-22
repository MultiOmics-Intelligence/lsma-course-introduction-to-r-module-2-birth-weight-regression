# Task 5 · Adjust
# Lessons to revisit: Module 2, lessons 3 and 4

source("scripts/01_clean.R")

# TODO 5a: fit the linear model lm(bwt ~ ht + smoke + lwt, data = bw)
#          and the logistic model glm(low ~ ht + smoke + lwt, data = bw, family = binomial).

# TODO 5b: save results/adjusted_effects.csv with one row per model term and the columns
#          model, term, estimate, conf_low, conf_high, p_value
#          model is "linear" or "logistic"; term is the coefficient name R gives (for example "lwt").
#          Linear model: estimates and intervals in grams (coef() and confint()).
#          Logistic model: odds ratios, so exp() of the coefficients and of the confint() limits.

# TODO 5c: summarise the mother's weight (lwt) by hypertension group and save
#          results/lwt_by_ht.csv with the columns ht, mean_lwt

# TODO 5d: draw the four diagnostic plots of the linear model with plot()
#          and save them as results/diagnostics.png
#          Hint: png("results/diagnostics.png", width = 2000, height = 2000, res = 300);
#                par(mfrow = c(2, 2)); plot(...); dev.off()
