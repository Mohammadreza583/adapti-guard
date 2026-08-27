from dataclasses import dataclass

from src.adapti_guard.core.models import DefenseAction


@dataclass
class DefenseResult:
    action: DefenseAction
    allowed: bool
    content: str
    tool_access: bool
    reason: str


class DefenseActionLayer:
    """
    Executes the defense action selected by the policy engine.

    MVP implementation:
    A0 = allow
    A1 = sanitize
    A2 = restrict tools
    A3 = block
    """

    def execute(
        self,
        action: DefenseAction,
        content: str,
    ) -> DefenseResult:

        if action == DefenseAction.NO_INTERVENTION:
            return DefenseResult(
                action=action,
                allowed=True,
                content=content,
                tool_access=True,
                reason="no_intervention",
            )

        if action == DefenseAction.SANITIZE:
            sanitized = self._sanitize(content)

            return DefenseResult(
                action=action,
                allowed=True,
                content=sanitized,
                tool_access=True,
                reason="content_sanitized",
            )

        if action == DefenseAction.TOOL_RESTRICTION:
            return DefenseResult(
                action=action,
                allowed=True,
                content=content,
                tool_access=False,
                reason="tool_access_restricted",
            )

        if action == DefenseAction.BLOCK:
            return DefenseResult(
                action=action,
                allowed=False,
                content="",
                tool_access=False,
                reason="interaction_blocked",
            )

        raise ValueError(f"Unsupported defense action: {action}")

    def _sanitize(self, content: str) -> str:
        """
        Lightweight MVP sanitization.

        Removes common instruction-like attack markers while
        preserving the remaining user/content text.
        """

        patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "ignore prior instructions",
            "reveal your system prompt",
        ]

        import re

        sanitized = content

        for pattern in patterns:
            sanitized = re.sub(
                re.escape(pattern),
                "",
                sanitized,
                flags=re.IGNORECASE,
            )

        return sanitized.strip()
