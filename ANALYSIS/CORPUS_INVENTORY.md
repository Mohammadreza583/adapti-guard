# CORPUS_INVENTORY

Generated: 2026-08-29T12:40:28.345382+00:00

## Authoritative corpus status

**TOTAL--/ NOT FOUND** in this environment.

Searched paths (all missing):
- `/mnt/c/Users/MohammadReza/Desktop/adapti-guard/paper/references/TOTAL--`
- `/workspace/TOTAL--`
- `/workspace/paper/references/TOTAL--`
- `15_BASE_Q1/` (missing; Adapti-Guard audited from `/workspace/src/adapti_guard/` + `results/`)

Requested groups not present locally:
`01_CORE/`, `02_AGENT_SECURITY/`, `03_DEFENSE/`, `04_BACKGROUND/`, `05_2025_2026/`, `07_VERIFIED_AGENT_PAPERS/`, `supporting/`, `15_BASE_Q1/`, `ANALYSIS/TXT/`

`.venv/` / `site-packages/` not scanned.

## Fallback inventory (incomplete)

Because TOTAL-- is absent, unique papers below are from previously retrieved full-text extracts under agent-tools (actual paper text, not titles alone). This is **NOT** a complete local-corpus inventory. Duplicates of the same work (multiple HTML/PDF extracts) are collapsed once.

### Unique papers retained for audit (n=20)

| ID | Paper | ArXiv (if known) | Category (proxy) |
|----|-------|------------------|------------------|
| P01 | AgentAntibody | 2608.04053 | supporting / adaptive runtime |
| P02 | COPA | 2608.19982 | supporting / continual defense |
| P03 | Beyond Handcrafted / HARD | 2608.12977 | supporting / self-evolving runtime |
| P04 | Send a SCOUT First | 2605.30837 | supporting / detector allocation |
| P05 | SecOPD | 2608.21500 | supporting / training-time |
| P06 | Adaptive Adversaries | 2607.18063 | supporting / adaptive attacker eval |
| P07 | AutoDojo | 2606.15057 | supporting / adaptive IPI eval |
| P08 | SafeHarness | 2604.13630 | agent security / levels |
| P09 | CaMeL (Defeating PI by Design) | 2503.18813 | defense / system-level |
| P10 | Progent | 2504.11703 | defense / privilege control |
| P11 | Meta SecAlign | 2507.02735 | defense / model-level |
| P12 | AttriGuard | 2603.10749 | agent security / causal attribution |
| P13 | AgentVisor | 2604.24118 | agent security / semantic virtualization |
| P14 | SHE | 2608.09885 | harness evolution |
| P15 | HarnessX | 2606.14249 | harness foundry (adjacent) |
| P16 | Adapting the Interface (runtime harness adaptation) | 2605.22166 | harness adaptation |
| P17 | ProbGuard | 2508.00500 | runtime monitoring |
| P18 | AgentSentinel | 2509.07764 | computer-use agent defense |
| P19 | Adaptive Evaluation of Out-of-Band Defenses | 2606.26479 | evaluation / out-of-band |
| P20 | From Craft to Kernel | 2604.18652 | background / governance architecture |

### Duplicates collapsed

- COPA: multiple HTML extracts → one
- AgentAntibody: abs+html → one
- HARD: two HTML copies → one
- AttriGuard: PDF+HTML → one
- AutoDojo: abs+blog commentary → paper once; commentary excluded as secondary
- SCOUT: paper retained; "Scout: Disambiguating a Multifaceted Research Name" excluded (meta topic page)

### Papers / files excluded

| Item | Reason |
|------|--------|
| Scout disambiguation page | Not a defense method paper |
| Alam modular multi-agent framework PDF | Not primarily PI adaptive-defense contribution |
| AgentBound extract (partial) | Incomplete/ambiguous extract; insufficient for matrix without TOTAL-- PDF |
| Any `.venv` / site-packages PDFs | Excluded by rule |
| Generated analysis JSONs | Not literature |

### Category counts (fallback only)

- Core/defense/system-level: P09–P11, P19–P20
- Agent security / runtime: P08, P12–P18
- Supporting adaptive/evolving: P01–P07
- Background: P20

**Core papers (local TOTAL--) = 0**  
**Supporting papers (local TOTAL--) = 0**  
**Relevant unique papers in fallback = 20**
