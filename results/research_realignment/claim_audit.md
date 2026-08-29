# Claim Audit

Generated: 2026-08-29T15:36:31.416191+00:00

Source: Phase10 `claim_evidence_matrix_v1.json` + Phase11 novelty statuses + code wiring.

| Claim | Phase10 | Action | Reason |
| ----- | ------- | ------ | ------ |
| C1: Adaptive defense changes defense policy over time. | SUPPORTED | **KEEP** | Supported: policy changes over time (transitions observed). Drop uniqueness. |
| C2: Adaptive defense provides meaningful security against prompt injection. | PARTIALLY SUPPORTED | **WEAKEN** | Security is tradeoff-local vs Fixed-L3 ASR=0; do not claim absolute superiority. |
| C3: Adaptive defense preserves utility while applying defense. | SUPPORTED | **KEEP** | Utility preserved under protocol (util=1.0 vs Fixed-L3 util=0). Scope to protocol. |
| C4: Adaptive defense has a measurable security–utility–cost tradeoff. | SUPPORTED | **KEEP** | SUC metrics exist and discriminate methods. |
| C5: Adaptation contributes beyond fixed defense levels. | PARTIALLY SUPPORTED | **WEAKEN** | Adaptation beyond fixed is PARTIAL (SUC point), not ASR-dominance. |
| C6: Historical attack feedback contributes to adaptation. | NOT SUPPORTED | **REMOVE** | historical_signal_changed_aggregates=false — cannot be a contribution. |
| C7: Performance differs across attack families. | SUPPORTED | **KEEP** | Family differences supported; descriptive only. |
| C8: Adaptive defense can handle novel attacks. | LIMITED | **WEAKEN** | LIMITED novel-set evidence; ban open-world wording. |
| C9: Adaptive defense can respond to evolving attack sequences. | PARTIALLY SUPPORTED | **WEAKEN** | Constructed evolving stream ≠ AutoDojo adaptive optimizer; say “evaluated under constructed evolving sequences”. |
| C10: Results are reproducible across seeds. | SUPPORTED | **WEAKEN** | Reproducible yes; std=0 means determinism check not stochastic robustness. |

## Banned without stronger evidence
- first / novel / state-of-the-art / solves / guarantees
- robust against adaptive attackers (use: evaluated under adaptive/constructed evolving conditions)
- historical feedback improves adaptation

## KEEP contribution spine
1. Discrete L0–L3 intervention policy with escalate/de-escalate rules (non-unique levels; AG-specific semantics/triggers).
2. Mixed-workload fixed-vs-adaptive SUC comparison under controlled protocol.
3. Evidence-bounded reporting including null historical ablation.
