from src.adapti_guard.core.pipeline import DefensePipeline


pipeline = DefensePipeline()


def adapti_guard_generate(prompt: str, **kwargs):
    result = pipeline.run(
        text=prompt,
        contextual_risk=kwargs.get("contextual_risk", 0.0),
        tool_sensitive=kwargs.get("tool_sensitive", False),
    )

    return [result.response]
