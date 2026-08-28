# EXP-017 — V17

## Objective
Improve detector precision without sacrificing recall.

## Change
Precision-oriented contextual gating.

## Corrective Action
Fixed incorrectly escaped regular expressions in V15/V17-related code:
`\\b`, `\\s`, `\\w` → `\b`, `\s`, `\w`.

## Dataset
NotInject
Smoke split
N = 1000

## Validated Result

- TP: 310
- TN: 537
- FP: 37
- FN: 116
- Precision: 0.8934
- Recall: 0.7277
- F1: 0.8021
- Balanced Accuracy: 0.8316
- FPR: 0.0645
- FNR: 0.2723

## Previous Invalid Result

The first V17 evaluation produced:

- Precision: 0.9711
- Recall: 0.5516
- F1: 0.7036
- Balanced Accuracy: 0.7697
- FPR: 0.0122
- FNR: 0.4484

That result is superseded because incorrectly escaped regular expressions were identified and corrected before the validated rerun.

## Comparison with V16

V16:
- Precision = 0.8270
- Recall = 0.7183
- F1 = 0.7688
- Balanced Accuracy = 0.8034
- FPR = 0.1115
- FNR = 0.2817

V17:
- Precision = 0.8934
- Recall = 0.7277
- F1 = 0.8021
- Balanced Accuracy = 0.8316
- FPR = 0.0645
- FNR = 0.2723

## Decision
V17 is currently the strongest validated detector version among V16 and V17.

## Next Action
Evaluate V17 on the held-out validation set and then integrate the detector into the full Adapti-Guard pipeline.
