from dataclasses import dataclass
import re


@dataclass
class DetectionResult:
    score: float
    indicators: list[str]
    is_injection: bool


class PromptInjectionDetector:
    """
    Interpretable rule-based prompt injection detector.

    MVP detector for ADAPTI-GUARD.
    """

    PATTERNS = {
        "ignore_previous_instructions": [
            r"\bignore\s+(all\s+)?previous\s+instructions?\b",
            r"\bignore\s+(all\s+)?prior\s+instructions?\b",
        ],

        "follow_instead": [
            r"\bfollow\s+this\s+instruction\s+instead\b",
            r"\bfollow\s+the\s+following\s+instruction\b",
        ],

        "system_prompt_extraction": [
            r"\breveal\s+(your\s+)?system\s+prompt\b",
            r"\bshow\s+(me\s+)?your\s+system\s+prompt\b",
            r"\bprint\s+(your\s+)?system\s+prompt\b",
            r"\breveal\s+protected\s+information\b",
        ],

        "instruction_override": [
            r"\byou\s+are\s+now\b",
            r"\bnew\s+instructions?\b",
            r"\boverride\s+(the\s+)?instructions?\b",
            r"\bsuperseded\b",
            r"\bno\s+longer\s+applicable\b",
        ],

        "system_authority_impersonation": [
            r"\bsystem\s+(update|message|instruction)\b",
            r"\btrusted\s+(system\s+)?instruction\b",
            r"\bhigher\s+priority\b",
            r"\bsystem\s+authorizes?\b",
            r"\bsystem\s+has\s+authorized\b",
        ],

        "tool_output_injection": [
            r"\btool\s+result\b",
            r"\btool\s+output\b",
            r"\btrusted\s+tool\s+output\b",
            r"\bexecute\s+the\s+following\s+instruction\b",
        ],

        "context_manipulation": [
            r"\bsecurity\s+policy\s+was\s+updated\b",
            r"\bsecurity\s+policy\s+has\s+been\s+updated\b",
            r"\bprevious\s+security\s+policy\b",
            r"\bprevious\s+safety\s+constraints\b",
            r"\bconstraints\s+have\s+been\s+superseded\b",
            r"\binstructions\s+contained\s+in\s+this\s+context\b",
        ],

        "jailbreak_language": [
            r"\bbypass\s+(the\s+)?(safety|security)\b",
            r"\bdisable\s+(the\s+)?safety\b",
            r"\bdo\s+not\s+follow\s+(the\s+)?rules\b",
        ],

        "secret_extraction": [
            r"\breveal\s+(the\s+)?secret\b",
            r"\bshow\s+(me\s+)?confidential\b",
            r"\bexfiltrate\b",
        ],
    }

    def detect(self, text: str) -> DetectionResult:
        if not text:
            return DetectionResult(
                score=0.0,
                indicators=[],
                is_injection=False,
            )

        text_lower = text.lower()
        indicators = []

        for category, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    indicators.append(category)
                    break

        # Each independent indicator contributes 0.25.
        score = min(len(indicators) * 0.25, 1.0)

        return DetectionResult(
            score=score,
            indicators=indicators,
            is_injection=score >= 0.25,
        )
