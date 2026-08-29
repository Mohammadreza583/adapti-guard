# CLAIM_EVIDENCE_MAP

Sources: Phase10 matrix claim texts + implemented/evaluated behavior. Phase10 file not modified.

| Claim (operational) | Status | Evidence | Relevant prior work | Problem | Required rewrite |
|---------------------|--------|----------|---------------------|---------|------------------|
| Adaptive defense changes over time | SUPPORTED | Phase7 transitions 25 (↑14/↓11); code PolicyUpdateEngine | SafeHarness, AgentAntibody, SCOUT | Uniqueness not supported | Keep as system property; drop "first/unique" |
| Discrete L0–L3 interventions | SUPPORTED | action_for_level + ACTION_COST | SafeHarness has discrete levels (privilege) | Levels exist elsewhere | Claim AG-specific detect/sanitize/restrict/block semantics, not discrete levels in abstract |
| Runtime escalation | SUPPORTED | INCREASE_DEFENSE on attack_success | SafeHarness escalate; SCOUT escalate to judge | Not unique | Describe AG rule precisely |
| Runtime de-escalation via legitimate+cost | SUPPORTED | REDUCE_DEFENSE gates on legitimate_task & cost | SafeHarness safe-window recovery (different trigger) | Closest overlap | Emphasize legitimate-task cost trigger vs privilege recovery |
| Security–utility tradeoff | SUPPORTED | Adaptive util=1.0 vs Fixed-L3 util=0; SUC artifact | widespread (HARD, SCOUT, SecOPD, CaMeL) | Not novel alone | Protocol-local reporting only |
| Defense-cost awareness | SUPPORTED | cost in reward & de-escalation | SCOUT latency cost; AttriGuard token cost | Cost axes common | Keep as AG metricization of A0–A3 costs |
| Historical signal helps | NOT_SUPPORTED / CONTRADICTED by ablation | hist_changed=false | AgentAntibody/SCOUT/SafeHarness history helps elsewhere | Claiming contribution false | REMOVE / limitation only |
| Adaptive beats all fixed on ASR | NOT_SUPPORTED | Fixed-L3 ASR=0 < Adaptive 0.373 | — | Overclaim | PARTIAL tradeoff only |
| Adaptation beyond fixed levels | PARTIAL | Distinct SUC point vs Fixed-L*; not ASR-dominant | SafeHarness/SCOUT also adaptive intensity | — | Tradeoff wording |
| Handles novel attacks / generalizes | LIMITED | Phase8C novel; detection_rate=0; Phase9 LIMITED | AgentAntibody/HARD stronger transfer claims in their settings | Overgeneralization risk | LIMITED set-specific only |
| Robust to evolving attacks | PARTIAL / UNTESTED vs AutoDojo | Constructed evolving stream; AdaptiveAttacker not primary protocol | COPA/HARD/AutoDojo/Adaptive Adversaries | Threat-model gap | Downgrade; need adaptive attacker eval |
| Unified evaluation framework | PARTIAL | Internal Phase7–10 package | AgentDojo/AutoDojo/SCOUT | Framework uniqueness weak | "Controlled protocol package" not community framework |
| Reproducible multi-seed | SUPPORTED | std=0 n=5 | — | Misread as stochastic robustness | Reproducibility only |
| Q1 algorithmic novelty of adaptive levels | NOT_SUPPORTED | SafeHarness DIRECT-level capability overlap on escalate/de-escalate | SafeHarness | Central uniqueness fails | Reframe to methodological/protocol contribution |
