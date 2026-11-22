<a href="https://lsma.co.uk/courses"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/lsma-walk-courses.svg" alt="LSMA, London School of Multiomics and AI: learn by doing, on real data" width="100%"></a>

# Module 2 project: Risk factors for low birth weight

LSMA · Introduction to R · Module 2 project

<p>
<img src="https://img.shields.io/badge/LSMA-free%20course-D9481F?style=flat-square" alt="LSMA free course">
<img src="https://img.shields.io/badge/course-Introduction%20to%20R-0F1B33?style=flat-square" alt="Course">
<img src="https://img.shields.io/badge/language-R-276DC3?style=flat-square&logo=r&logoColor=white" alt="Language">
<img src="https://img.shields.io/badge/checks-automatic-2F7D5B?style=flat-square&logo=githubactions&logoColor=white" alt="Automatic checks">
</p>

## Research question

Is a history of hypertension in the mother (`ht`) associated with lower birth weight, and does the
association hold after adjusting for smoking and the mother's weight?

Hypertension is persistently high blood pressure. In `birthwt`, the column `ht` records whether the
mother had a history of it: 0 for no, 1 for yes. An association means that babies in one group tend
to differ from babies in the other; it does not by itself say why. Adjusting means comparing mothers
with and without hypertension who are alike in the other factors, here smoking and weight.

## What you will build

**In:** `data/birthwt.csv`, 189 births (the same data as `MASS::birthwt`; see `data/README.md`).

**Out:** numbered scripts in `scripts/`, the tables and figures they write in `results/`, and a short
Quarto report, `report.qmd`.

| Script | Task | Writes |
|---|---|---|
| `scripts/01_clean.R` | 1 | `results/ht_counts.csv` |
| `scripts/02_describe.R` | 2 | `results/bwt_by_ht.csv`, `results/bwt_by_ht.png` |
| `scripts/03_compare.R` | 3 and 4 | `results/ht_tests.csv`, `results/ht_low_table.csv`, `results/fisher_test.csv` |
| `scripts/04_models.R` | 5 | `results/adjusted_effects.csv`, `results/lwt_by_ht.csv`, `results/diagnostics.png` |
| `scripts/05_sample_size.R` | 6 | `results/sample_size.csv` |
| `report.qmd` | 6 | your report (render it to check it works) |

The TODO comments in each script give the exact file names and column names. The check reads those
files, so keep the names as they are.

## Before you start

1. Get your own copy of this repository. Use the GitHub Classroom invitation link in the project
   lesson on lsma.co.uk, or click **Use this template** on GitHub.
2. Clone your copy to your computer, then open the folder in RStudio as a Project
   (File > New Project > Existing Directory). This sets the working directory to the project folder,
   so `data/...` and `results/...` work in every script.
3. You need R with the packages dplyr and ggplot2, and Quarto for the report (it comes with
   recent versions of RStudio).
4. Work in `scripts/`, write every output to `results/`, and never edit `data/`.

At the end you should be able to delete everything in `results/`, run the scripts in order and get
the same files back.

## Tasks

Work through the tasks in order: clean data feed the descriptions, the descriptions tell you which
tests suit the data, and the tests and models feed the report. For every comparison, write down the
size of the difference, its 95% confidence interval and then the p-value. Keep a short notes file of
each decision and why you made it; it becomes the methods and limitations of your report.

### 1. Set up and clean

Turn `smoke`, `ht` and `low` into labelled factors. Make "no hypertension" the first level, so it
becomes the reference group. Check your work with `nrow()` and a `table()` of the new `ht` column.

Lesson to revisit: Module 1, lessons 3 and 4; Module 2, lesson 6.

**Checkpoint:** 189 births; 12 mothers with a history of hypertension.

### 2. Describe

Summarise birth weight by hypertension: n, mean, SD, median. Plot the two groups with every baby
shown as a point.

Lesson to revisit: Module 1, lesson 5; Module 2, lesson 1.

**Checkpoint:** babies of mothers with hypertension weigh about 2,537 g on average, against about
2,972 g; with only 12 in one group, the points matter more than the means.

### 3. Compare

Run Welch's t-test and the Wilcoxon test. Report the difference with its 95% confidence interval.

Lesson to revisit: Module 2, lesson 2.

**Checkpoint:** a difference of about 435 g, with a 95% interval from about −154 to 1,024 g and p of
about 0.13, so the data cannot rule out no difference. Explain why a group of 12 makes the interval
so wide.

### 4. Low birth weight

Make the two-by-two table of `ht` against `low`, with row percentages. Use Fisher's exact test, and
say why it suits these counts.

Lesson to revisit: Module 2, lesson 3.

**Checkpoint:** 7 of 12 babies (58%) of mothers with hypertension had low birth weight, against 52 of
177 (29%); Fisher's p is about 0.05.

### 5. Adjust

Fit `lm(bwt ~ ht + smoke + lwt)` and a logistic regression for `low` with the same factors. Report
each effect with its confidence interval, and check the diagnostic plots.

Lesson to revisit: Module 2, lessons 3 and 4.

**Checkpoint:** after adjustment, hypertension is linked to a drop of about 586 g (95% CI about 165
to 1,008 g; p ≈ 0.007), larger and clearer than in task 3. Mothers with hypertension were heavier on
average (about 158 against 128 lb), and heavier mothers tend to have heavier babies, so the
unadjusted comparison hid part of the effect.

### 6. Report

Write a short Quarto report with inline numbers: methods, results, one figure, limitations. State how
many babies per group a study would need to detect a 300 g difference with 80% power.

Lesson to revisit: Module 2, lessons 5 and 6.

**Checkpoint:** your limitations mention the small hypertension group, one centre in 1986, and that
this is an association, not proof of cause.

## Hand in

Commit and push `scripts/`, `results/` and `report.qmd`. The **Checks** tab (GitHub Actions) then
runs automatically. A green tick means every checkpoint passed. You can push as often as you like.

You can run the same check on your own computer first: `python tests/check_results.py`.

## If a check fails

Open the **Actions** tab, click the latest run and read the log. Each line names a task and says
what to look at, for example:

```
FAIL  Task 3 · Compare: the 95% confidence interval of the Welch test does not match the checkpoint
```

Fix that task, rerun your scripts, commit the new results and push again.

## Getting help

- The project lesson on lsma.co.uk, and the lessons named under each task.
- Helix, the course tutor.
- Email info@lsma.co.uk.

Never post personal data in a public place, including issues and discussions on GitHub.

**Follow LSMA**

<p>
  <a href="https://lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-website.svg" alt="LSMA: lsma.co.uk" height="54"></a>
  <a href="https://www.linkedin.com/showcase/113252126/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-linkedin.svg" alt="LSMA on LinkedIn" height="54"></a>
  <a href="https://www.instagram.com/lsma.uk/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-instagram.svg" alt="LSMA on Instagram: @lsma.uk" height="54"></a>
  <a href="mailto:info@lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-email.svg" alt="Email: info@lsma.co.uk" height="54"></a>
</p>

Good luck, and enjoy the project.

**Dr. Anas Alzaeem**<br>
Academic Director, LSMA

[![Dr. Anas Alzaeem, Academic Director, LSMA](https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/signature/LSMA_Banner_Anas_Alzaeem.png)](https://lsma.co.uk)

© 2026 MultiOmics Intelligence Ltd. LSMA is the education arm of MultiOmics Intelligence. Code licensed under MIT.
