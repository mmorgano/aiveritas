"""Placeholder AI integration for issue explanations."""

from __future__ import annotations

from typing import Any


def explain_issue(issue: dict[str, Any]) -> dict[str, Any]:
    """Return a placeholder AI explanation for a validation issue.

    Args:
        issue: Structured validation issue payload.

    Returns:
        A mock explanation object prepared for future LLM integration.
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
            "Replace this stub with a real LLM-backed explanation service later.",
        ],
        "metadata": {
            "issue_code": issue_code,
            "issue_stage": issue.get("stage"),
            "llm_integration_ready": False,
            "note": "This response is a placeholder for future LLM integration.",
        },
    }
