from src.adapti_guard.experiments.experiment_runner import ExperimentRunner

runner = ExperimentRunner()
results = runner.run(episodes=50)

runner.save_results(
    results,
    "results/mvp_50_episodes.json",
)

print("=" * 60)
print("ADAPTI-GUARD MVP")
print("=" * 60)

for r in results:
    print(
        f"Episode {r.episode_id:02d} | "
        f"Family={r.attack_family} | "
        f"Risk={r.risk_score:.3f} | "
        f"Level={r.risk_level} | "
        f"Action={r.defense_action} | "
        f"AttackSuccess={r.attack_success} | "
        f"DefenseLevel={r.defense_level}"
    )

n = len(results)

asr = sum(r.attack_success for r in results) / n
security = sum(r.security_score for r in results) / n
utility = sum(r.utility_score for r in results) / n
cost = sum(r.defense_cost for r in results) / n

print("=" * 60)
print(f"Episodes:            {n}")
print(f"Attack Success Rate: {asr:.3f}")
print(f"Security Score:      {security:.3f}")
print(f"Utility Score:       {utility:.3f}")
print(f"Average Cost:        {cost:.3f}")
print("=" * 60)
print("Saved: results/mvp_50_episodes.json")
