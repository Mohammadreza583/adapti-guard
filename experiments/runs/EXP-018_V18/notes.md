# EXP-018 — V17 Held-Out Validation Re-run

## Purpose
Independent re-run of the V17 detector on the held-out NotInject validation set.

## Result

- N = 144
- TP = 17
- TN = 78
- FP = 18
- FN = 31
- Precision = 0.4857
- Recall = 0.3542
- F1 = 0.4096
- Balanced Accuracy = 0.5833
- FPR = 0.1875
- FNR = 0.6458

## Conclusion
The held-out result reproduces the previous V17 validation result.
The observed poor generalization is therefore reproducible.

## Interpretation
The current detector should not be promoted to the final model based on the development/smoke result.
Next work should address source/domain heterogeneity and detector feature coverage.
