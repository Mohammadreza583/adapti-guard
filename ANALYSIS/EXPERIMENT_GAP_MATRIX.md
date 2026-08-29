# EXPERIMENT_GAP_MATRIX

| # | Experiment | Status in AG | Necessity | Why (one sentence) |
|---|------------|--------------|-----------|--------------------|
| 1 | Fixed L0 | DONE (Phase7/8) | NECESSARY | Anchor undefended baseline for SUC comparison. |
| 2 | Fixed L1 | DONE | NECESSARY | Intermediate fixed intervention reference. |
| 3 | Fixed L2 | DONE | NECESSARY | Intermediate fixed intervention reference. |
| 4 | Fixed L3 | DONE | NECESSARY | Max-security fixed baseline exposing utility collapse. |
| 5 | Escalate-only | MISSING | NECESSARY | Isolates whether de-escalation is causally responsible for utility preservation. |
| 6 | Adaptive + de-escalation (full) | DONE | NECESSARY | Primary method condition. |
| 7 | Legitimate-heavy workload | MISSING | HIGH-VALUE | Stress-tests de-escalation and over-defense under higher N_l. |
| 8 | Mixed attack/legitimate 75/25 | DONE | NECESSARY | Enables non-vacuous utility and de-escalation. |
| 9 | Adaptive/black-box attacker (AutoDojo-like) | MISSING (class exists; not primary eval) | NECESSARY for evolving claims | Without it, evolving-robustness claims stay PARTIAL under Q1 threat models. |
| 10 | Multi-seed | DONE but std=0 | HIGH-VALUE | Keep for reproducibility; not stochastic robustness. |
| 11 | Ablation of de-escalation | MISSING (same as escalate-only) | NECESSARY | Core differentiator vs escalate-only / SafeHarness comparison needs this. |
| 12 | Cost/utility/security Pareto | DONE (known scenario) | NECESSARY | Documents tradeoff contribution; extend under adaptive attacker if claims strengthened. |
| — | vs SafeHarness-style privilege degradation | MISSING | HIGH-VALUE | Closest discrete-level baseline; without it novelty positioning stays weak. |
| — | Historical-signal non-null regime | MISSING | OPTIONAL | Only if pursuing C6; currently correctly NOT_SUPPORTED. |
