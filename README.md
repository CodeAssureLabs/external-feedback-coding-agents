# Supplement: Fixed or Deleted? External Feedback Lets Cheaper AI Coding Agents Repair Rule Violations

This supplement lets readers recompute every table and statistical test in the paper *Fixed or Deleted? External Feedback Lets Cheaper AI Coding Agents Repair Rule Violations* (Wynter, 2026) from the outcome of each run.

```
python3 analyze.py > results.md
```

The script uses only the Python standard library and takes a few seconds. `results.md` is its output, committed for reference.

## Contents

| Path | Description |
|---|---|
| `data/runs.csv` | One row per run: 1,524 runs, for Alone, CA and the ablation of CA's deletion check (1,350), and the comparison with GitHub Copilot code review (174). |
| `data/detection.csv` | One row per planted defect (31): PR identifier, defect number within the PR, defect type, language, and for CA and each free tool run out of the box whether it detected the defect (`yes`, `partial` when only some of the affected lines were reported, or `no`). |
| `analyze.py` | Recomputes Tables 2 to 11 of the paper, including the build and feature check (Tables 8 and 9), the scorer and checker agreement, and the Copilot sensitivity check. |
| `results.md` | Output of `analyze.py`. |

## Columns of `data/runs.csv`

| Column | Meaning |
|---|---|
| `pr` | Opaque benchmark identifier for the pull request, `PR-01` to `PR-30`. Identifiers are assigned at random and are the same in every study. |
| `defect_type` | `code-visible`, `convention`, `architecture rule`, `multiple` (two or three defects), or `clean` (no defect). |
| `study` | `main` (Alone, CA and the ablation) or `comparison` (Copilot). |
| `model` | `Haiku 4.5`, `Sonnet 5.5` or `Fable 5.1` (API identifiers `claude-haiku-4-5-20251001`, `claude-sonnet-5-5`, `claude-fable-5-1`). |
| `workflow` | `alone`, `CA` (with its deletion check), `CA, deletion check off` (the ablation) or `Copilot review`. |
| `repetition` | 1 to 5 (1 to 3 for `Copilot review`). |
| `outcome` | Defective PRs: `repaired`, `removed feature` (a newly added file deleted or emptied of code, or a rename reverted) or `not repaired`. Clean PRs: `left alone`, `test only edit`, `code edit` or `removed feature`. Definitions are in Section 3.5 of the paper. |
| `sessions` | Agent sessions used (1, or 2 when findings remained after the first). |
| `agent_steps` | Agent turns, as reported by Claude Code. |
| `cost_usd` | Total model cost of the run at list API prices, November 2026: the agent's cost as reported by Claude Code, plus the checker's own cost in CA workflows. |
| `lines_changed` | Lines changed by the final commit, for clean PRs only. |
| `checker_verdict` | Alone and ablation runs on defective PRs only: the checker's own verdict on the final commit (`gone`, `not gone`, or `missing`). Used only for the agreement figure. |
| `build_check` | Runs scored `repaired` on defective PRs only: the result of the build and feature check of the final commit (Section 4.6 of the paper). `passed`, `does not compile` (only errors absent from the PR's own head are counted), `feature removed in place` (the behaviour the PR added was deleted while its file was kept) or `stub`. Empty for all other runs. |

One PR has no `Copilot review` rows, because Copilot repeatedly failed to review it. The paper explains why, and `analyze.py` reports a sensitivity check that scores it as repaired in all three runs or in none.

## Changes in version 2

- One PR (PR-25) was missing the list of files it adds from its scorer specification, so its deletion was not detected. Three runs with that file deleted (two Sonnet 5.5 alone, one Haiku 4.5 with the deletion check off) changed from `repaired` to `removed feature`, as the paper's rules require.
- New column `build_check` and Tables 8 and 9 for the build and feature check. The Copilot comparison and the detection table are now Tables 10 and 11, as in version 2 of the paper.

## What this supplement does and does not allow

It allows a reader to check that every reported rate, interval and p-value follows from the run outcomes, and to run other analyses of them.

It does not allow a reader to re-score the runs. The outcomes are the verdicts of the study team's scorer. The project names, PR contents, planted defects, scorer specifications, agent instructions, checker findings and rules, transcripts and diffs are not included. The study's per-run records are available to reviewers on request under a confidentiality agreement, from hello@codeassurelabs.com.

## Conflict of interest

The author is affiliated with CodeAssure Labs, which develops CodeAssure (CA), the checker studied.

## License

Code (`analyze.py`): MIT, see `LICENSE`. Data (`data/runs.csv`, `results.md`): CC BY 4.0.

## Citation

Wynter, L. (2026). Fixed or Deleted? External Feedback Lets Cheaper AI Coding Agents Repair Rule Violations. Preprint.
