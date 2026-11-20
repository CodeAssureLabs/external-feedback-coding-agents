#!/usr/bin/env python3
"""Recompute the tables and tests of "Fixed or Deleted? External Feedback Lets Cheaper AI Coding Agents Repair Rule Violations" from data/runs.csv.

Standard library only:  python3 analyze.py  > results.md

Conventions (as in the paper):
- repair rate = share of runs with outcome "repaired"; defect-gone rate = "repaired" or "removed feature".
- The pull request (PR) is the unit of inference. Paired comparisons average the runs of each PR, then use an exact
  two-sided sign-flip permutation test over PRs (primary) and a paired bootstrap interval. The run-level McNemar
  test (runs matched by PR and repetition) is reported as secondary.
- Bootstraps: 10,000 resamples of PRs, seed 20261112, values sorted first, so a configuration has the same interval
  in every table.
- Cost per change = mean over runs of the total cost (agent, plus the checker in CA workflows).
"""
import collections, csv, math, os, random, statistics as st

ITERS, SEED = 10000, 20261112
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = list(csv.DictReader(open(os.path.join(HERE, "data", "runs.csv"))))
for r in RUNS:
    r["repetition"] = int(r["repetition"]); r["sessions"] = int(r["sessions"]); r["agent_steps"] = int(r["agent_steps"])
    r["cost"] = float(r["cost_usd"])


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def boot(vals):
    rng = random.Random(SEED); vals = sorted(vals); m = sum(vals) / len(vals); bs = []
    for _ in range(ITERS):
        s = [vals[rng.randrange(len(vals))] for _ in vals]; bs.append(sum(s) / len(s))
    bs.sort(); return m, bs[int(0.025 * ITERS)], bs[int(0.975 * ITERS) - 1]


def mcnemar(b, c):
    n = b + c
    if n == 0: return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


def perm(diffs):
    xs = [round(d * 15) for d in diffs if abs(d) > 1e-12]   # per-PR mean differences are multiples of 1/15
    if not xs: return 1.0
    dist = {0: 1}
    for x in xs:
        nd = collections.Counter()
        for s_, c in dist.items(): nd[s_ + x] += c; nd[s_ - x] += c
        dist = nd
    obs = abs(sum(xs)); return sum(c for s_, c in dist.items() if abs(s_) >= obs) / 2 ** len(xs)


def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n; pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe)


fixed = lambda r: r["outcome"] == "repaired"
gone = lambda r: r["outcome"] in ("repaired", "removed feature")
pct = lambda t: f"{100 * t[0]:.0f}% [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"
usd = lambda t: f"${t[0]:.2f} [{t[1]:.2f}, {t[2]:.2f}]"
pv = lambda p: "< 0.001" if p < 0.001 else f"{p:.2g}" if p < 0.995 else "1.0"


def runs(study, model, workflow, clean=False):
    return [r for r in RUNS if r["study"] == study and r["model"] == model and r["workflow"] == workflow and (r["defect_type"] == "clean") == clean]


def per_pr(rs, f):
    d = collections.defaultdict(list)
    for r in rs: d[r["pr"]].append(float(f(r)))
    return {k: st.mean(v) for k, v in d.items()}


def paired(ra, rb, f):
    A = {(r["pr"], r["repetition"]): f(r) for r in ra}; B = {(r["pr"], r["repetition"]): f(r) for r in rb}
    keys = sorted(set(A) & set(B)); x = sum(A[k] and not B[k] for k in keys); y = sum(B[k] and not A[k] for k in keys)
    d = collections.defaultdict(list)
    for k in keys: d[k[0]].append(float(A[k]) - float(B[k]))
    dm = [st.mean(v) for v in d.values()]
    return dict(a_only=x, b_only=y, mcnemar=mcnemar(x, y), perm=perm(dm), diff=boot(dm), prs=len(dm))


MODELS = ["Haiku 4.5", "Sonnet 5.5", "Fable 5.1"]
out = ["# Recomputed results\n"]


def config_row(name, rs, extra=()):
    k = sum(map(fixed, rs)); g = sum(map(gone, rs)); n = len(rs)
    rem = sum(r["outcome"] == "removed feature" for r in rs)
    cells = [name, f"{k}/{n} = {pct(wilson(k, n))}", pct(boot(list(per_pr(rs, fixed).values())))[4:].strip() if False else
             "[{1:.0f}, {2:.0f}]".format(*[100 * v for v in boot(list(per_pr(rs, fixed).values()))]),
             f"{g}/{n} = {pct(wilson(g, n))}", str(rem), *extra, usd(boot(list(per_pr(rs, lambda r: r["cost"]).values())))]
    return "| " + " | ".join(cells) + " |"


# Table 2
out += ["## Table 2. Alone and CA, defective PRs\n", "| configuration | repair rate (Wilson) | cluster bootstrap | defect-gone rate (Wilson) | removed | cost per change |", "|---|---|---|---|---|---|"]
for m in MODELS:
    for wf in ("alone", "CA"): out.append(config_row(f"{m} {'+ CA' if wf == 'CA' else 'alone'}", runs("main", m, wf)))

# Table 3
out += ["\n## Table 3. Paired comparisons\n", "| A vs B | repair rate: mean difference [95%] | A only / B only | PR-level p | McNemar p | defect gone: A only / B only | PR-level p | McNemar p |", "|---|---|---|---|---|---|---|---|"]
for (ma, wa), (mb, wb) in [(("Haiku 4.5", "CA"), ("Haiku 4.5", "alone")), (("Sonnet 5.5", "CA"), ("Sonnet 5.5", "alone")), (("Fable 5.1", "CA"), ("Fable 5.1", "alone")),
                           (("Sonnet 5.5", "CA"), ("Fable 5.1", "alone")), (("Haiku 4.5", "CA"), ("Fable 5.1", "alone"))]:
    a, b = runs("main", ma, wa), runs("main", mb, wb); P = paired(a, b, fixed); G = paired(a, b, gone)
    out.append(f"| {ma} {wa} vs {mb} {wb} | {100 * P['diff'][0]:+.0f} pts [{100 * P['diff'][1]:.0f}, {100 * P['diff'][2]:.0f}] | {P['a_only']} / {P['b_only']} | {pv(P['perm'])} | {pv(P['mcnemar'])} | {G['a_only']} / {G['b_only']} | {pv(G['perm'])} | {pv(G['mcnemar'])} |")

# Table 4
TYPES = ["code-visible", "convention", "architecture rule", "multiple"]
out += ["\n## Table 4. Runs repaired, by defect type\n", "| configuration | " + " | ".join(TYPES) + " |", "|---|---|---|---|---|"]
for wf in ("alone", "CA"):
    for m in MODELS:
        rs = runs("main", m, wf)
        out.append(f"| {m} {wf} | " + " | ".join(f"{sum(map(fixed, [r for r in rs if r['defect_type'] == t]))}/{sum(r['defect_type'] == t for r in rs)}" for t in TYPES) + " |")

# Table 5
out += ["\n## Table 6. Clean PRs\n", "| configuration | left alone (incl. test-only) | code edit | removed | mean lines changed | mean cost |", "|---|---|---|---|---|---|"]
for wf in ("alone", "CA"):
    for m in MODELS:
        rs = runs("main", m, wf, clean=True); c = collections.Counter(r["outcome"] for r in rs)
        out.append(f"| {m} {wf} | {c['left alone'] + c['test only edit']} | {c['code edit']} | {c['removed feature']} | {st.mean(float(r['lines_changed'] or 0) for r in rs):.1f} | ${st.mean(r['cost'] for r in rs):.2f} |")

# Table 6
out += ["\n## Table 7. Effort and cost per change, defective PRs\n", "| model | steps alone / with | second session (with CA) | cost per change alone / with |", "|---|---|---|---|"]
for m in MODELS:
    a, c = runs("main", m, "alone"), runs("main", m, "CA")
    out.append(f"| {m} | {st.mean(r['agent_steps'] for r in a):.0f} / {st.mean(r['agent_steps'] for r in c):.0f} | {sum(r['sessions'] >= 2 for r in c)} of {len(c)} | ${st.mean(r['cost'] for r in a):.2f} / ${st.mean(r['cost'] for r in c):.2f} |")

# Agreement
m_rs = [r for r in RUNS if r["workflow"] in ("alone", "CA, deletion check off") and r["defect_type"] != "clean" and r["checker_verdict"] in ("gone", "not gone")]
sc = [gone(r) for r in m_rs]; ck = [r["checker_verdict"] == "gone" for r in m_rs]
out += ["\n## Scorer and checker agreement (Alone and ablation runs, defective PRs)\n",
        f"Runs with both verdicts: {len(m_rs)}. Agreement {100 * sum(x == y for x, y in zip(sc, ck)) / len(m_rs):.1f}%, Cohen's kappa {kappa(sc, ck):.2f}. "
        f"Checker gone, scorer not: {sum(y and not x for x, y in zip(sc, ck))}. Scorer gone, checker not: {sum(x and not y for x, y in zip(sc, ck))}."]

# Table 5: ablation of the deletion check (CA as designed vs CA with the check turned off)
out += ["\n## Table 5. Ablation of the deletion check, defective PRs\n", "| configuration | repair rate (Wilson) | cluster bootstrap | defect-gone rate (Wilson) | removed | second session | cost per change |", "|---|---|---|---|---|---|---|"]
for m in MODELS:
    for wf, lab in (("CA", "+ CA"), ("CA, deletion check off", "+ CA, check off")):
        rs = runs("main", m, wf); out.append(config_row(f"{m} {lab}", rs, extra=(str(sum(r["sessions"] >= 2 for r in rs)),)))
out += ["\n| A vs B | repair rate: mean difference [95%] | A only / B only | PR-level p | McNemar p |", "|---|---|---|---|---|"]
for m in MODELS:
    P = paired(runs("main", m, "CA"), runs("main", m, "CA, deletion check off"), fixed)
    out.append(f"| {m} CA vs CA with the check off | {100 * P['diff'][0]:+.0f} pts [{100 * P['diff'][1]:.0f}, {100 * P['diff'][2]:.0f}] | {P['a_only']} / {P['b_only']} | {pv(P['perm'])} | {pv(P['mcnemar'])} |")

# Table 8
def wf_runs(m, wf, clean=False):
    if wf in ("alone", "CA"): return runs("main", m, wf, clean)
    return runs("comparison", m, wf, clean)
out += ["\n## Table 8. Comparison with GitHub Copilot code review (Haiku and Sonnet)\n", "| model | workflow | repair rate (Wilson) | removed | clean: code edits / runs | vs CA: A only / B only, PR-level p |", "|---|---|---|---|---|---|"]
for m in ("Haiku 4.5", "Sonnet 5.5"):
    D = wf_runs(m, "CA")
    for wf in ("alone", "Copilot review", "CA"):
        rs = wf_runs(m, wf); k = sum(map(fixed, rs)); cl = wf_runs(m, wf, clean=True)
        ce = sum(r["outcome"] in ("code edit", "removed feature") for r in cl)
        pc = "" if wf == "CA" else (lambda P: f"{P['a_only']} / {P['b_only']}, {pv(P['perm'])}")(paired(D, rs, fixed))
        out.append(f"| {m} | {wf} | {k}/{len(rs)} = {pct(wilson(k, len(rs)))} | {sum(r['outcome'] == 'removed feature' for r in rs)} | {ce} / {len(cl)} | {pc} |")
out += ["\n| A vs B | A only / B only | PR-level p | McNemar p |", "|---|---|---|---|"]
for m in ("Haiku 4.5", "Sonnet 5.5"):
    for a, b in (("Copilot review", "alone"),):
        P = paired(wf_runs(m, a), wf_runs(m, b), fixed)
        out.append(f"| {m}: {a} vs {b} | {P['a_only']} / {P['b_only']} | {pv(P['perm'])} | {pv(P['mcnemar'])} |")

# Copilot sensitivity: the one PR Copilot could not review, scored as all fixed or all not fixed
out += ["\n## Copilot sensitivity (the excluded PR scored as repaired in all three runs, or in none)\n", "| model | assumption | repair rate | vs alone: PR-level p | vs CA: PR-level p |", "|---|---|---|---|---|"]
for m in ("Haiku 4.5", "Sonnet 5.5"):
    P_ = wf_runs(m, "Copilot review"); have = {r["pr"] for r in P_}
    missing = sorted({r["pr"] for r in wf_runs(m, "alone")} - have)
    for assume in (True, False):
        fake = P_ + [{"pr": pr, "repetition": rep, "outcome": "repaired" if assume else "not repaired"} for pr in missing for rep in (1, 2, 3)]
        k = sum(map(fixed, fake))
        out.append(f"| {m} | {'repaired' if assume else 'not repaired'} | {k}/{len(fake)} = {100 * k / len(fake):.0f}% | {pv(paired(fake, wf_runs(m, 'alone'), fixed)['perm'])} | {pv(paired(fake, wf_runs(m, 'CA'), fixed)['perm'])} |")

# Table 9: detection of the 31 planted defects by tools run out of the box (data/detection.csv)
DET = list(csv.DictReader(open(os.path.join(HERE, "data", "detection.csv"))))
SCOPE = {"CA": None, "rust_build_clippy": {"rust"}, "semgrep": None, "pylint": {"python"}, "sonarqube_community": {"python", "typescript", "java"},
         "ruff": {"python"}, "eslint": {"typescript"}, "clang_tidy": {"cpp"}, "cppcheck": {"cpp"}, "pmd": {"java"}}
hit = lambda r, t: r[t] in ("yes", "partial")
out += ["\n## Table 9. Detection of the planted defects by tools run out of the box\n",
        "| tool | in scope | detected (of which partial) | missed in scope | not covered | not caught (of 31) |", "|---|---|---|---|---|---|"]
for t, langs in SCOPE.items():
    ins = [r for r in DET if langs is None or r["language"] in langs]; k = sum(hit(r, t) for r in ins)
    out.append(f"| {t} | {len(ins)} | {k} ({sum(r[t] == 'partial' for r in ins)}) | {len(ins) - k} | {len(DET) - len(ins)} | {len(DET) - k} |")
free = [t for t in SCOPE if t != "CA"]; u = sum(any(hit(r, t) for t in free) for r in DET)
out.append(f"| all free tools together | {len(DET)} | {u} | {len(DET) - u} | 0 | {len(DET) - u} |")

print("\n".join(out))
