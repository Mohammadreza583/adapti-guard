# Final Research Position

Generated: 2026-08-29T15:36:31.416191+00:00

1. **Problem:** LLM agents need runtime defenses that balance security, utility, and defense cost as attack pressure and legitimate traffic mix change.
2. **Existing limitation:** Many defenses are static (prompt/model/system) or adapt in other regimes (training continual, detector allocation, privilege harness recovery) without AG’s intervention-level mixed SUC protocol.
3. **Research gap (bounded):** Controlled comparison of discrete sanitize/restrict/block levels with attack escalation + legitimate-cost de-escalation vs fixed levels under mixed workloads; AutoDojo-class adaptive attacker still open for AG.
4. **ADAPTI-GUARD contribution:** An MVP runtime controller over L0–L3 interventions with explicit escalate/de-escalate rules and a frozen mixed-workload SUC evaluation against fixed levels.
5. **Genuine novelty:** Provisional methodological/protocol package (fixed-vs-adaptive discrete intervention SUC under mixed 75/25). Not uniqueness of discrete adaptive levels.
6. **Non-novel aspects:** Escalate/de-escalate levels (SafeHarness); SUC tradeoffs (SCOUT/HARD); runtime memory adaptation (AgentAntibody); adaptive attackers as eval idea (AutoDojo).
7. **Evaluation hypothesis:** Under the controlled mixed protocol, adaptive L0–L3 yields a distinct SUC operating point vs fixed levels (utility preserved vs Fixed-L3) without claiming ASR dominance or open-world robustness.
8. **Required experiments (future, non-destructive):** escalate-only ablation; optional live AdaptiveAttacker/AutoDojo-style eval; optional legitimate-heavy sensitivity.
9. **Expected contribution:** Defensible Q1-positioned empirical study of cost-aware discrete intervention-level control under mixed workloads — contingent on honest claim boundaries.
