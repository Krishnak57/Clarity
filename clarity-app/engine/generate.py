"""Grounded generation — the LLM answers STRICTLY from retrieved passages.

Uses the Groq free tier (Llama 3.3 70B). The API key is read from the .env file
(GROQ_API_KEY) and never hardcoded. The model receives only the retrieved
passages plus the user's situation, and is instructed to abstain when the
passages don't contain the answer.
"""
from functools import lru_cache

from dotenv import load_dotenv
from groq import Groq

import config

# Load .env so GROQ_API_KEY is available (config re-reads it below).
load_dotenv(dotenv_path=config.BASE_DIR.parent / ".env")

ABSTAIN_SENTINEL = "I don't have a verified answer for that."


@lru_cache(maxsize=1)
def _client() -> Groq:
    import os
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Add it to the .env file at the repo root."
        )
    return Groq(api_key=key)


@lru_cache(maxsize=1)
def _system_template() -> str:
    with open(config.SYSTEM_PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def _format_passages(chunks: list[dict]) -> str:
    """Render retrieved chunks into a clearly-delimited block for the prompt."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        blocks.append(
            f"[Passage {i}]\n"
            f"source_name: {c.get('source_name')}\n"
            f"source_url: {c.get('source_url')}\n"
            f"last_verified_date: {c.get('last_verified_date')}\n"
            f"jurisdiction: {c.get('jurisdiction')}\n"
            f"text: {c.get('text')}\n"
        )
    return "\n".join(blocks) if blocks else "(no passages provided)"


def generate_answer(user_situation: str, chunks: list[dict]) -> str:
    """Call the LLM with the strict grounding prompt. Returns the answer text."""
    prompt = _system_template().format(
        retrieved_passages=_format_passages(chunks),
        user_situation=user_situation,
    )
    resp = _client().chat.completions.create(
        model=config.GROQ_MODEL,
        temperature=config.LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_situation},
        ],
    )
    return resp.choices[0].message.content.strip()


# --- Structured generation (for the checklist UI) ---------------------------

_JSON_INSTRUCTION = """
Return ONLY a JSON object with this exact shape:
{
  "answerable": true or false,
  "summary": "one plain-language sentence answering the user, or empty if not answerable",
  "steps": [
    {
      "action": "what the user should do, in plain language",
      "documents": ["document or item needed", "..."],
      "source_passage": <the Passage number (1-based) this step is grounded in>
    }
  ]
}

Rules:
- Use ONLY the SOURCE PASSAGES. If they do not contain the answer, set
  "answerable": false, "summary": "", and "steps": [].
- Every step MUST set "source_passage" to the passage number it comes from.
- Do NOT invent steps, documents, links, or dates. Plain, short language.
- Do NOT include source names or dates inside the text — those are added later
  from the passage metadata.
"""


def generate_structured(user_situation: str, chunks: list[dict]) -> dict:
    """Grounded generation that returns structured steps for the checklist UI.

    The model supplies plain-language actions and points each step at the passage
    it came from; source name/url/date are attached later from chunk metadata
    (so no citation is ever model-fabricated).
    """
    import json

    prompt = _system_template().format(
        retrieved_passages=_format_passages(chunks),
        user_situation=user_situation,
    ) + "\n" + _JSON_INSTRUCTION

    resp = _client().chat.completions.create(
        model=config.GROQ_MODEL,
        temperature=config.LLM_TEMPERATURE,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_situation},
        ],
    )
    raw = resp.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"answerable": False, "summary": "", "steps": []}

    # Normalize shape defensively.
    data.setdefault("answerable", False)
    data.setdefault("summary", "")
    data.setdefault("steps", [])
    return data


if __name__ == "__main__":
    from engine.retrieval import retrieve

    q = "How do I open a bank account as an F-1 student?"
    r = retrieve(q, journey="A_bank_account")
    print(f"top_score={r['top_score']:.3f} abstain={r['abstain']}\n")
    print(generate_answer(q, r["chunks"]))
