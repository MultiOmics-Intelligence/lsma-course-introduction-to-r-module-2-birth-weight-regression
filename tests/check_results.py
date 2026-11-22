"""Checks for the Module 2 project: risk factors for low birth weight.

Run from the repository folder:  python tests/check_results.py
Python 3 standard library only. It reads the files you commit in scripts/,
results/ and report.qmd; it does not run R.
"""

import csv
import hashlib
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Fingerprints of the untouched starter files, so the check can tell
# whether you have started work on each one.
STARTER = {
    "scripts/01_clean.R": "dff328c88cc937fbde63911f5fb095fa2ea963dbd086365c3f727ba871ab126c",
    "scripts/02_describe.R": "1d7ceb839d86791387e2928d3a292c1713125488a5b002da641af2a76858dc3f",
    "scripts/03_compare.R": "71f2f3f40edc5136080d2b3dfb9e689e16f7fdc0e3e60f7a4fbbf65c714daa93",
    "scripts/04_models.R": "33768f8e88f285fa7a9bd11a841d377053802111418382eeefaeba1911a7325d",
    "scripts/05_sample_size.R": "43faaf99ffa5a5c92e31e3772842fb3790f8e8849977a4b9085be6e2fabefaea",
    "report.qmd": "f16cfeeb3fc60fdc084bb2106c36a17405a99d3464fee09bf562ef724af702fa",
}


class Fail(Exception):
    pass


def fingerprint(path):
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n")).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def need_edited(rel):
    path = ROOT / rel
    if not path.is_file():
        raise Fail(f"{rel} is missing; keep the file and write your code in it")
    if fingerprint(path) == STARTER.get(rel):
        raise Fail(f"{rel} is still the untouched starter; write your code under the TODO comments")


def read_csv(rel, min_rows=1):
    path = ROOT / rel
    if not path.is_file():
        raise Fail(f"{rel} not found; run your script and commit the file it writes")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise Fail(f"{rel} is empty")
        rows = []
        for raw in reader:
            row = {}
            for key, value in raw.items():
                if key is None or key.strip() == "":
                    continue  # row names written by write.csv()
                row[key.strip().lower()] = (value or "").strip()
            rows.append(row)
    if len(rows) < min_rows:
        raise Fail(f"{rel} has {len(rows)} rows; expected at least {min_rows}")
    return rows


def need_columns(rows, rel, cols):
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        raise Fail(f"{rel} needs the column(s) {', '.join(missing)}; found {', '.join(rows[0])}")


def num(row, col, rel):
    value = row.get(col, "")
    try:
        return float(value)
    except ValueError:
        raise Fail(f"{rel}: column {col} should hold a number, found '{value}'")


def near(value, target, tol):
    return abs(value - target) <= tol


def png_size(rel):
    path = ROOT / rel
    if not path.is_file():
        raise Fail(f"{rel} not found; save the figure with ggsave() or png() and commit it")
    data = path.read_bytes()[:32]
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise Fail(f"{rel} is not a PNG file")
    return struct.unpack(">II", data[16:24])


def is_reference(label):
    return re.search(r"\bno\b|\bnon|without|absent|^0$", label.lower()) is not None


# ---------------------------------------------------------------- tasks

def task1():
    need_edited("scripts/01_clean.R")
    rel = "results/ht_counts.csv"
    rows = read_csv(rel, 1)
    need_columns(rows, rel, ["ht", "n"])
    if len(rows) != 2:
        raise Fail(f"expected 2 rows in {rel} (one per hypertension group), found {len(rows)}")
    ns = [num(r, "n", rel) for r in rows]
    if sum(ns) != 189:
        raise Fail(f"the groups in {rel} add up to {sum(ns):g} births; the checkpoint says 189")
    if sorted(ns) != [12, 177]:
        raise Fail(f"the group sizes in {rel} do not match the checkpoint; check how ht was coded")
    if ns[0] != 177 or not is_reference(rows[0]["ht"]):
        raise Fail("the first level of ht should be the mothers with no hypertension, so it becomes the reference group")


def task2():
    need_edited("scripts/02_describe.R")
    rel = "results/bwt_by_ht.csv"
    rows = read_csv(rel, 2)
    need_columns(rows, rel, ["ht", "n", "mean", "sd", "median"])
    if len(rows) != 2:
        raise Fail(f"expected 2 rows in {rel}, found {len(rows)}")
    by_n = {num(r, "n", rel): r for r in rows}
    if set(by_n) != {12, 177}:
        raise Fail(f"the n column in {rel} should give the size of each hypertension group")
    expected = {177: (2972.2, 709.4, 2977), 12: (2536.8, 917.4, 2495)}
    for n, (mean, sd, median) in expected.items():
        r = by_n[n]
        if not near(num(r, "mean", rel), mean, 1.0):
            raise Fail(f"the mean birth weight for the group of {n:g} does not match the checkpoint; group by ht, not smoke")
        if not near(num(r, "sd", rel), sd, 1.0):
            raise Fail(f"the SD for the group of {n:g} looks wrong; use sd() on bwt within each group")
        if not near(num(r, "median", rel), median, 1.0):
            raise Fail(f"the median for the group of {n:g} looks wrong; use median() on bwt within each group")
    width, height = png_size("results/bwt_by_ht.png")
    if width < 300 or height < 300:
        raise Fail("results/bwt_by_ht.png is very small; save it with ggsave() at a readable size")


def task3():
    need_edited("scripts/03_compare.R")
    rel = "results/ht_tests.csv"
    rows = read_csv(rel, 2)
    need_columns(rows, rel, ["test", "estimate", "conf_low", "conf_high", "p_value"])
    tests = {r["test"].lower(): r for r in rows}
    welch = next((r for k, r in tests.items() if "welch" in k), None)
    wilcox = next((r for k, r in tests.items() if "wilcox" in k), None)
    if welch is None or wilcox is None:
        raise Fail(f"{rel} needs one row with test = welch_t and one with test = wilcoxon")
    est = num(welch, "estimate", rel)
    low, high = num(welch, "conf_low", rel), num(welch, "conf_high", rel)
    if est < 0:  # hypertension minus no hypertension is also a fair way to report it
        est, low, high = -est, -high, -low
    if not near(est, 435.4, 2.0):
        raise Fail("the Welch difference in mean birth weight does not match the checkpoint; estimate should be the difference between the two group means in grams")
    if not (near(low, -153.7, 3.0) and near(high, 1024.5, 3.0)):
        raise Fail("the 95% confidence interval of the Welch test does not match the checkpoint; take it from t.test()$conf.int")
    if not near(num(welch, "p_value", rel), 0.133, 0.005):
        raise Fail("the Welch p-value does not match the checkpoint; use Welch's test (the t.test() default), not var.equal = TRUE")
    if not near(num(wilcox, "p_value", rel), 0.118, 0.01):
        raise Fail("the Wilcoxon p-value looks wrong; use wilcox.test(bwt ~ ht, data = bw)")


def task4():
    need_edited("scripts/03_compare.R")
    rel = "results/ht_low_table.csv"
    rows = read_csv(rel, 2)
    need_columns(rows, rel, ["ht", "normal", "low", "pct_low"])
    if len(rows) != 2:
        raise Fail(f"expected 2 rows in {rel} (one per hypertension group), found {len(rows)}")
    by_total = {num(r, "normal", rel) + num(r, "low", rel): r for r in rows}
    if set(by_total) != {12, 177}:
        raise Fail(f"the rows of {rel} should be the hypertension groups and the columns the low birth weight groups")
    for total, low, pct in ((12, 7, 58.3), (177, 52, 29.4)):
        r = by_total[total]
        if num(r, "low", rel) != low:
            raise Fail(f"the count of low birth weight babies in the group of {total} does not match the checkpoint")
        p = num(r, "pct_low", rel)
        if p <= 1:
            p *= 100
        if not near(p, pct, 0.2):
            raise Fail("pct_low should be the percentage within each hypertension group (prop.table(..., margin = 1))")
    rel = "results/fisher_test.csv"
    rows = read_csv(rel, 1)
    need_columns(rows, rel, ["p_value", "expected_smallest"])
    if not near(num(rows[0], "p_value", rel), 0.0516, 0.002):
        raise Fail("the Fisher p-value does not match the checkpoint; run fisher.test() on the two-by-two table")
    if not near(num(rows[0], "expected_smallest", rel), 3.75, 0.02):
        raise Fail("expected_smallest looks wrong; use row total x column total / grand total for each cell and keep the smallest")


def find_term(rows, model, pattern):
    for r in rows:
        if r["model"].lower() == model and re.search(pattern, r["term"].lower()):
            return r
    raise Fail(f"results/adjusted_effects.csv has no {model} row for the term matching '{pattern}'")


def task5():
    need_edited("scripts/04_models.R")
    rel = "results/adjusted_effects.csv"
    rows = read_csv(rel, 6)
    need_columns(rows, rel, ["model", "term", "estimate", "conf_low", "conf_high", "p_value"])
    models = {r["model"].lower() for r in rows}
    if not {"linear", "logistic"} <= models:
        raise Fail(f"{rel} needs rows with model = linear and model = logistic")
    ht = find_term(rows, "linear", r"^ht|hyper")
    est = num(ht, "estimate", rel)
    if near(est, 586.4, 3.0):
        raise Fail("the linear hypertension effect has the wrong sign; is no hypertension the reference level?")
    if not near(est, -586.4, 3.0):
        raise Fail("the adjusted hypertension effect in the linear model does not match the checkpoint; fit lm(bwt ~ ht + smoke + lwt)")
    if not (near(num(ht, "conf_low", rel), -1007.9, 3.0) and near(num(ht, "conf_high", rel), -164.9, 3.0)):
        raise Fail("the 95% interval for the linear hypertension effect does not match the checkpoint; use confint()")
    if not near(num(ht, "p_value", rel), 0.0067, 0.001):
        raise Fail("the p-value for the linear hypertension effect does not match the checkpoint")
    if not near(num(find_term(rows, "linear", r"smok"), "estimate", rel), -265.1, 3.0):
        raise Fail("the smoking effect in the linear model looks wrong; check how smoke was coded")
    if not near(num(find_term(rows, "linear", r"^lwt$"), "estimate", rel), 5.35, 0.05):
        raise Fail("the lwt effect in the linear model looks wrong")
    ht = find_term(rows, "logistic", r"^ht|hyper")
    odds = num(ht, "estimate", rel)
    if near(odds, 1.822, 0.02):
        raise Fail("the logistic estimates look like log-odds; turn them into odds ratios with exp()")
    if not near(odds, 6.18, 0.06):
        raise Fail("the hypertension odds ratio does not match a glm(low ~ ht + smoke + lwt, family = binomial)")
    low, high = num(ht, "conf_low", rel), num(ht, "conf_high", rel)
    if not (low < odds < high and near(low, 1.68, 0.2) and near(high, 26.2, 3.0)):
        raise Fail("the interval for the hypertension odds ratio looks wrong; use exp() of confint()")
    rel = "results/lwt_by_ht.csv"
    rows = read_csv(rel, 2)
    need_columns(rows, rel, ["ht", "mean_lwt"])
    means = sorted(num(r, "mean_lwt", rel) for r in rows)
    if len(means) != 2 or not (near(means[0], 127.9, 0.2) and near(means[1], 157.5, 0.2)):
        raise Fail(f"the mean mother's weight per hypertension group in {rel} does not match the checkpoint")
    png_size("results/diagnostics.png")


def task6():
    need_edited("scripts/05_sample_size.R")
    rel = "results/sample_size.csv"
    rows = read_csv(rel, 1)
    need_columns(rows, rel, ["delta", "sd", "power", "n_per_group"])
    if not near(num(rows[0], "sd", rel), 729.2, 1.0):
        raise Fail("use the SD of birth weight from your own data, sd(bw$bwt)")
    if not near(num(rows[0], "n_per_group", rel), 94, 1.0):
        raise Fail("n_per_group does not match power.t.test(delta = 300, sd = ..., power = 0.8)")
    need_edited("report.qmd")
    text = (ROOT / "report.qmd").read_text(encoding="utf-8", errors="replace")
    if "TODO" in text:
        raise Fail("report.qmd still has TODO lines; replace each one with your own text")
    if not re.search(r"`r\s", text):
        raise Fail("report.qmd should take its numbers from the analysis with inline code, `r ...`")
    match = re.search(r"^#+\s*Limitations?\b(.*?)(?=^#+\s|\Z)", text, re.S | re.M | re.I)
    if not match or len(match.group(1).split()) < 20:
        raise Fail("report.qmd needs a Limitations section of a few sentences")
    lim = match.group(1).lower()
    missing = []
    if not re.search(r"\b12\b|twelve|small", lim):
        missing.append("the size of the hypertension group")
    if not ("1986" in lim and re.search(r"(one|single|1)\s+(us\s+)?(medical\s+)?(centre|center|hospital|site|clinic)", lim)):
        missing.append("where and when the data were collected")
    if not re.search(r"caus", lim):
        missing.append("what the design can and cannot show")
    if missing:
        raise Fail("your limitations do not yet mention " + "; ".join(missing))


TASKS = [
    ("Task 1 · Set up and clean", task1),
    ("Task 2 · Describe", task2),
    ("Task 3 · Compare", task3),
    ("Task 4 · Low birth weight", task4),
    ("Task 5 · Adjust", task5),
    ("Task 6 · Report", task6),
]


def main():
    failed = 0
    for name, func in TASKS:
        try:
            func()
            print(f"PASS  {name}")
        except Fail as err:
            failed += 1
            print(f"FAIL  {name}: {err}")
    print()
    if failed:
        print(f"{failed} of {len(TASKS)} checks failed. Read the message, fix that task, then push again.")
        sys.exit(1)
    print("All checks passed. Well done.")


if __name__ == "__main__":
    main()
