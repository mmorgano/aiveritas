"""Non-core placeholder explanation scaffolding for issue payloads."""

from __future__ import annotations

from typing import Any


def explain_issue(issue: dict[str, Any]) -> dict[str, Any]:
    """Return placeholder explanation data for a validation issue.

    Args:
        issue: Structured validation issue payload.

    Returns:
        A non-core placeholder object kept for schema continuity.
    """
    issue_code = str(issue.get("code", "unknown_issue"))
    columns = issue.get("scope", {}).get("columns", [])
    scope_label = ", ".join(columns) if columns else "dataset"

    return {
        "status": "placeholder",
        "provider": {
            "name": "stub",
            "model": None,
        },
        "summary": f"Mock explanation generated for '{issue_code}' on {scope_label}.",
        "confidence": "low",
        "possible_causes": [
            "Source data may be incomplete or inconsistent.",
            "Upstream extraction or transformation logic may need review.",
        ],
        "recommended_actions": [
            "Inspect the affected rows and related upstream systems.",
            "Treat this explanation block as placeholder metadata, not as a validation feature.",
        ],
        "metadata": {
            "issue_code": issue_code,
            "issue_stage": issue.get("stage"),
            "llm_integration_ready": False,
            "note": (
                "This response is placeholder scaffolding and not part "
                "of the primary v0.1 workflow."
            ),
        },
    }
