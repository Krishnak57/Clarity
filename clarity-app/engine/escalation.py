"""Human-in-the-loop escalation — threshold + high-stakes logic, directory lookup.

Escalation is ALWAYS available and AUTO-surfaced when:
  - retrieval confidence is low (the abstain gate fired), OR
  - the topic is high-stakes (immigration / legal / financial / status-affecting).

This is the honest answer to "what if the AI is wrong?": a real human owns the
high-stakes call.
"""
import json
from functools import lru_cache

import config


@lru_cache(maxsize=1)
def load_directory() -> list[dict]:
    with open(config.ESCALATION_PATH, encoding="utf-8") as f:
        return json.load(f)


def is_high_stakes(text: str) -> bool:
    """True if the text touches immigration / legal / status-affecting topics."""
    low = text.lower()
    return any(kw in low for kw in config.HIGH_STAKES_KEYWORDS)


def contacts_for(journey: str | None, query: str = "") -> list[dict]:
    """Return the most relevant human contacts for a journey/query.

    Prefers contacts mapped to the journey; for high-stakes queries also includes
    the immigration/legal contacts. Falls back to the full directory so the user
    is never left without a human to call.
    """
    directory = load_directory()
    chosen: list[dict] = []

    for entry in directory:
        if journey and journey in entry.get("journeys", []):
            chosen.append(entry)

    if is_high_stakes(query):
        for entry in directory:
            if entry not in chosen and (
                "immigration" in entry["topic"].lower()
                or "legal" in entry["topic"].lower()
            ):
                chosen.append(entry)

    if not chosen:
        chosen = list(directory)
    return chosen


def should_escalate(abstain: bool, query: str) -> tuple[bool, str]:
    """Decide whether to auto-surface escalation and why.

    Returns (escalate, reason). Escalation is always *offered* in the UI; this
    flags when it must be auto-surfaced and prominently shown.
    """
    if abstain:
        return True, "low_confidence"
    if is_high_stakes(query):
        return True, "high_stakes"
    return False, ""


if __name__ == "__main__":
    for q, j in [
        ("How do I open a bank account?", "A_bank_account"),
        ("Will using benefits affect my visa status?", "C_benefits"),
        ("random unrelated question", None),
    ]:
        esc, reason = should_escalate(abstain=(j is None), query=q)
        print(f"\nQ: {q}\n  escalate={esc} reason='{reason}' high_stakes={is_high_stakes(q)}")
        for c in contacts_for(j, q):
            print(f"  -> {c['contact_name']} ({c['contact_type']}): {c['how_to_reach']}")
