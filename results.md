# Recomputed results

## Table 2. Alone and CA, defective PRs

| configuration | repair rate (Wilson) | cluster bootstrap | defect-gone rate (Wilson) | removed | cost per change |
|---|---|---|---|---|---|
| Haiku 4.5 alone | 35/125 = 28% [21, 36] | [13, 44] | 48/125 = 38% [30, 47] | 13 | $0.18 [0.14, 0.23] |
| Haiku 4.5 + CA | 107/125 = 86% [78, 91] | [75, 94] | 114/125 = 91% [85, 95] | 7 | $0.42 [0.31, 0.53] |
| Sonnet 5.5 alone | 59/125 = 47% [39, 56] | [30, 65] | 90/125 = 72% [64, 79] | 31 | $0.06 [0.06, 0.07] |
| Sonnet 5.5 + CA | 118/125 = 94% [89, 97] | [86, 100] | 120/125 = 96% [91, 98] | 2 | $0.17 [0.14, 0.19] |
| Fable 5.1 alone | 56/125 = 45% [36, 54] | [28, 62] | 100/125 = 80% [72, 86] | 44 | $0.91 [0.76, 1.08] |
| Fable 5.1 + CA | 125/125 = 100% [97, 100] | [100, 100] | 125/125 = 100% [97, 100] | 0 | $1.73 [1.32, 2.18] |

## Table 3. Paired comparisons

| A vs B | repair rate: mean difference [95%] | A only / B only | PR-level p | McNemar p | defect gone: A only / B only | PR-level p | McNemar p |
|---|---|---|---|---|---|---|---|
| Haiku 4.5 CA vs Haiku 4.5 alone | +58 pts [38, 74] | 77 / 5 | < 0.001 | < 0.001 | 72 / 6 | < 0.001 | < 0.001 |
| Sonnet 5.5 CA vs Sonnet 5.5 alone | +47 pts [28, 66] | 62 / 3 | < 0.001 | < 0.001 | 33 / 3 | 0.014 | < 0.001 |
| Fable 5.1 CA vs Fable 5.1 alone | +55 pts [38, 72] | 69 / 0 | < 0.001 | < 0.001 | 25 / 0 | 0.016 | < 0.001 |
| Sonnet 5.5 CA vs Fable 5.1 alone | +50 pts [33, 66] | 62 / 0 | < 0.001 | < 0.001 | 25 / 5 | 0.062 | < 0.001 |
| Haiku 4.5 CA vs Fable 5.1 alone | +41 pts [20, 60] | 59 / 8 | 0.0013 | < 0.001 | 25 / 11 | 0.27 | 0.029 |

## Table 4. Runs repaired, by defect type

| configuration | code-visible | convention | architecture rule | multiple |
|---|---|---|---|---|
| Haiku 4.5 alone | 15/15 | 11/40 | 5/45 | 4/25 |
| Sonnet 5.5 alone | 15/15 | 20/40 | 19/45 | 5/25 |
| Fable 5.1 alone | 14/15 | 21/40 | 13/45 | 8/25 |
| Haiku 4.5 CA | 11/15 | 38/40 | 35/45 | 23/25 |
| Sonnet 5.5 CA | 15/15 | 40/40 | 41/45 | 22/25 |
| Fable 5.1 CA | 15/15 | 40/40 | 45/45 | 25/25 |

## Table 6. Clean PRs

| configuration | left alone (incl. test-only) | code edit | removed | mean lines changed | mean cost |
|---|---|---|---|---|---|
| Haiku 4.5 alone | 9 | 16 | 0 | 7.8 | $0.11 |
| Sonnet 5.5 alone | 0 | 25 | 0 | 8.5 | $0.06 |
| Fable 5.1 alone | 0 | 20 | 5 | 21.6 | $0.73 |
| Haiku 4.5 CA | 25 | 0 | 0 | 0.0 | $0.04 |
| Sonnet 5.5 CA | 25 | 0 | 0 | 0.0 | $0.03 |
| Fable 5.1 CA | 25 | 0 | 0 | 0.0 | $0.27 |

## Table 7. Effort and cost per change, defective PRs

| model | steps alone / with | second session (with CA) | cost per change alone / with |
|---|---|---|---|
| Haiku 4.5 | 43 / 60 | 41 of 125 | $0.18 / $0.42 |
| Sonnet 5.5 | 12 / 16 | 46 of 125 | $0.06 / $0.17 |
| Fable 5.1 | 22 / 34 | 18 of 125 | $0.91 / $1.73 |

## Scorer and checker agreement (Alone and ablation runs, defective PRs)

Runs with both verdicts: 748. Agreement 94.8%, Cohen's kappa 0.84. Checker gone, scorer not: 24. Scorer gone, checker not: 15.

## Table 5. Ablation of the deletion check, defective PRs

| configuration | repair rate (Wilson) | cluster bootstrap | defect-gone rate (Wilson) | removed | second session | cost per change |
|---|---|---|---|---|---|---|
| Haiku 4.5 + CA | 107/125 = 86% [78, 91] | [75, 94] | 114/125 = 91% [85, 95] | 7 | 41 | $0.42 [0.31, 0.53] |
| Haiku 4.5 + CA, check off | 89/125 = 71% [63, 78] | [57, 84] | 108/125 = 86% [79, 91] | 19 | 33 | $0.37 [0.28, 0.46] |
| Sonnet 5.5 + CA | 118/125 = 94% [89, 97] | [86, 100] | 120/125 = 96% [91, 98] | 2 | 46 | $0.17 [0.14, 0.19] |
| Sonnet 5.5 + CA, check off | 92/125 = 74% [65, 81] | [58, 87] | 121/125 = 97% [92, 99] | 29 | 19 | $0.14 [0.12, 0.15] |
| Fable 5.1 + CA | 125/125 = 100% [97, 100] | [100, 100] | 125/125 = 100% [97, 100] | 0 | 18 | $1.73 [1.32, 2.18] |
| Fable 5.1 + CA, check off | 108/125 = 86% [79, 91] | [73, 98] | 125/125 = 100% [97, 100] | 17 | 7 | $1.22 [1.01, 1.45] |

| A vs B | repair rate: mean difference [95%] | A only / B only | PR-level p | McNemar p |
|---|---|---|---|---|
| Haiku 4.5 CA vs CA with the check off | +14 pts [3, 27] | 27 / 9 | 0.036 | 0.0039 |
| Sonnet 5.5 CA vs CA with the check off | +21 pts [7, 35] | 30 / 4 | 0.0098 | < 0.001 |
| Fable 5.1 CA vs CA with the check off | +14 pts [2, 27] | 17 / 0 | 0.12 | < 0.001 |

## Table 10. Comparison with GitHub Copilot code review (Haiku and Sonnet)

| model | workflow | repair rate (Wilson) | removed | clean: code edits / runs | vs CA: A only / B only, PR-level p |
|---|---|---|---|---|---|
| Haiku 4.5 | alone | 35/125 = 28% [21, 36] | 13 | 16 / 25 | 77 / 5, < 0.001 |
| Haiku 4.5 | Copilot review | 29/72 = 40% [30, 52] | 13 | 12 / 15 | 38 / 5, < 0.001 |
| Haiku 4.5 | CA | 107/125 = 86% [78, 91] | 7 | 0 / 25 |  |
| Sonnet 5.5 | alone | 59/125 = 47% [39, 56] | 31 | 25 / 25 | 62 / 3, < 0.001 |
| Sonnet 5.5 | Copilot review | 33/72 = 46% [35, 57] | 9 | 12 / 15 | 37 / 1, < 0.001 |
| Sonnet 5.5 | CA | 118/125 = 94% [89, 97] | 2 | 0 / 25 |  |

| A vs B | A only / B only | PR-level p | McNemar p |
|---|---|---|---|
| Haiku 4.5: Copilot review vs alone | 17 / 9 | 0.35 | 0.17 |
| Sonnet 5.5: Copilot review vs alone | 8 / 12 | 0.65 | 0.5 |

## Copilot sensitivity (the excluded PR scored as repaired in all three runs, or in none)

| model | assumption | repair rate | vs alone: PR-level p | vs CA: PR-level p |
|---|---|---|---|---|
| Haiku 4.5 | repaired | 32/75 = 43% | 0.21 | < 0.001 |
| Haiku 4.5 | not repaired | 29/75 = 39% | 0.35 | < 0.001 |
| Sonnet 5.5 | repaired | 36/75 = 48% | 1.0 | < 0.001 |
| Sonnet 5.5 | not repaired | 33/75 = 44% | 0.65 | < 0.001 |

## Table 11. Detection of the planted defects by tools run out of the box

| tool | in scope | detected (of which partial) | missed in scope | not covered | not caught (of 31) |
|---|---|---|---|---|---|
| CA | 31 | 31 (7) | 0 | 0 | 0 |
| rust_build_clippy | 10 | 6 (3) | 4 | 21 | 25 |
| semgrep | 31 | 2 (0) | 29 | 0 | 29 |
| pylint | 7 | 1 (0) | 6 | 24 | 30 |
| sonarqube_community | 9 | 1 (1) | 8 | 22 | 30 |
| ruff | 7 | 0 (0) | 7 | 24 | 31 |
| eslint | 1 | 0 (0) | 1 | 30 | 31 |
| clang_tidy | 12 | 0 (0) | 12 | 19 | 31 |
| cppcheck | 12 | 0 (0) | 12 | 19 | 31 |
| pmd | 1 | 0 (0) | 1 | 30 | 31 |
| all free tools together | 31 | 8 | 23 | 0 | 23 |

## Table 8. Build and feature check by language (runs scored as repaired, all workflows; last column +CA only)

| language | checked | do not compile | removed in place or stub | failed with +CA |
|---|---|---|---|---|
| java | 51 | 0 | 0 | 0 of 15 |
| typescript | 30 | 0 | 0 | 0 of 15 |
| python | 202 | 0 | 21 | 8 of 70 |
| cpp | 305 | 16 | 2 | 8 of 137 |
| rust | 263 | 34 | 2 | 19 of 113 |
| total | 851 | 50 | 25 | 35 of 350 |

## Table 9. Repair rate under the static scorer and after the build and feature check, defective PRs

| model | workflow | static scorer | build-checked (Wilson) | build-checked cluster bootstrap |
|---|---|---|---|---|
| Haiku 4.5 | alone | 35/125 | 32/125 = 26% [19, 34] | [11, 41] |
| Haiku 4.5 | CA | 107/125 | 86/125 = 69% [60, 76] | [54, 82] |
| Haiku 4.5 | CA, deletion check off | 89/125 | 67/125 = 54% [45, 62] | [40, 67] |
| Haiku 4.5 | Copilot review | 29/72 | 23/72 = 32% [22, 43] | [17, 49] |
| Sonnet 5.5 | alone | 59/125 | 57/125 = 46% [37, 54] | [28, 63] |
| Sonnet 5.5 | CA | 118/125 | 113/125 = 90% [84, 94] | [79, 99] |
| Sonnet 5.5 | CA, deletion check off | 92/125 | 87/125 = 70% [61, 77] | [54, 84] |
| Sonnet 5.5 | Copilot review | 33/72 | 33/72 = 46% [35, 57] | [28, 64] |
| Fable 5.1 | alone | 56/125 | 56/125 = 45% [36, 54] | [28, 62] |
| Fable 5.1 | CA | 125/125 | 116/125 = 93% [87, 96] | [83, 100] |
| Fable 5.1 | CA, deletion check off | 108/125 | 106/125 = 85% [77, 90] | [70, 96] |

### Paired comparisons, build-checked repair rate

| A vs B | mean difference [95%] | A only / B only | PR-level p | McNemar p |
|---|---|---|---|---|
| Haiku 4.5 CA vs Haiku 4.5 alone | +43 pts [23, 62] | 63 / 9 | < 0.001 | < 0.001 |
| Sonnet 5.5 CA vs Sonnet 5.5 alone | +45 pts [26, 64] | 59 / 3 | < 0.001 | < 0.001 |
| Fable 5.1 CA vs Fable 5.1 alone | +48 pts [31, 65] | 60 / 0 | < 0.001 | < 0.001 |
| Sonnet 5.5 CA vs Fable 5.1 alone | +46 pts [29, 62] | 58 / 1 | < 0.001 | < 0.001 |
| Haiku 4.5 CA vs Fable 5.1 alone | +24 pts [-1, 47] | 50 / 20 | 0.075 | < 0.001 |
| Haiku 4.5 CA vs Haiku 4.5 CA, deletion check off | +15 pts [4, 27] | 32 / 13 | 0.023 | 0.0066 |
| Sonnet 5.5 CA vs Sonnet 5.5 CA, deletion check off | +21 pts [7, 35] | 30 / 4 | 0.0098 | < 0.001 |
| Fable 5.1 CA vs Fable 5.1 CA, deletion check off | +8 pts [-2, 19] | 13 / 3 | 0.25 | 0.021 |
| Haiku 4.5 CA vs Haiku 4.5 Copilot review | +40 pts [19, 60] | 33 / 4 | 0.0021 | < 0.001 |
| Sonnet 5.5 CA vs Sonnet 5.5 Copilot review | +46 pts [28, 64] | 34 / 1 | < 0.001 | < 0.001 |

Runs repaired and passing the check: CA 315/375, alone 145/375.
