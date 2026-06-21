"""Checklist formatter — turns grounded structured steps into an ordered list.

Each rendered step carries fields straight from the SOURCE CHUNK metadata
(source name, official link, last-verified date, confidence flag), so nothing on
screen is a model-invented citation. The model only supplies the plain-language
action and which passage it used.
"""
import config


def _is_verified_date(date_str: str) -> bool:
    """A date counts as verified only if it is a real value, not a placeholder."""
    if not date_str:
        return False
    return "[TO VERIFY]" not in date_str and "TO VERIFY" not in date_str


def build_checklist(structured: dict, chunks: list[dict], high_stakes: bool) -> list[dict]:
    """Attach real source metadata to each LLM step.

    Returns a list of step dicts:
        order, action, documents, source_name, source_url,
        last_verified_date, confidence ("verified" | "check_human")
    """
    steps_out = []
    for i, step in enumerate(structured.get("steps", []), start=1):
        passage_no = step.get("source_passage")
        chunk = None
        if isinstance(passage_no, int) and 1 <= passage_no <= len(chunks):
            chunk = chunks[passage_no - 1]
        elif chunks:
            chunk = chunks[0]  # fallback: best-scoring chunk

        date = chunk.get("last_verified_date") if chunk else None
        # Confidence: verified only if the source date is real AND not high-stakes.
        confidence = "verified" if (_is_verified_date(date) and not high_stakes) else "check_human"

        steps_out.append({
            "order": i,
            "action": step.get("action", ""),
            "documents": step.get("documents", []) or [],
            "source_name": chunk.get("source_name") if chunk else None,
            "source_url": chunk.get("source_url") if chunk else None,
            "last_verified_date": date,
            "confidence": confidence,
        })
    return steps_out


def confidence_badge(confidence: str) -> str:
    return "✅ verified" if confidence == "verified" else "⚠️ check with a human"


if __name__ == "__main__":
    from engine.retrieval import retrieve
    from engine.generate import generate_structured
    from engine.escalation import is_high_stakes

    q = "How do I open a bank account as an F-1 student?"
    r = retrieve(q, journey="A_bank_account")
    structured = generate_structured(q, r["chunks"])
    steps = build_checklist(structured, r["chunks"], high_stakes=is_high_stakes(q))
    print("answerable:", structured.get("answerable"), "| summary:", structured.get("summary"))
    for s in steps:
        print(f"\n{s['order']}. {s['action']}")
        if s["documents"]:
            print(f"   docs: {', '.join(s['documents'])}")
        print(f"   {confidence_badge(s['confidence'])} | {s['source_name']} ({s['last_verified_date']})")
        print(f"   link: {s['source_url']}")
